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
from game_engine import init_game_engine
from utils.font_manager import init_font_manager
from utils.resource_loader import init_resource_loader
from ui.ui_manager import init_ui_manager

def main():
    """游戏主函数"""
    try:
        print("正在启动植物大战僵尸风格贪吃蛇游戏...")
        
        # 检查依赖库
        if not pygame.get_init():
            pygame.init()
            print("Pygame已初始化")
        
        # 初始化游戏引擎
        game = init_game_engine()
        print("游戏引擎初始化完成")
        
        # 启动游戏
        game.start()
    except Exception as e:
        print(f"游戏运行出错: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")

if __name__ == "__main__":
    main() 