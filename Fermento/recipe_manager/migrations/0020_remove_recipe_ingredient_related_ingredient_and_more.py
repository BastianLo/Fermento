# Generated by Django 4.2 on 2023-04-08 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0019_recipe_ingredient_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe_ingredient',
            name='related_ingredient',
        ),
        migrations.DeleteModel(
            name='ingredient',
        ),
    ]
