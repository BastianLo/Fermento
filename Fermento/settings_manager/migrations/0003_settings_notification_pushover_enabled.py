# Generated by Django 4.2 on 2023-04-16 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings_manager', '0002_settings_notification_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings_notification',
            name='pushover_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
