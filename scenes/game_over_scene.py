"""
游戏结束场景
显示游戏结束时的界面
"""

import pygame
import random
import math
from scenes.base_scene import Scene
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, WHITE, 
    PVZ_GREEN, PVZ_DARK_GREEN, PVZ_CHERRY_RED
)
from ui.buttons import Button, WoodButton

class GameOverScene(Scene):
    """
    游戏结束场景类
    显示游戏结束界面、得分和重新开始选项
    """
    
    def __init__(self, game_engine):
        """初始化游戏结束场景"""
        super().__init__(game_engine)
        
        # 分数
        self.score = 0
        
        # 按钮状态
        self.buttons = {
            'restart': {
                'rect': pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 130, 300, 50),
                'text': '重新开始 (回车)',
                'hover': False,
                'active': False
            },
            'quit': {
                'rect': pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 200, 300, 50),
                'text': '退出游戏 (ESC)',
                'hover': False,
                'active': False
            }
        }
        
        # 坟墓动画
        self.animation_time = 0
        self.crack_positions = []
        
    def enter(self, **kwargs):
        """
        进入游戏结束场景
        
        参数:
            score (int): 游戏得分
        """
        self.score = kwargs.get('score', 0)
        
        # 生成坟墓裂纹位置
        self.crack_positions = []
        for _ in range(5):
            self.crack_positions.append({
                'x': random.randint(20, 220),
                'y': random.randint(20, 200),
                'length': random.randint(10, 30),
                'angle': random.randint(0, 360)
            })
        
        # 播放游戏结束音效
        try:
            self.resource_loader.play_sound("game_over")
        except:
            pass
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEMOTION:
            # 鼠标移动，检查按钮悬停状态
            mouse_pos = pygame.mouse.get_pos()
            for button in self.buttons.values():
                button['hover'] = button['rect'].collidepoint(mouse_pos)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 鼠标点击
            mouse_pos = pygame.mouse.get_pos()
            for button_name, button in self.buttons.items():
                if button['rect'].collidepoint(mouse_pos):
                    button['active'] = True
                    
                    # 播放点击音效
                    try:
                        self.resource_loader.play_sound("menu_click")
                    except:
                        pass
        
        elif event.type == pygame.MOUSEBUTTONUP:
            # 鼠标释放
            mouse_pos = pygame.mouse.get_pos()
            for button_name, button in self.buttons.items():
                if button['active'] and button['rect'].collidepoint(mouse_pos):
                    # 执行按钮动作
                    if button_name == 'restart':
                        self.game_engine.change_scene('game')
                    elif button_name == 'quit':
                        self.game_engine.running = False
                
                button['active'] = False
        
        elif event.type == pygame.KEYDOWN:
            # 键盘事件
            if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # 回车键或空格键重新开始游戏
                self.game_engine.change_scene('game')
            elif event.key == pygame.K_ESCAPE:
                # ESC键退出游戏
                self.game_engine.running = False
    
    def update(self, delta_time):
        """更新场景"""
        # 更新动画时间
        self.animation_time += delta_time
    
    def render(self, surface):
        """渲染场景"""
        # 绘制半透明的黑色背景
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        surface.blit(overlay, (0, 0))
        
        # 绘制坟墓和游戏结束文本
        self._draw_grave(surface)
        
        # 绘制按钮
        self._draw_buttons(surface)
    
    def _draw_grave(self, surface):
        """绘制PvZ风格的坟墓"""
        # 坟墓尺寸和位置
        grave_width = 240
        grave_height = 300
        grave_x = (WINDOW_WIDTH - grave_width) // 2
        grave_y = (WINDOW_HEIGHT - grave_height) // 2 - 40
        
        # 绘制坟墓底座
        pygame.draw.rect(surface, (100, 100, 100), 
                      pygame.Rect(grave_x + 20, grave_y + grave_height - 50, grave_width - 40, 50),
                      border_radius=10)
        
        # 绘制坟墓主体
        grave_rect = pygame.Rect(grave_x, grave_y, grave_width, grave_height - 50)
        pygame.draw.rect(surface, (150, 150, 150), grave_rect, border_radius=30)
        pygame.draw.rect(surface, (100, 100, 100), grave_rect, 4, border_radius=30)
        
        # 添加坟墓纹理
        for crack in self.crack_positions:
            crack_x = grave_x + crack['x']
            crack_y = grave_y + crack['y']
            crack_length = crack['length']
            crack_angle = crack['angle']
            end_x = crack_x + math.cos(math.radians(crack_angle)) * crack_length
            end_y = crack_y + math.sin(math.radians(crack_angle)) * crack_length
            pygame.draw.line(surface, (100, 100, 100), (crack_x, crack_y), (end_x, end_y), 2)
        
        # 绘制游戏结束文本
        game_over_text = self.font_manager.render_text(
            "游戏结束!", 
            self.font_manager.large_font, 
            PVZ_CHERRY_RED
        )
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, grave_y + 60))
        surface.blit(game_over_text, game_over_rect)
        
        # 绘制骷髅图标
        skull_radius = 25
        skull_x = WINDOW_WIDTH // 2
        skull_y = grave_y + 120
        
        # 绘制骷髅头
        pygame.draw.circle(surface, WHITE, (skull_x, skull_y), skull_radius)
        
        # 绘制眼睛
        eye_size = 10
        pygame.draw.ellipse(surface, BLACK, 
                        pygame.Rect(skull_x - skull_radius//2 - eye_size//2, 
                                  skull_y - eye_size//2, 
                                  eye_size, eye_size))
        pygame.draw.ellipse(surface, BLACK, 
                        pygame.Rect(skull_x + skull_radius//2 - eye_size//2, 
                                  skull_y - eye_size//2, 
                                  eye_size, eye_size))
        
        # 绘制鼻子
        nose_size = 5
        pygame.draw.ellipse(surface, BLACK, 
                        pygame.Rect(skull_x - nose_size//2, 
                                  skull_y + nose_size, 
                                  nose_size, nose_size))
        
        # 绘制嘴巴
        mouth_width = skull_radius
        for i in range(3):
            pygame.draw.line(surface, BLACK, 
                          (skull_x - mouth_width//2 + i*mouth_width//2, skull_y + skull_radius//2),
                          (skull_x - mouth_width//2 + (i+1)*mouth_width//2, skull_y + skull_radius//2),
                          2)
        
        # 绘制分数文本
        score_text = self.font_manager.render_text(
            f"最终阳光数: {self.score}", 
            self.font_manager.medium_font, 
            WHITE
        )
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, grave_y + 180))
        surface.blit(score_text, score_rect)
    
    def _draw_buttons(self, surface):
        """绘制按钮"""
        for button_name, button in self.buttons.items():
            # 根据按钮状态选择颜色
            if button['active']:
                # 按下状态
                color = (0, 100, 0) if button_name == 'restart' else (100, 0, 0)
                border_color = (0, 60, 0) if button_name == 'restart' else (60, 0, 0)
            elif button['hover']:
                # 悬停状态
                color = (0, 140, 0) if button_name == 'restart' else (140, 0, 0)
                border_color = (0, 100, 0) if button_name == 'restart' else (100, 0, 0)
            else:
                # 正常状态
                color = PVZ_GREEN if button_name == 'restart' else PVZ_CHERRY_RED
                border_color = PVZ_DARK_GREEN if button_name == 'restart' else (150, 0, 0)
            
            # 绘制按钮
            pygame.draw.rect(surface, color, button['rect'], border_radius=10)
            pygame.draw.rect(surface, border_color, button['rect'], 3, border_radius=10)
            
            # 绘制按钮文本
            text = self.font_manager.render_text(
                button['text'], 
                self.font_manager.medium_font, 
                WHITE
            )
            text_rect = text.get_rect(center=button['rect'].center)
            surface.blit(text, text_rect) 