from config import env
import os
from celery import Celery
import django
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
# 只在Django未初始化时才调用setup
# if not settings.configured:
#     django.setup()

app = Celery('application')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 到celery_tasks里自动发现tasks.py文件
app.autodiscover_tasks(["application.celery_task"])


######任务消费命令：celery  -A application  worker -l info -P eventlet
