"""
菜单场景
作为游戏的开始界面
"""

import pygame
import random
import math
from scenes.base_scene import Scene
from config import (
    WINDOW_WIDTH, WINDOW_HEIGHT, PVZ_GREEN, PVZ_DARK_GREEN, 
    PVZ_LIGHT_GREEN, PVZ_BROWN, PVZ_SKY_BLUE, PVZ_SUN_YELLOW, WHITE
)
from ui.buttons import Button, WoodButton, AnimatedButton

class MenuScene(Scene):
    """
    菜单场景类
    实现游戏的开始界面
    """
    
    def __init__(self, game_engine):
        """初始化菜单场景"""
        super().__init__(game_engine)
        
        # 动画计时器
        self.animation_time = 0
        
        # 阳光装饰
        self.suns = []
        for _ in range(8):
            self.suns.append({
                'x': random.randint(50, WINDOW_WIDTH - 50),
                'y': random.randint(50, WINDOW_HEIGHT - 50),
                'radius': random.randint(15, 25),
                'phase': random.random() * 6.28  # 随机初相位
            })
        
        # 闪烁效果计时器
        self.blink_timer = 0
        self.show_blink = True
        
        # 版本信息
        self.version = "v2.0 PvZ风格"
    
    def enter(self, **kwargs):
        """进入菜单场景"""
        # 设置UI管理器的活动按钮组为主菜单
        self.ui_manager.set_active_group("main_menu")
        
        # 加载并播放背景音乐
        # 注意: 目前可能没有音乐文件，所以这里只是尝试加载
        try:
            if self.resource_loader.load_music(self.game_engine.settings.get("background_music", "simple_background.wav")):
                self.resource_loader.play_music()
        except:
            print("无法加载背景音乐")
    
    def exit(self):
        """退出菜单场景"""
        pass
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            # 键盘事件
            if event.key == pygame.K_RETURN:
                # 回车键开始游戏
                self.game_engine.change_scene('game')
                return True
        
        # 其他事件由UI管理器处理
        return False
    
    def update(self, delta_time):
        """更新菜单场景"""
        # 更新动画时间
        self.animation_time += delta_time
        
        # 更新闪烁效果
        self.blink_timer += delta_time
        if self.blink_timer >= 0.5:  # 每0.5秒闪烁一次
            self.blink_timer = 0
            self.show_blink = not self.show_blink
    
    def render(self, surface):
        """渲染菜单场景"""
        # 绘制背景
        self._draw_background(surface)
        
        # 绘制标题
        self._draw_title(surface)
        
        # 绘制游戏说明
        self._draw_instructions(surface)
        
        # 绘制版本信息
        version_text = self.font_manager.render_text(
            f"版本: {self.version}", 
            self.font_manager.small_font, 
            (150, 150, 150)
        )
        version_rect = version_text.get_rect(bottomright=(WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10))
        surface.blit(version_text, version_rect)
    
    def _draw_background(self, surface):
        """绘制菜单背景"""
        # 绘制天空背景
        surface.fill(PVZ_SKY_BLUE)
        
        # 绘制草坪
        for y in range(0, WINDOW_HEIGHT, 30):
            for x in range(0, WINDOW_WIDTH, 30):
                # 棋盘格草地样式
                if (x // 30 + y // 30) % 2 == 0:
                    color = PVZ_GREEN
                else:
                    color = PVZ_LIGHT_GREEN
                
                pygame.draw.rect(surface, color, pygame.Rect(x, y, 30, 30))
                
                # 添加草地纹理细节 - 小草点缀
                if random.random() < 0.05:  # 随机在部分格子上绘制小草
                    grass_height = random.randint(2, 5)
                    grass_width = 2
                    grass_x = x + random.randint(5, 25)
                    grass_y = y + 30 - grass_height
                    pygame.draw.rect(surface, PVZ_DARK_GREEN, pygame.Rect(
                        grass_x, grass_y, grass_width, grass_height
                    ))
        
        # 绘制阳光装饰
        for sun in self.suns:
            # 添加浮动效果
            y_offset = math.sin(self.animation_time * 2 + sun['phase']) * 5
            sun_y = sun['y'] + y_offset
            
            # 绘制PvZ风格的阳光
            radius = sun['radius']
            
            # 外部发光效果
            for i in range(3):
                glow_radius = radius + (3-i)*2
                glow_alpha = 100 - i*30
                glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (255, 255, 0, glow_alpha), 
                                (glow_radius, glow_radius), glow_radius)
                surface.blit(glow_surface, 
                          (sun['x'] - glow_radius, sun_y - glow_radius))
            
            # 主体阳光
            pygame.draw.circle(surface, PVZ_SUN_YELLOW, (sun['x'], sun_y), radius)
            
            # 添加阳光光芒细节
            ray_length = radius + 4
            for angle in range(0, 360, 45):
                rad_angle = math.radians(angle)
                end_x = sun['x'] + math.cos(rad_angle) * ray_length
                end_y = sun_y + math.sin(rad_angle) * ray_length
                pygame.draw.line(surface, PVZ_SUN_YELLOW, (sun['x'], sun_y), 
                              (end_x, end_y), 2)
    
    def _draw_title(self, surface):
        """绘制菜单标题"""
        # 标题背景
        title_bg_width = 600
        title_bg_height = 120
        title_bg_rect = pygame.Rect(
            (WINDOW_WIDTH - title_bg_width) // 2,
            WINDOW_HEIGHT // 4 - 30,
            title_bg_width,
            title_bg_height
        )
        
        # 绘制木质标志牌风格的背景
        pygame.draw.rect(surface, PVZ_BROWN, title_bg_rect, border_radius=15)
        pygame.draw.rect(surface, (101, 67, 33), title_bg_rect, 4, border_radius=15)
        
        # 添加木纹细节
        for i in range(4):
            wood_line_y = title_bg_rect.top + 20 + i * 25
            pygame.draw.line(surface, (101, 67, 33), 
                          (title_bg_rect.left + 10, wood_line_y),
                          (title_bg_rect.right - 10, wood_line_y),
                          2)
        
        # 绘制游戏标题
        title_text = self.font_manager.render_text(
            "植物大战僵尸风格", 
            self.font_manager.large_font, 
            WHITE
        )
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4 - 10))
        surface.blit(title_text, title_rect)
        
        subtitle_text = self.font_manager.render_text(
            "贪吃蛇游戏", 
            self.font_manager.large_font, 
            WHITE
        )
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4 + 50))
        surface.blit(subtitle_text, subtitle_rect)
        
        # 绘制操作说明
        instructions_bg = pygame.Rect(
            (WINDOW_WIDTH - 500) // 2,
            WINDOW_HEIGHT // 2 - 50,
            500,
            200
        )
        pygame.draw.rect(surface, (0, 0, 0, 160), instructions_bg, border_radius=15)
        pygame.draw.rect(surface, PVZ_DARK_GREEN, instructions_bg, 3, border_radius=15)
        
        instructions = [
            "游戏说明:",
            "用方向键控制豌豆射手移动",
            "收集阳光可以得分并变长",
            "撞到自己或僵尸会导致游戏结束",
            "不同的植物食物有不同的效果",
            "按回车键开始游戏",
            "按ESC键退出游戏"
        ]
        
        for i, instruction in enumerate(instructions):
            if i == 0:  # 标题使用较大字体
                instruction_text = self.font_manager.render_text(
                    instruction, 
                    self.font_manager.medium_font, 
                    PVZ_LIGHT_GREEN
                )
            else:
                instruction_text = self.font_manager.render_text(
                    instruction, 
                    self.font_manager.small_font, 
                    WHITE
                )
            instruction_rect = instruction_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30 + i * 30)
            )
            surface.blit(instruction_text, instruction_rect)
    
    def _draw_instructions(self, surface):
        """绘制游戏说明"""
        # 游戏说明背景
        instructions_bg = pygame.Rect(
            (WINDOW_WIDTH - 500) // 2,
            WINDOW_HEIGHT // 2 - 50,
            500,
            200
        )
        pygame.draw.rect(surface, (0, 0, 0, 160), instructions_bg, border_radius=15)
        pygame.draw.rect(surface, PVZ_DARK_GREEN, instructions_bg, 3, border_radius=15)
        
        instructions = [
            "游戏说明:",
            "用方向键控制豌豆射手移动",
            "收集阳光可以得分并变长",
            "撞到自己或僵尸会导致游戏结束",
            "不同的植物食物有不同的效果",
            "按回车键开始游戏",
            "按ESC键退出游戏"
        ]
        
        for i, instruction in enumerate(instructions):
            if i == 0:  # 标题使用较大字体
                instruction_text = self.font_manager.render_text(
                    instruction, 
                    self.font_manager.medium_font, 
                    PVZ_LIGHT_GREEN
                )
            else:
                instruction_text = self.font_manager.render_text(
                    instruction, 
                    self.font_manager.small_font, 
                    WHITE
                )
            instruction_rect = instruction_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30 + i * 30)
            )
            surface.blit(instruction_text, instruction_rect) 