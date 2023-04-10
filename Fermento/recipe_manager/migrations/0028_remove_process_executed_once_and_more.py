# Generated by Django 4.2 on 2023-04-09 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0027_remove_process_start_time_process_schedule'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='executed_once',
        ),
        migrations.AddField(
            model_name='process_schedule',
            name='executed_once',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
