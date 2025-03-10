"""
游戏引擎
负责管理游戏的主循环、场景切换和资源加载
"""

import sys
import pygame
import time
from utils.resource_loader import ResourceLoader
from utils.font_manager import FontManager, init_font_manager
from scenes.scene_manager import SceneManager
from ui.ui_manager import UIManager
import config  # 导入配置模块

class GameEngine:
    """
    游戏引擎类
    负责管理游戏的主循环、场景切换和资源加载
    """
    
    def __init__(self):
        """初始化游戏引擎"""
        print("正在启动植物大战僵尸风格贪吃蛇游戏...")
        
        # 初始化pygame
        pygame.init()
        print("Pygame已初始化")
        
        # 创建游戏窗口
        self.window = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption(config.WINDOW_TITLE)
        
        # 设置游戏时钟
        self.clock = pygame.time.Clock()
        
        # 游戏状态
        self.running = True
        self.paused = False
        
        # 添加配置模块引用
        self.config = config
        
        # 游戏设置
        self.settings = config.DEFAULT_SETTINGS.copy()
        
        # 加载资源
        self.resource_loader = ResourceLoader()
        self.resource_loader.set_game_engine(self)  # 设置游戏引擎引用
        
        # 初始化字体管理器
        self.font_manager = init_font_manager()
        
        # 初始化UI管理器
        self.ui_manager = UIManager(self)
        
        # 初始化场景管理器
        self.scene_manager = SceneManager(self)
        
        # 加载音乐和音效
        self.resource_loader.load_sounds()
        
        print("游戏引擎初始化完成")
    
    def main_loop(self):
        """游戏主循环"""
        last_time = time.time()
        
        try:
            while self.running:
                # 计算时间增量
                current_time = time.time()
                delta_time = current_time - last_time
                last_time = current_time
                
                # 处理事件
                self.handle_events()
                
                # 更新游戏状态
                if not self.paused:
                    self.update(delta_time)
                
                # 渲染游戏
                self.render()
                
                # 控制帧率
                self.clock.tick(config.FPS)
        
        except Exception as e:
            print(f"游戏运行出错: {e}")
            import traceback
            traceback.print_exc()
            
            # 记录更多调试信息
            print("\n--- 调试信息 ---")
            print(f"当前场景: {self.scene_manager.current_scene_name}")
            if hasattr(self.scene_manager.current_scene, 'snake'):
                snake = self.scene_manager.current_scene.snake
                print(f"蛇的位置: {snake.positions}")
                print(f"蛇的方向: {snake.direction}")
                print(f"蛇的下一个方向: {snake.next_direction}")
            print("----------------\n")
        
        finally:
            # 游戏结束，清理资源
            self.cleanup()
            
            # 等待用户按键退出
            print("按回车键退出...")
            input()
    
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            # 退出事件
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # 按键事件
            if event.type == pygame.KEYDOWN:
                # ESC键暂停/继续游戏
                if event.key == pygame.K_ESCAPE:
                    self.toggle_pause()
                
                # 方向键事件直接传递给场景管理器
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    self.scene_manager.handle_event(event)
                    continue
            
            # 先让UI管理器处理事件
            if self.ui_manager.handle_event(event):
                continue
            
            # 再让场景管理器处理事件
            self.scene_manager.handle_event(event)
    
    def update(self, delta_time):
        """更新游戏状态"""
        # 更新场景
        self.scene_manager.update(delta_time)
        
        # 更新UI
        self.ui_manager.update(delta_time)
    
    def render(self):
        """渲染游戏"""
        # 清空屏幕
        self.window.fill((0, 0, 0))
        
        # 渲染当前场景
        self.scene_manager.render(self.window)
        
        # 渲染UI
        self.ui_manager.render(self.window)
        
        # 更新显示
        pygame.display.flip()
    
    def toggle_pause(self):
        """切换游戏暂停状态"""
        self.paused = not self.paused
        self.ui_manager.on_pause_changed(self.paused)
    
    def change_scene(self, scene_name, **kwargs):
        """
        切换场景
        
        参数:
            scene_name: 场景名称
            **kwargs: 传递给场景的参数
        """
        # 清除UI管理器的活动按钮，避免UI元素重叠
        if scene_name == "game":
            self.ui_manager.active_buttons = []
            self.ui_manager.active_group = None
        elif scene_name == "menu":
            self.ui_manager.set_active_group("main_menu")
        elif scene_name == "game_over":
            self.ui_manager.set_active_group("game_over")
        
        # 切换场景
        self.scene_manager.change_scene(scene_name, **kwargs)
    
    def cleanup(self):
        """清理游戏资源"""
        pygame.quit()
    
    def restart(self):
        """重新开始游戏"""
        self.change_scene("game")
        self.paused = False
        
    def set_setting(self, key, value):
        """
        设置游戏设置
        
        参数:
            key: 设置键
            value: 设置值
        """
        self.settings[key] = value
        
        # 如果是音量设置，更新音量
        if key == "music_volume":
            self.resource_loader.set_music_volume(value)
        elif key == "sfx_volume":
            self.resource_loader.set_sfx_volume(value)
    
    def get_setting(self, key, default=None):
        """
        获取游戏设置
        
        参数:
            key: 设置键
            default: 默认值
            
        返回:
            设置值
        """
        return self.settings.get(key, default)

def main():
    """游戏入口函数"""
    game = GameEngine()
    
    # 启动场景管理器，进入主菜单场景
    game.scene_manager.start()
    
    # 开始游戏主循环
    game.main_loop()

if __name__ == "__main__":
    main() 