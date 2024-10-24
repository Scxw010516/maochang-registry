# -*- coding: utf-8 -*-
from __future__ import absolute_import
import os
from celery import Celery
from config import env

# 只要是想在自己的脚本中访问Django的数据库等文件就必须配置Django的环境变量
os.environ.setdefault(env.DATABASE_NAME, 'application.settings')

# app名字
# app = Celery('application',broker="redis://127.0.0.1:6379/1",backend="redis://127.0.0.1:6379/2")
app = Celery('application',)

# 配置celery
class Config:
    BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'

app.config_from_object(Config)
# 到celery_tasks里自动发现tasks.py文件
app.autodiscover_tasks(["application.celery_task.tasks"])

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

######任务消费命令：celery  -A application  worker -l info -P eventlet