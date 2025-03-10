"""
游戏引擎
负责游戏的主循环和统筹管理
"""

import pygame
import sys
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, FPS, 
    DEFAULT_SETTINGS  # 添加DEFAULT_SETTINGS导入
)
from utils.font_manager import init_font_manager, get_font_manager
from utils.resource_loader import init_resource_loader, get_resource_loader
from scenes.scene_manager import SceneManager
from ui.ui_manager import init_ui_manager, get_ui_manager

class GameEngine:
    """
    游戏引擎类
    负责初始化游戏、运行游戏主循环并管理游戏状态
    """
    
    def __init__(self):
        """初始化游戏引擎"""
        # 初始化pygame
        pygame.init()
        
        # 创建游戏窗口
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        
        # 创建时钟对象
        self.clock = pygame.time.Clock()
        
        # 游戏设置 - 移到前面
        self.settings = DEFAULT_SETTINGS.copy()
        
        # 初始化字体管理器
        self.font_manager = init_font_manager()
        
        # 初始化资源加载器
        self.resource_loader = init_resource_loader()
        
        # 初始化UI管理器
        self.ui_manager = init_ui_manager(self)
        
        # 初始化场景管理器
        self.scene_manager = SceneManager(self)
        
        # 游戏状态
        self.running = False
        self.paused = False
        
        # 最后一次循环的时间和这一次循环的时间差（毫秒）
        self.delta_time = 0
        self.last_time = pygame.time.get_ticks()
    
    def start(self):
        """启动游戏"""
        self.running = True
        self.scene_manager.start()
        self.main_loop()
    
    def main_loop(self):
        """游戏主循环"""
        while self.running:
            # 计算帧间隔时间
            current_time = pygame.time.get_ticks()
            self.delta_time = (current_time - self.last_time) / 1000.0  # 转换为秒
            self.last_time = current_time
            
            # 处理事件
            self.handle_events()
            
            # 如果游戏未暂停，更新游戏状态
            if not self.paused:
                self.update()
            
            # 渲染游戏画面
            self.render()
            
            # 控制帧率
            self.clock.tick(FPS)
    
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            # 处理窗口关闭事件
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            
            # 处理键盘事件
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # ESC键退出游戏
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # 空格键暂停/继续游戏
                    self.toggle_pause()
            
            # 先让UI管理器处理事件
            if self.ui_manager.handle_event(event):
                continue
                
            # 然后让当前场景处理事件
            self.scene_manager.handle_event(event)
    
    def update(self):
        """更新游戏状态"""
        # 更新UI元素
        self.ui_manager.update(self.delta_time)
        
        # 更新当前场景
        self.scene_manager.update(self.delta_time)
    
    def render(self):
        """渲染游戏画面"""
        # 清空屏幕
        self.window.fill((0, 0, 0))
        
        # 渲染当前场景
        self.scene_manager.render(self.window)
        
        # 渲染UI
        self.ui_manager.render()
        
        # 更新屏幕显示
        pygame.display.flip()
    
    def toggle_pause(self):
        """切换游戏暂停状态"""
        self.paused = not self.paused
        
        # 播放暂停/继续音效
        if self.paused:
            self.resource_loader.play_sound("menu_click")
        else:
            self.resource_loader.play_sound("menu_click")
        
        # 通知当前场景暂停状态变化
        self.scene_manager.on_pause_changed(self.paused)
    
    def change_scene(self, scene_name, **kwargs):
        """切换游戏场景"""
        # 如果游戏处于暂停状态，先恢复
        if self.paused:
            self.paused = False
        
        # 切换场景
        self.scene_manager.change_scene(scene_name, **kwargs)
    
    def set_setting(self, key, value):
        """修改游戏设置"""
        if key in self.settings:
            old_value = self.settings[key]
            self.settings[key] = value
            
            # 根据设置变化进行相应处理
            if key == "music_volume":
                # 调整音乐音量
                self.resource_loader.set_music_volume(value)
            elif key == "sfx_volume":
                # 调整音效音量
                self.resource_loader.set_sfx_volume(value)
            
            # 返回旧值
            return old_value
        return None
    
    def get_setting(self, key, default=None):
        """获取游戏设置"""
        return self.settings.get(key, default)

# 游戏引擎单例
_game_engine = None

def init_game_engine():
    """初始化游戏引擎"""
    global _game_engine
    _game_engine = GameEngine()
    return _game_engine

def get_game_engine():
    """获取游戏引擎实例"""
    return _game_engine 