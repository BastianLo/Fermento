# Generated by Django 4.2 on 2023-04-16 21:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import encrypted_model_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('settings_manager', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='settings_notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pushover_user_token', encrypted_model_fields.fields.EncryptedCharField()),
                ('pushover_app_token', encrypted_model_fields.fields.EncryptedCharField()),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='notification_credentials',
        ),
    ]