from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
import os
import datetime 
from django.utils import timezone

from batches.models import Execution


def start():
    if not os.environ.get('RUN_MAIN'):
        return
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_scheduled_tasks, 'interval', seconds=int(settings.SCHEDULE_UPDATE_INTERVAL))
    scheduler.start()


def check_scheduled_tasks():
    pass
    #print(datetime.datetime.now())
    for execution in Execution.objects.all():
        if timezone.now() > execution.execution_datetime:
            print(f"Execution {execution.id} triggered.")
            #send notification
            execution.delete()
            execution.related_batch.create_next_executions()