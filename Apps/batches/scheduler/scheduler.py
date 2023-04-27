import os

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext as _
from notifiers import get_notifier

from Apps.batches.models import Execution
from Apps.settings_manager.models import SettingsNotification


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_scheduled_tasks, 'interval', seconds=int(settings.SCHEDULE_UPDATE_INTERVAL))
    scheduler.start()


def check_scheduled_tasks():
    for execution in Execution.objects.filter(notification_sent=False):
        if timezone.now() > execution.execution_datetime:
            print(f"Execution {execution.id} triggered.")
            send_notifications(execution)
            execution.related_batch.create_next_executions()


def send_notifications(execution):
    notification_settings = SettingsNotification.objects.get(user=execution.owner)
    notofication_data = {
        "title": execution.related_process.name,
        "description": _("Batch") + ": " + execution.related_batch.name + " " + _("HasANewTask"),
        "url": os.getenv("APP_URL") + "/batches/batch/" + str(execution.related_batch.id)
    }
    if notification_settings.pushover_enabled:
        send_notification_pushover(execution, notofication_data)
    execution.notification_sent = True
    execution.save()


def send_notification_pushover(execution, data):
    notification_settings = SettingsNotification.objects.get(user=execution.owner)
    p = get_notifier('pushover')
    p.notify(user=notification_settings.pushover_user_token,
             token=notification_settings.pushover_app_token,
             title=data["title"],
             message=data["description"],
             url=data["url"])
