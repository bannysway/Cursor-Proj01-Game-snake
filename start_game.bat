@echo off
echo 正在启动植物大战僵尸风格贪吃蛇游戏...
python main.py
if %ERRORLEVEL% NEQ 0 (
    echo 游戏启动失败！请确保已安装Python和Pygame库。
    echo 您可以运行以下命令安装Pygame: pip install pygame
    pause
) 