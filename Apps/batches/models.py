import os
from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from Apps.recipe_manager.models import Recipe, Process

USER_FOREIGN_KEY = "auth.User"


class Batch(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(USER_FOREIGN_KEY, related_name='batch_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    start_date = models.DateTimeField(auto_now_add=True)
    related_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def get_qrcode(self):
        return QrCode.objects.filter(batch=self).first()

    def get_progress_percentage(self):
        duration = self.related_recipe.time_until_complete()
        progress_duration = timezone.now() - self.start_date
        return min(100, round(progress_duration / duration * 100))

    def get_end_date(self):
        return self.start_date + self.related_recipe.time_until_complete()

    def get_executions_overdue(self):
        return [e for e in self.get_executions() if e.is_overdue()]

    def get_executions(self):
        return Execution.objects.filter(related_batch=self).order_by("execution_datetime")

    def create_next_executions(self):
        # TODO: If process frequency changes, delete old entries
        for process in self.related_recipe.get_processes():
            for schedule in process.get_process_schedule():
                next_execution_datetime = schedule.get_next_execution(self.start_date + timedelta(milliseconds=100))
                if next_execution_datetime is None:
                    continue
                Execution.objects.get_or_create(owner=self.owner, execution_datetime=next_execution_datetime,
                                                related_process=process, related_batch=self)

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
    related_process = models.ForeignKey(Process, on_delete=models.CASCADE)
    related_batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    notification_sent = models.BooleanField(default=False)

    def is_overdue(self):
        return self.execution_datetime < timezone.now()

    def archive(self):
        self.delete()
