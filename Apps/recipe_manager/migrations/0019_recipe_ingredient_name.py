# Generated by Django 4.2 on 2023-04-08 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0018_recipe_preparation_duration_recipe_total_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe_ingredient',
            name='name',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
