#!/bin/sh
# 设置shell若有指令失败立刻退出
# set -e
# 执行数据库迁移
python manage.py makemigrations
python manage.py migrate
if [ $? -ne 0 ];then
    echo '数据库连接失败重启'
    exit 1
fi

# 创建管理员用户
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', '13888888888', '123456')" | python manage.py shell &> /dev/null


# 启动supervisor
supervisord -c supervisord.conf
