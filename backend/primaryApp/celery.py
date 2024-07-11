# -*- coding: utf-8 -*-
# @author: HRUN

import os

from celery import Celery

# 为`celery`设置默认的django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'primaryApp.settings')

app = Celery('primaryApp')

# 设置配置来源为django项目的配置文件
app.config_from_object('django.conf:settings', namespace='CELERY')

# # 加载所有的已注册django应用中的任务
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')  # 打印任务执行的请求信息
