from django.db import models

from encrypted_model_fields.fields import EncryptedCharField
from django.contrib.auth.models import User


class settings_notification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    #Pushover
    pushover_enabled = models.BooleanField(default=False)
    pushover_user_token = EncryptedCharField(max_length=100)
    pushover_app_token = EncryptedCharField(max_length=100)
