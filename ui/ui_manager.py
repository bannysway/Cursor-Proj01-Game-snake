"""
UI管理器
负责管理和渲染UI元素
"""

import pygame
from config import PVZ_GREEN, PVZ_DARK_GREEN, WHITE, PVZ_BROWN

class UIManager:
    """UI管理器类，处理游戏中所有的UI元素"""
    
    def __init__(self, game_engine):
        """初始化UI管理器"""
        self.game_engine = game_engine
        self.window = game_engine.window
        self.font_manager = game_engine.font_manager
        self.resource_loader = game_engine.resource_loader
        
        # UI元素集合
        self.elements = {}
        
        # 当前活动的UI组
        self.active_group = None
    
    def add_element(self, element_id, element, group=None):
        """添加UI元素"""
        if group not in self.elements:
            self.elements[group] = {}
        
        self.elements[group][element_id] = element
        
        # 设置元素的父UI管理器
        element.ui_manager = self
        
        return element
    
    def remove_element(self, element_id, group=None):
        """移除UI元素"""
        if group in self.elements and element_id in self.elements[group]:
            del self.elements[group][element_id]
            return True
        return False
    
    def get_element(self, element_id, group=None):
        """获取UI元素"""
        if group in self.elements and element_id in self.elements[group]:
            return self.elements[group][element_id]
        return None
    
    def set_active_group(self, group):
        """设置活动UI组"""
        self.active_group = group
    
    def update(self, delta_time):
        """更新所有UI元素"""
        if self.active_group in self.elements:
            for element in self.elements[self.active_group].values():
                if hasattr(element, 'update') and callable(element.update):
                    element.update(delta_time)
    
    def render(self):
        """渲染所有UI元素"""
        if self.active_group in self.elements:
            for element in self.elements[self.active_group].values():
                element.render(self.window)
    
    def handle_event(self, event):
        """处理事件"""
        if self.active_group in self.elements:
            for element in self.elements[self.active_group].values():
                if hasattr(element, 'handle_event') and callable(element.handle_event):
                    if element.handle_event(event):
                        return True  # 事件已处理
        return False
    
    def clear_group(self, group):
        """清除某个UI组的所有元素"""
        if group in self.elements:
            self.elements[group] = {}
    
    def clear_all(self):
        """清除所有UI元素"""
        self.elements = {}

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