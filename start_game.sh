#!/bin/bash
echo "正在启动植物大战僵尸风格贪吃蛇游戏..."
python3 main.py

if [ $? -ne 0 ]; then
    echo "游戏启动失败！请确保已安装Python和Pygame库。"
    echo "您可以运行以下命令安装Pygame: pip3 install pygame"
    read -p "按回车键退出..." 
fi 