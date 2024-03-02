import os
from celery import Celery
from celery.schedules import crontab


# Set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BulletinBoard.settings')

app = Celery('BulletinBoard')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'weekly_newsletter': {
        'task': 'board.tasks.adverts_weekly_newsletter',
        'schedule': crontab(hour='20', minute='0', day_of_week='fri'),
    },
}
