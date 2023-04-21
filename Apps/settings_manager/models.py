from django.contrib.auth.models import User
from django.db import models
from encrypted_model_fields.fields import EncryptedCharField


class SettingsNotification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    # Pushover
    pushover_enabled = models.BooleanField(default=False)
    pushover_user_token = EncryptedCharField(max_length=100)
    pushover_app_token = EncryptedCharField(max_length=100)
