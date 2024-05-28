from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)

# 服务监听ip和端口
bind = '0.0.0.0:8000'
# 调试模式下设置为True，有代码修改会自动重启，生产环境要设置为False
reload = False
# gunicorn的进程pid文件，关闭操作依赖这个文件
pidfile = '/tmp/gunicorn.pid'   # linux 的绝对路径
accesslog = str(BASE_DIR / 'logs/gunicorn_access.log')   # 通过的日志文件
errorlog = str(BASE_DIR / 'logs/gunicorn_error.log')  # 其他日志文件
