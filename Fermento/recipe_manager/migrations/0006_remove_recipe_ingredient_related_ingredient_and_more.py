# Generated by Django 4.2 on 2023-04-05 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0005_ingredient_owner_recipe_ingredient_owner_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe_ingredient',
            name='related_ingredient',
        ),
        migrations.RemoveField(
            model_name='recipe_ingredient',
            name='related_recipe',
        ),
        migrations.AddField(
            model_name='recipe_ingredient',
            name='related_ingredient',
            field=models.ManyToManyField(to='recipe_manager.ingredient'),
        ),
        migrations.AddField(
            model_name='recipe_ingredient',
            name='related_recipe',
            field=models.ManyToManyField(to='recipe_manager.recipe'),
        ),
    ]
