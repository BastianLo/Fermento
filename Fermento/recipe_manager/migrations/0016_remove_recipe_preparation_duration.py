# Generated by Django 4.2 on 2023-04-06 08:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0015_alter_recipe_preparation_duration_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='preparation_duration',
        ),
    ]
