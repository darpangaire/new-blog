from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

app = Celery('blog')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Add this 👇
from celery.schedules import crontab

app.conf.beat_schedule = {
    'update-stock-every-10-seconds': {
        'task': 'stockmarket.tasks.update_stock_prices',
        'schedule': 10.0,  # Every 10 seconds
    },
}

app.conf.timezone = 'UTC'

