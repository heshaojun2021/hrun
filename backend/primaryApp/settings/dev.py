# 开发配置模块
# 导入公共配置
from .base_settings import *

ASGI_APPLICATION = "primaryApp.asgi.application"
# 开发配置
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Hrun_db',
        'USER': 'root',
        'PASSWORD': 'pythonvip',
        'PORT': '3307',
        # 'HOST': '172.21.0.3'  # 如果写成了ip，这个ip并不是固定，最好写成容器的名字
                              # docker的网桥维护了一个host，使用容器的名字映射容器的ip
        'HOST': '139.9.38.166'
    }
}


# 跨域配置
# 运行所有域名跨域
CORS_ORIGIN_ALLOW_ALL = True
# 允许cookie跨域，如果前端携带了cookie，必须要配
CORS_ALLOW_CREDENTIALS = True


# celery配置
# 时区
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = 'redis://@139.9.38.166:9000/0'
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
# CELERY_BROKER_URL = 'redis://:pythonvip@192.168.66.101:2000/2'
# 禁止celery自己的日志器
# 然后在django项目中配置日志器
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

# redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://139.9.38.166:9000/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

