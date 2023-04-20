# Generated by Django 4.2 on 2023-04-06 08:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0017_remove_recipe_total_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='preparation_duration',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AddField(
            model_name='recipe',
            name='total_duration',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]