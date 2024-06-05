# 从哪个镜像开始构建
FROM python:3.9.7-alpine
# 注释标签
LABEL maintainer='heshaojun'
LABEL description='Django project'

# 创建/app目录并切换进目录下
WORKDIR /app
# 拷贝代码到镜像中
# 拷贝文件到镜像中
# 第一个目录是宿主机目录，第二个目录是镜像的目录
# 第一个目录是相对路径，相对Dockerfile所在的目录
# 第二个目录如果是相对路径，那么就是以workdir的目录
COPY . .

# 安装必要的库
# RUN执行shell命令
# build的时候执行
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories && \
    apk update && \
    apk upgrade && \
    apk add --no-cache tzdata mariadb-dev gcc libc-dev && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone && \
    python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple --upgrade pip && \
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt && \
    chmod +x ./entrypoint.sh

# 创建日志挂载点避免容器越来越大
VOLUME /app/logs/

# 挂载端口
EXPOSE 8000

# 启动容器后会执行的命令
# 执行shell命令
# CMD

ENTRYPOINT [ "./entrypoint.sh" ]
