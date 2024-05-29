#!/bin/bash
project=backend

# 删除正在运行的容器
delete_running_containers(){
    echo "检查是否有容器正在运行..."
    running_containers=$(docker ps -q --filter="name=$project")
    if [ -n "$running_containers" ]; then
        echo "发现正在运行的容器，将它们删除..."
        docker-compose -p $project down
        echo "已删除正在运行的容器"
    else
        echo "没有发现正在运行的容器"
    fi
}

# 部署函数
deploy(){
	echo "开始部署项目"
	echo "注意部署项目会强制构建镜像"
	docker-compose -p $project up -d --build && echo "部署成功"
}

# 开始函数
start(){
    # 删除正在运行的容器
    delete_running_containers
    # 部署项目
    deploy
}

# 执行开始函数
start
