from django.db import models
from datetime import timedelta

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
    preparation_duration = models.DurationField(default=timedelta(minutes=0))
    total_duration = models.DurationField(default=timedelta(minutes=0))
    difficulty = models.CharField(choices=recipe_difficulty.choices, max_length=20, default=recipe_difficulty.undefined)

    def __str__(self):
        return  f"recipe_{self.id}_{self.name}"

class recipe_ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.User', related_name='recipe_ingredient_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=1, max_digits=7)
    unit = models.CharField(max_length=20)
    related_recipe = models.ForeignKey(recipe, on_delete=models.CASCADE)

    def __str__(self):
        return  f"{self.id}_{self.amount}_{self.unit}_{self.name}"

class process_step(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.User', related_name='process_step_user', on_delete=models.CASCADE)
    index = models.IntegerField()
    text = models.CharField(max_length=1000)
    related_recipe = models.ForeignKey(recipe, on_delete=models.CASCADE)