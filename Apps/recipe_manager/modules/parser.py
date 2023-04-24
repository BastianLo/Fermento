import json
import uuid
from io import BytesIO

from PIL import Image, ExifTags
from django.conf import settings
from django.core import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction

from Apps.recipe_manager.models import ProcessStep, RecipeIngredient, Utensils, ProcessSchedule


@transaction.atomic
class RecipeParser:
    def __init__(self):
        self.user = None
        self.recipe = None

    def parse_recipe(self, request):
        recipe_json = json.loads(request.POST.dict()["recipe"])
        self.user = request.user
        # del recipe_json["fields"]["image"]
        # del recipe_json["fields"]["cropping"]
        recipe = list(serializers.deserialize('json', json.dumps([recipe_json])))[0]
        self.recipe = recipe
        recipe.object.owner_id = self.user.id
        if "image" in request.FILES:
            recipe.object.image = downsize_image(request.FILES["image"])
        recipe.object.save()
        self.parse_process(recipe_json["processes"])
        return recipe.object

    def parse_process(self, process_json):
        for process in process_json:
            print(process_json)
            p = list(serializers.deserialize('json', json.dumps([process], ensure_ascii=False)))[0]
            p.object.related_recipe_id = self.recipe.object.id
            p.object.owner_id = self.user.id
            p.save()
            self.parse_process_step(process["process_steps"], p)
            self.parse_ingredients(process["ingredients"], p)
            self.parse_utensils(process["utils"], p)
            self.parse_schedule(process["schedule"], p)

    def parse_process_step(self, process_step_json, process_object):
        steps = list(serializers.deserialize('json', json.dumps([step for step in process_step_json])))
        for index, step in enumerate(steps):
            step.object.index = index
            step.object.owner_id = self.user.id
            step.object.related_process = process_object.object
            step.object.save()
        all_steps = [ps.id for ps in ProcessStep.objects.filter(owner=self.user, related_process=process_object.object)]
        delete_steps = set(all_steps) - set([step.object.id for step in steps])
        [ProcessStep.objects.filter(owner=self.user, id=ds).first().delete() for ds in delete_steps]

    def parse_ingredients(self, ingredient_json, process_object):
        ingredients = list(
            serializers.deserialize('json', json.dumps([step for step in ingredient_json], ensure_ascii=False)))
        for ingredient in ingredients:
            ingredient.object.owner_id = self.user.id
            ingredient.object.related_process = process_object.object
            ingredient.object.save()
        all_ingredients = [ingr.id for ingr in
                           RecipeIngredient.objects.filter(owner=self.user, related_process=process_object.object)]
        delete_ingredients = set(all_ingredients) - set([ingr.object.id for ingr in ingredients])
        [RecipeIngredient.objects.filter(owner=self.user, id=ds).first().delete() for ds in delete_ingredients]

    def parse_utensils(self, utensil_json, process_object):
        utensils = list(
            serializers.deserialize('json', json.dumps([step for step in utensil_json], ensure_ascii=False)))
        for utensil in utensils:
            utensil.object.owner_id = self.user.id
            utensil.object.related_process = process_object.object
            utensil.object.save()
        all_utensils = [utensil.id for utensil in
                        Utensils.objects.filter(owner=self.user, related_process=process_object.object)]
        delete_utensils = set(all_utensils) - set([utensil.object.id for utensil in utensils])
        [Utensils.objects.filter(owner=self.user, id=ds).first().delete() for ds in delete_utensils]

    def parse_schedule(self, schedule_json, process_object):
        schedules = list(
            serializers.deserialize('json', json.dumps([schedule for schedule in schedule_json], ensure_ascii=False)))

        for schedule in schedules:
            schedule.object.owner_id = self.user.id
            schedule.object.related_process = process_object.object
            schedule.object.save()
        all_schedules = [schedule.id for schedule in
                         ProcessSchedule.objects.filter(owner=self.user, related_process=process_object.object)]
        delete_schedules = set(all_schedules) - set([schedule.object.id for schedule in schedules])
        [ProcessSchedule.objects.filter(owner=self.user, id=ds).first().delete() for ds in delete_schedules]


def downsize_image(image):
    if not settings.DOWNSIZE_IMAGES:
        return image
    image = Image.open(image)
    base_width = settings.MAX_IMAGE_WIDTH
    # Rotate the image based on the EXIF orientation tag
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                exif = dict(image._getexif().items())
                if exif[orientation] == 3:
                    image = image.rotate(180, expand=True)
                elif exif[orientation] == 6:
                    image = image.rotate(270, expand=True)
                elif exif[orientation] == 8:
                    image = image.rotate(90, expand=True)
                break
    except (AttributeError, KeyError, IndexError):
        pass

    width_percent = (base_width / float(image.size[0]))
    hsize = int((float(image.size[1]) * float(width_percent)))
    image = image.resize((base_width, hsize), Image.Resampling.LANCZOS)

    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    image_file = InMemoryUploadedFile(buffer, None, f"image_{uuid.uuid4()}.jpg", "image/jpeg",
                                      buffer.getbuffer().nbytes, None)
    return image_file
