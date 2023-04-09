# Generated by Django 4.2 on 2023-04-08 22:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0026_process_executed_once_process_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='process',
            name='start_time',
        ),
        migrations.CreateModel(
            name='process_schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DurationField(default=datetime.timedelta(0))),
                ('end_time', models.DurationField(default=datetime.timedelta(0))),
                ('wait_time', models.DurationField(default=datetime.timedelta(0))),
                ('related_process', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe_manager.process')),
            ],
        ),
    ]