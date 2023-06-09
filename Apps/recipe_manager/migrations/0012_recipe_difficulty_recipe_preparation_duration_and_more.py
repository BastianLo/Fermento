# Generated by Django 4.2 on 2023-04-06 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe_manager', '0011_process_step'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(choices=[('undefined', 'Undefined'), ('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='undefined', max_length=20),
        ),
        migrations.AddField(
            model_name='recipe',
            name='preparation_duration',
            field=models.DurationField(default=None),
        ),
        migrations.AddField(
            model_name='recipe',
            name='total_duration',
            field=models.DurationField(default=None),
        ),
    ]
