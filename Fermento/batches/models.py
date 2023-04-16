from django.db import models
import os
from recipe_manager.models import recipe, process
from django.db.models.signals import post_save






USER_FOREIGN_KEY = "auth.User"
class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(USER_FOREIGN_KEY, related_name='batch_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    start_date = models.DateTimeField(auto_now_add=True)
    related_recipe = models.ForeignKey(recipe, on_delete=models.CASCADE)

    def get_qrcode(self):
        return QrCode.objects.filter(batch=self).first()
    
    def create_next_executions(self):
        for process in self.related_recipe.get_processes():
            for schedule in process.get_process_schedule():
                next_execution_datetime = schedule.get_next_execution(self.start_date)
                if not next_execution_datetime:
                    continue
                Execution.objects.get_or_create(owner=self.owner, execution_datetime=next_execution_datetime, related_process=process, related_batch=self)

    def model_created_or_updated(sender, **kwargs):
        the_instance = kwargs['instance']
        the_instance.create_next_executions()

post_save.connect(Batch.model_created_or_updated, sender=Batch)

class QrCode(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(USER_FOREIGN_KEY, related_name='qrcode_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    batch = models.OneToOneField(Batch, on_delete=models.CASCADE, null=True)

    def get_url(self):
        return os.getenv("APP_URL") + "/batches/batch/" + str(self.batch.id)
    
class Execution(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(USER_FOREIGN_KEY, related_name='execution_user', on_delete=models.CASCADE)
    execution_datetime = models.DateTimeField()
    related_process = models.ForeignKey(process, on_delete=models.CASCADE)
    related_batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
