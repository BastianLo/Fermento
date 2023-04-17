from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
import os
import datetime 
from django.utils import timezone
from batches.models import Execution
from settings_manager.models import settings_notification
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
            send_notifications(execution)
            execution.delete()
            execution.related_batch.create_next_executions()

def send_notifications(execution):
    notification_settings = settings_notification.objects.get(user=execution.owner)
    if notification_settings.pushover_enabled:
        send_notification_pushover(execution)


def send_notification_pushover(execution):
    notification_settings = settings_notification.objects.get(user=execution.owner)
    p = get_notifier('pushover')
    p.notify(user=notification_settings.pushover_user_token, token=notification_settings.pushover_app_token, message='test')