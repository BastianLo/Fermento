# Generated by Django 4.2 on 2023-04-24 12:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('recipe_manager', '0045_alter_processstep_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='processstep',
            unique_together=set(),
        ),
    ]
