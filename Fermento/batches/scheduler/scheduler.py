from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
import os
import datetime 


def start():
    if not os.environ.get('RUN_MAIN'):
        return
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_scheduled_tasks, 'interval', seconds=int(settings.SCHEDULE_UPDATE_INTERVAL))
    scheduler.start()


def check_scheduled_tasks():
    pass
    #print(datetime.datetime.now())