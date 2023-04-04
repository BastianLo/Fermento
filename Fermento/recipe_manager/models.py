from django.db import models

# Create your models here.

class recipe(models.Model):
    recipe_name = models.CharField(max_length=100)
    recipe_description = models.CharField(max_length=2000)
