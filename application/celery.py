from config import env
import os
from celery import Celery
import django

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'application.settings')
django.setup()

app = Celery('application')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings', namespace='CELERY')
class Config:
    # BROKER_URL = 'redis://127.0.0.1:6379/1'
    # CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/2'
    BROKER_URL = 'redis://redis:6379/1'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/2'
    # BROKER_URL = 'redis://0.0.0.0:6379/1'
    # CELERY_RESULT_BACKEND = 'redis://0.0.0.0:6379/2'

app.config_from_object(Config)
# app.conf.beat_schedule = {
#     'restart-uncalc-frame': {
#         'task': 'application.celery_task.tasks.restart_uncalc_frame',
#         'schedule': 30.0,
#     },
# }
# 到celery_tasks里自动发现tasks.py文件
app.autodiscover_tasks(["application.celery_task"])

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
######任务消费命令：celery  -A application  worker -l info -P eventlet