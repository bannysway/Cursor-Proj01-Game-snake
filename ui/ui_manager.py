"""
UI管理器
负责管理游戏中的UI元素
"""

import pygame
from ui.buttons import Button, AnimatedButton, IconButton

class UIManager:
    """
    UI管理器类
    负责管理游戏中的UI元素
    """
    
    def __init__(self, game_engine):
        """
        初始化UI管理器
        
        参数:
            game_engine: 游戏引擎实例
        """
        self.game_engine = game_engine
        self.resource_loader = game_engine.resource_loader
        self.font_manager = game_engine.font_manager
        self.window = game_engine.window
        
        # UI元素
        self.buttons = {}  # 按钮 {name: button}
        self.active_buttons = []  # 当前活动的按钮
        
        # UI组
        self.button_groups = {}  # 按钮组 {group_name: [button_names]}
        self.active_group = None  # 当前活动的按钮组
        
        # 初始化UI
        self._init_ui()
    
    def _init_ui(self):
        """初始化UI元素"""
        # 创建按钮
        self._create_buttons()
        
        # 创建按钮组
        self._create_button_groups()
    
    def _create_buttons(self):
        """创建按钮"""
        window_width, window_height = self.window.get_size()
        
        # 创建开始按钮
        start_button = AnimatedButton(
            window_width // 2 - 100,
            window_height // 2,
            200, 50,
            "开始游戏",
            lambda: self.game_engine.change_scene("game"),
            sound="menu_click"
        )
        start_button.ui_manager = self
        self.buttons["start_button"] = start_button
        
        # 创建设置按钮
        settings_button = AnimatedButton(
            window_width // 2 - 100,
            window_height // 2 + 70,
            200, 50,
            "设置",
            lambda: self.set_active_group("settings"),
            sound="menu_click"
        )
        settings_button.ui_manager = self
        self.buttons["settings_button"] = settings_button
        
        # 创建退出按钮
        exit_button = AnimatedButton(
            window_width // 2 - 100,
            window_height // 2 + 140,
            200, 50,
            "退出游戏",
            lambda: self._exit_game(),
            sound="menu_click"
        )
        exit_button.ui_manager = self
        self.buttons["exit_button"] = exit_button
        
        # 创建返回按钮
        back_button = AnimatedButton(
            window_width // 2 - 100,
            window_height // 2 + 210,
            200, 50,
            "返回",
            lambda: self.set_active_group("main_menu"),
            sound="menu_click"
        )
        back_button.ui_manager = self
        self.buttons["back_button"] = back_button
        
        # 创建重新开始按钮
        restart_button = AnimatedButton(
            window_width // 2 - 100,
            window_height // 2 + 70,
            200, 50,
            "重新开始",
            lambda: self.game_engine.change_scene("game"),
            sound="menu_click"
        )
        restart_button.ui_manager = self
        self.buttons["restart_button"] = restart_button
        
        # 创建返回主菜单按钮
        menu_button = AnimatedButton(
            window_width // 2 - 100,
            window_height // 2 + 140,
            200, 50,
            "返回主菜单",
            lambda: self.game_engine.change_scene("menu"),
            sound="menu_click"
        )
        menu_button.ui_manager = self
        self.buttons["menu_button"] = menu_button
    
    def _create_button_groups(self):
        """创建按钮组"""
        # 主菜单按钮组
        self.button_groups["main_menu"] = ["start_button", "settings_button", "exit_button"]
        
        # 设置菜单按钮组
        self.button_groups["settings"] = ["back_button"]
        
        # 游戏结束按钮组
        self.button_groups["game_over"] = ["restart_button", "menu_button", "exit_button"]
        
        # 暂停菜单按钮组
        self.button_groups["pause_menu"] = ["restart_button", "menu_button", "exit_button"]
        
        # 默认激活主菜单
        self.set_active_group("main_menu")
    
    def set_active_group(self, group_name):
        """
        设置当前活动的按钮组
        
        参数:
            group_name: 按钮组名称
        """
        if group_name in self.button_groups:
            self.active_group = group_name
            self.active_buttons = [self.buttons[name] for name in self.button_groups[group_name]]
    
    def handle_event(self, event):
        """
        处理UI事件
        
        参数:
            event: Pygame事件对象
            
        返回:
            bool: 事件是否被处理
        """
        # 如果没有活动按钮，直接返回
        if not self.active_buttons:
            return False
        
        # 处理按钮事件
        for button in self.active_buttons:
            if button.handle_event(event):
                return True
        
        return False
    
    def update(self, delta_time):
        """
        更新UI状态
        
        参数:
            delta_time: 时间增量
        """
        # 更新活动按钮
        for button in self.active_buttons:
            button.update(delta_time)
    
    def render(self, surface):
        """
        渲染UI
        
        参数:
            surface: 渲染目标表面
        """
        # 渲染活动按钮
        for button in self.active_buttons:
            button.render(surface)
    
    def on_pause_changed(self, paused):
        """
        处理游戏暂停状态变化
        
        参数:
            paused: 是否暂停
        """
        if paused:
            self.set_active_group("pause_menu")
        else:
            self.active_buttons = []
    
    def _exit_game(self):
        """退出游戏"""
        self.game_engine.running = False

# UI管理器单例
_ui_manager = None

def init_ui_manager(game_engine):
    """初始化UI管理器"""
    global _ui_manager
    _ui_manager = UIManager(game_engine)
    return _ui_manager

def get_ui_manager():
    """获取UI管理器实例"""
    return _ui_manager 