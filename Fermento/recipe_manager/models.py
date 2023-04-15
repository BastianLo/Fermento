from django.db import models
from datetime import timedelta
from django.db.models import Sum
import math
from image_cropping import ImageRatioField, ImageCropField

# Create your models here.

USER_FOREIGN_KEY = "auth.User"
class recipe(models.Model):
    class recipe_difficulty(models.TextChoices):
        undefined = 'undefined'
        easy = 'easy'
        medium = 'medium'
        hard = 'hard'

    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(USER_FOREIGN_KEY, related_name='recipe_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    image = ImageCropField(upload_to='images/dynamic', default="images/placeholder/recipe.png")
    cropping = ImageRatioField('image', '600x400')
    difficulty = models.CharField(choices=recipe_difficulty.choices, max_length=20, default=recipe_difficulty.undefined)

    def create_process(self, **kwargs):
        return process.objects.create(owner=self.owner, related_recipe=self, **kwargs)
    def get_description_preview(self):
        CHAR_LIMIT = 100
        if len(self.description) > CHAR_LIMIT:
            return self.description[:CHAR_LIMIT] + "..."
        else:
            return self.description
    def get_total_work_duration(self):
        if len(process.objects.filter(related_recipe=self)) > 0:
            return process.objects.filter(related_recipe=self).aggregate(Sum("work_duration"))["work_duration__sum"]
        else:
            return timedelta(minutes=0)
    def get_total_wait_duration(self):
        return process.objects.filter(related_recipe=self).aggregate(Sum("wait_duration"))["wait_duration__sum"]
    
    def get_processes(self):
        return process.objects.filter(related_recipe=self)
    
    def __str__(self):
        return  f"Recipe_{self.id}_{self.name}"

class process(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(USER_FOREIGN_KEY, related_name='process_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    work_duration = models.DurationField(default=timedelta(minutes=0))
    wait_duration = models.DurationField(default=timedelta(minutes=0))
    related_recipe = models.ForeignKey(recipe, on_delete=models.CASCADE)

    def create_schedule(self, **kwargs):
        return process_schedule.objects.create(owner=self.owner, related_process=self, **kwargs)
    def create_recipe_ingredient(self, **kwargs):
        return recipe_ingredient.objects.create(owner=self.owner, related_process=self, **kwargs)
    def create_process_step(self, **kwargs):
        return process_step.objects.create(owner=self.owner, related_process=self, **kwargs)
    def create_utensil(self, **kwargs):
        return utensils.objects.create(owner=self.owner, related_process=self, **kwargs)

    def get_ingredients(self):
        return recipe_ingredient.objects.filter(related_process=self)
    def get_utensils(self):
        return utensils.objects.filter(related_process=self)
    def get_process_steps(self):
        return process_step.objects.filter(related_process=self).order_by("index")
    def get_process_schedule(self):
        return process_schedule.objects.filter(related_process=self)

    def __str__(self) -> str:
        return f"Process_{self.id}_{self.name}_{self.related_recipe}"

class process_schedule(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(USER_FOREIGN_KEY, related_name='schedule_user', on_delete=models.CASCADE)
    related_process = models.ForeignKey(process, on_delete=models.CASCADE)
    #True, if this process only gets executed once and is not repeated
    executed_once = models.BooleanField()
    #Time from batch start, when the schedule starts
    start_time = models.DurationField(default=timedelta(minutes=0))
    #Time from batch start, when the schedule ends
    end_time = models.DurationField(default=timedelta(minutes=0))
    #How often the process gets triggered
    wait_time = models.DurationField(default=timedelta(minutes=0))

    def get_total_execution_count(self):
        if self.executed_once:
            return 1
        if not self.end_time:
            return "∞"
        return math.floor((self.end_time - self.start_time)/self.wait_time)
    
    def __str__(self):
        return  f"ProcessSchedule{self.id}"

class recipe_ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(USER_FOREIGN_KEY, related_name='recipe_ingredient_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=1, max_digits=7)
    unit = models.CharField(max_length=20)
    related_process = models.ForeignKey(process, on_delete=models.CASCADE)
    #TODO: Add index in recipe
    def __str__(self):
        return  f"RecipeIngredient_{self.id}_{self.amount}_{self.unit}_{self.name}"

class process_step(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(USER_FOREIGN_KEY, related_name='process_step_user', on_delete=models.CASCADE)
    index = models.IntegerField()
    text = models.CharField(max_length=1000)
    related_process = models.ForeignKey(process, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"ProcessStep_{self.id}_{self.index}_{self.related_process}"
    
class utensils(models.Model):
    id = models.AutoField(primary_key=True)
    related_process = models.ForeignKey(process, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(USER_FOREIGN_KEY, related_name='utensil_user', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"Utensil_{self.id}"