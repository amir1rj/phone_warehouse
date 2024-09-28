import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "Warehousing.settings")
app = Celery('Warehousing')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
