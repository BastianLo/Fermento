from django.db import models

# Create your models here.

class recipe(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('auth.User', related_name='announces', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)

    def __str__(self):
        return  f"{self.id}_{self.name}"