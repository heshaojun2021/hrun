# 生产配置模块
# 导入公共配
from .base_settings import *

# 生产配置
DEBUG = False

# 允许的域名与主机
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'HRUN',
        'USER': 'root',
        'PASSWORD': 'pythonvip',
        'PORT': '3306',
        'HOST': 'mariadb'
    }
}

# 跨域配置
# 运行所有域名跨域
CORS_ALLOW_ALL_ORIGINS = True
# 允许cookie跨域，如果前端携带了cookie，必须要配
CORS_ALLOW_CREDENTIALS = True

# celery配置
CELERY_BROKER_URL = 'redis://redis:6379/0'  # 参考数据库host也要写成redis容器名
CELERY_TIMEZONE = "Asia/Shanghai"
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_WORKER_HIJACK_ROOT_LOGGER = False


# redis
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
