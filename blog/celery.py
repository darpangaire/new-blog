# myproject/celery.py

import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

app = Celery('stockmarket')


app.config_from_object('django.conf:settings',
                       namespace='CELERY')

# Load task modules from all registered Django app configs.
app.conf.beat_schedule = {
  'every_10_seconds':{
    'task':'stockmarket.tasks.update_stock_prices',
    'schedule':10,
    'args':(),
  },
}

# Auto-discover tasks
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    





