import json

from django.core import serializers
from django.db import transaction

from Apps.recipe_manager.models import ProcessStep, RecipeIngredient, Utensils, ProcessSchedule


@transaction.atomic
class RecipeParser:
    def parse_recipe(self, user, recipe_json):
        self.user = user
        recipe = list(serializers.deserialize('json', json.dumps(recipe_json)))[0]
        recipe.object.save()
        self.parse_process(recipe_json[0]["processes"])

    def parse_process(self, process_json):
        for process in process_json:
            p = list(serializers.deserialize('json', json.dumps([process], ensure_ascii=False)))[0]
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
        print(list(
            serializers.deserialize('json', json.dumps([schedule for schedule in schedule_json], ensure_ascii=False))))
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
