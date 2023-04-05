from django.db import models

# Create your models here.

class recipe(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.User', related_name='recipe_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return  f"recipe_{self.id}_{self.name}"

class ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.User', related_name='ingredient_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return  f"ingredient_{self.id}_{self.name}"

class recipe_ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.User', related_name='recipe_ingredient_user', on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=1, max_digits=7)
    unit = models.CharField(max_length=20)
    related_recipe = models.ForeignKey(recipe, on_delete=models.CASCADE)
    related_ingredient = models.ForeignKey(ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return  f"{self.id}_{self.amount}_{self.unit}"
