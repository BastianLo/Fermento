# Generated by Django 4.2 on 2023-04-21 15:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('recipe_manager', '0044_recipe_created_at'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='processstep',
            unique_together={('related_process', 'index')},
        ),
    ]
