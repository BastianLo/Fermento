# Generated by Django 4.2 on 2023-04-21 09:23

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe_manager', '0042_alter_recipe_rating'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='process_schedule',
            new_name='ProcessSchedule',
        ),
        migrations.RenameModel(
            old_name='process_step',
            new_name='ProcessStep',
        ),
        migrations.RenameModel(
            old_name='recipe_ingredient',
            new_name='RecipeIngredient',
        ),
    ]
