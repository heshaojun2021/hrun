# backend

#### 介绍
学习交流分享

#### 软件架构
软件架构说明
```
    Mysql
    Django
    Python
    Nginx
    Redis
    Celery
    Docker
    Jenkins
```

#### 安装教程
手动部署
```
1、创建虚拟环境执行依赖包：pip install -r requirements.txt
2、backend/primaryApp/settings/dev.py或pro.py修改自己的数据库和Redis配置信息
3、数据库迁移：python manage.py makemigrations
4、数据库执行迁移文件：python manage.py migrate
5、运行Django服务：python manage.py runserver
```
自动部署
```
1、服务器中安装docker和docker-compose
2、运行 sh deploy.sh
```
#### 使用说明
static配置文件生成
```
python manage.py collectstatic
```
数据库迁移
```
python manage.py makemigrations
```
数据库执行迁移文件
```
python manage.py migrate
```
运行Django服务
```
python manage.py runserver
```
#### 项目目录结构

#### 参与贡献
