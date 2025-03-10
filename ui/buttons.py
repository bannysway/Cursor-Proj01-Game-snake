"""
按钮和交互元素
为游戏提供各种UI按钮和交互组件
"""

import pygame
import math
from config import PVZ_GREEN, PVZ_DARK_GREEN, WHITE, PVZ_BROWN

class Button:
    """基础按钮类"""
    
    def __init__(self, x, y, width, height, text="", callback=None,
                 bg_color=PVZ_GREEN, hover_color=None, border_color=PVZ_DARK_GREEN,
                 text_color=WHITE, font_size="medium", border_radius=10, border_width=3,
                 sound="menu_click"):
        """初始化按钮"""
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color or tuple(min(c + 30, 255) for c in bg_color)
        self.border_color = border_color
        self.text_color = text_color
        self.font_size = font_size
        self.border_radius = border_radius
        self.border_width = border_width
        self.sound = sound
        
        # 状态变量
        self.hovered = False
        self.pressed = False
        self.ui_manager = None  # 将在添加到UI管理器时设置
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            return self.hovered
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.hovered:
                self.pressed = True
                return True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.pressed:
                self.pressed = False
                if self.hovered:
                    # 点击声音
                    if self.sound and self.ui_manager:
                        self.ui_manager.resource_loader.play_sound(self.sound)
                    
                    # 执行回调
                    if self.callback:
                        self.callback()
                    return True
        
        return False
    
    def render(self, surface):
        """渲染按钮"""
        # 确定当前颜色
        current_color = self.hover_color if self.hovered else self.bg_color
        
        # 绘制按钮背景
        pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)
        
        # 绘制边框
        pygame.draw.rect(surface, self.border_color, self.rect, 
                        width=self.border_width, border_radius=self.border_radius)
        
        # 如果有文本，绘制文本
        if self.text and self.ui_manager:
            font = self.ui_manager.font_manager.get_font(self.font_size)
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

class WoodButton(Button):
    """木质风格按钮，类似PvZ的木质标牌"""
    
    def __init__(self, x, y, width, height, text="", callback=None,
                 text_color=WHITE, font_size="medium", sound="menu_click"):
        """初始化木质按钮"""
        super().__init__(x, y, width, height, text, callback,
                       PVZ_BROWN, None, (101, 67, 33),
                       text_color, font_size, 15, 4, sound)
        
        # 木质风格特有参数
        self.wood_lines = 3  # 木纹线条数量
    
    def render(self, surface):
        """渲染木质按钮"""
        # 绘制基础按钮
        super().render(surface)
        
        # 添加木纹纹理
        for i in range(self.wood_lines):
            y_pos = self.rect.y + (i + 1) * self.rect.height // (self.wood_lines + 1)
            pygame.draw.line(surface, (101, 67, 33), 
                           (self.rect.x + 10, y_pos),
                           (self.rect.x + self.rect.width - 10, y_pos),
                           2)

class AnimatedButton(Button):
    """带有动画效果的按钮"""
    
    def __init__(self, x, y, width, height, text="", callback=None,
                 bg_color=PVZ_GREEN, hover_color=None, border_color=PVZ_DARK_GREEN,
                 text_color=WHITE, font_size="medium", border_radius=10, border_width=3,
                 sound="menu_click", animation_speed=0.05):
        """初始化动画按钮"""
        super().__init__(x, y, width, height, text, callback,
                       bg_color, hover_color, border_color,
                       text_color, font_size, border_radius, border_width, sound)
        
        # 动画参数
        self.animation_offset = 0
        self.animation_speed = animation_speed
    
    def update(self, delta_time):
        """更新按钮动画"""
        self.animation_offset = (self.animation_offset + self.animation_speed) % (math.pi * 2)
    
    def render(self, surface):
        """渲染带有动画效果的按钮"""
        # 计算动画偏移量
        y_offset = int(math.sin(self.animation_offset) * 3)
        
        # 临时调整按钮位置
        original_pos = self.rect.topleft
        self.rect.y += y_offset
        
        # 绘制基础按钮
        super().render(surface)
        
        # 恢复原位置
        self.rect.topleft = original_pos

class IconButton(Button):
    """带有图标的按钮"""
    
    def __init__(self, x, y, width, height, icon_name=None, text="", callback=None,
                 bg_color=PVZ_GREEN, hover_color=None, border_color=PVZ_DARK_GREEN,
                 text_color=WHITE, font_size="medium", border_radius=10, border_width=3,
                 sound="menu_click"):
        """初始化图标按钮"""
        super().__init__(x, y, width, height, text, callback,
                       bg_color, hover_color, border_color,
                       text_color, font_size, border_radius, border_width, sound)
        
        # 图标参数
        self.icon_name = icon_name
        self.icon = None
    
    def render(self, surface):
        """渲染带有图标的按钮"""
        # 绘制基础按钮
        super().render(surface)
        
        # 如果有图标并且UI管理器存在，加载并绘制图标
        if self.icon_name and self.ui_manager:
            if not self.icon:
                self.icon = self.ui_manager.resource_loader.load_image(self.icon_name)
            
            if self.icon:
                # 计算图标位置
                if self.text:
                    # 如果有文本，将图标放在文本左侧
                    icon_rect = self.icon.get_rect(
                        midright=(self.rect.centerx - 10, self.rect.centery)
                    )
                else:
                    # 如果没有文本，将图标放在中央
                    icon_rect = self.icon.get_rect(center=self.rect.center)
                
                surface.blit(self.icon, icon_rect) 