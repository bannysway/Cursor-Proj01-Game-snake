"""
贪吃蛇游戏 - 植物大战僵尸风格
主入口文件，初始化并启动游戏

版本: 3.0
日期: 2023年3月
"""

import pygame
import sys
import os

# 如果运行不成功，尝试调整一下 Python 模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入游戏引擎
from game_engine import main as start_game

if __name__ == "__main__":
    start_game() 