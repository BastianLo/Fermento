from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
import os
import datetime 
from django.utils import timezone
from batches.models import Execution, notification_credentials
from notifiers import get_notifier


def start():
    if not os.environ.get('RUN_MAIN'):
        return
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_scheduled_tasks, 'interval', seconds=int(settings.SCHEDULE_UPDATE_INTERVAL))
    scheduler.start()


def check_scheduled_tasks():
    for execution in Execution.objects.all():
        if timezone.now() > execution.execution_datetime:
            print(f"Execution {execution.id} triggered.")
            send_notification_pushover(execution)
            execution.delete()
            execution.related_batch.create_next_executions()

def send_notification():
    pass


def send_notification_pushover(execution):
    credentials = notification_credentials.objects.get(user=execution.owner)
    p = get_notifier('pushover')
    p.notify(user=credentials.pushover_user_token, token=credentials.pushover_app_token, message='test')