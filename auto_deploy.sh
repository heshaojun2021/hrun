#!/bin/bash
project=${1:-backend}
echo $project

# 检查容器是否在运行
check_running_containers(){
    # 检查并删除镜像名称为空的镜像
    check_and_delete_empty_images
    echo "检查容器是否在运行..."
    running_containers=$(docker ps -q --filter="name=$project")
    if [ -n "$running_containers" ]; then
        echo "发现正在运行的容器，将执行滚动更新..."
        deploy
    else
        echo "没有发现正在运行的容器"
        delete_stopped_containers
        echo "已删除已停止的容器，现在开始部署项目"
        deploy
    fi
}

# 检查并删除镜像名称为空的镜像
check_and_delete_empty_images(){
    echo "检查是否有镜像名称为空的脏镜像..."
    dirty_images=$(docker images -qf "dangling=true")
    if [ -n "$dirty_images" ]; then
        echo "发现镜像名称为空的脏镜像，将它们删除..."
        docker rmi $dirty_images
        echo "已删除镜像名称为空的脏镜像"
    else
        echo "没有发现镜像名称为空的脏镜像"
    fi
}

# 删除已停止的容器
delete_stopped_containers(){
    echo "检查是否有已停止的容器..."
    stopped_containers=$(docker ps -aq --filter="name=$project" --filter="status=exited")
    if [ -n "$stopped_containers" ]; then
        echo "发现已停止的容器，将它们删除..."
        docker rm $stopped_containers
        echo "已删除已停止的容器"
    else
        echo "没有发现已停止的容器"
    fi
}

# 部署函数
deploy(){
    echo "开始滚动更新项目"
    echo "注意滚动更新项目会逐个更新服务"

    # 获取服务列表
    services=$(docker-compose config --services)

    # 逐个更新服务
    for service in $services; do
        echo "正在滚动更新服务: $service"
        docker-compose -p $project up --no-deps --build -d $service
        if [ $? -eq 0 ]; then
            echo "服务 $service 更新成功"
        else
            echo "服务 $service 更新失败"
        fi
    done

    echo "滚动更新完成"
}

# 执行检查容器函数
check_running_containers