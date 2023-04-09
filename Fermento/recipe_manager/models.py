from django.db import models
from datetime import timedelta
from django.db.models import Sum

# Create your models here.

class recipe(models.Model):
    class recipe_difficulty(models.TextChoices):
        undefined = 'undefined'
        easy = 'easy'
        medium = 'medium'
        hard = 'hard'

    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.User', related_name='recipe_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='images/')
    difficulty = models.CharField(choices=recipe_difficulty.choices, max_length=20, default=recipe_difficulty.undefined)

    def get_total_work_duration(self):
        return process.objects.filter(related_recipe=self).aggregate(Sum("work_duration"))["work_duration__sum"]
    
    def get_total_wait_duration(self):
        return process.objects.filter(related_recipe=self).aggregate(Sum("wait_duration"))["wait_duration"]
    
    def get_processes(self):
        return process.objects.filter(related_recipe=self)
    
    def __str__(self):
        return  f"recipe_{self.id}_{self.name}"

class process(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.User', related_name='process_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    work_duration = models.DurationField(default=timedelta(minutes=0))
    wait_duration = models.DurationField(default=timedelta(minutes=0))
    related_recipe = models.ForeignKey(recipe, on_delete=models.CASCADE)

    #True, if this process only gets executed once and is not repeated
    executed_once = models.BooleanField()

    def get_ingredients(self):
        return recipe_ingredient.objects.filter(related_process=self)
    def get_process_steps(self):
        return process_step.objects.filter(related_process=self)
    def get_process_schedule(self):
        return process_schedule.objects.filter(related_process=self)

    def __str__(self) -> str:
        return f"{self.id}_{self.name}_{self.related_recipe}"

class process_schedule(models.Model):
    related_process = models.ForeignKey(process, on_delete=models.CASCADE)
    #Time from batch start, when the schedule starts
    start_time = models.DurationField(default=timedelta(minutes=0))
    #Time from batch start, when the schedule ends
    end_time = models.DurationField(default=timedelta(minutes=0))
    #How often the process gets triggered
    wait_time = models.DurationField(default=timedelta(minutes=0))

class recipe_ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.User', related_name='recipe_ingredient_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=1, max_digits=7)
    unit = models.CharField(max_length=20)
    related_process = models.ForeignKey(process, on_delete=models.CASCADE)

    def __str__(self):
        return  f"{self.id}_{self.amount}_{self.unit}_{self.name}"

class process_step(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.User', related_name='process_step_user', on_delete=models.CASCADE)
    index = models.IntegerField()
    text = models.CharField(max_length=1000)
    related_process = models.ForeignKey(process, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.id}_{self.index}_{self.related_process}"