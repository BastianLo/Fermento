from django.db import models
import os

# Create your models here.

USER_FOREIGN_KEY = "auth.User"
class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(USER_FOREIGN_KEY, related_name='batch_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)

    def get_qrcode(self):
        return QrCode.objects.filter(batch=self).first()



class QrCode(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(USER_FOREIGN_KEY, related_name='qrcode_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    batch = models.OneToOneField(Batch, on_delete=models.CASCADE, null=True)

    def get_url(self):
        return os.getenv("APP_URL") + "/batches/batch/" + str(self.batch.id)