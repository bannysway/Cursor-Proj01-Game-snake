"""
蛇实体类
负责蛇的移动、生长和绘制
"""

import pygame
import math
from config import (
    GRID_WIDTH, GRID_HEIGHT, GRID_SIZE, 
    UP, DOWN, LEFT, RIGHT,
    PVZ_GREEN, PVZ_LIGHT_GREEN, PVZ_DARK_GREEN, WHITE, BLACK
)

class Snake:
    """
    蛇实体类
    负责蛇的移动、生长、碰撞检测和绘制
    """
    
    def __init__(self):
        """初始化蛇"""
        # 蛇的位置，初始在屏幕中央
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        
        # 方向和移动
        self.direction = RIGHT        # 当前方向
        self.next_direction = RIGHT   # 下一步的方向
        self.grew = False             # 是否刚吃了食物需要生长
        
        # 动画
        self.animation_offset = 0.0   # 动画偏移量，用于制作摆动效果
        
        # 特殊能力
        self.abilities = {}           # 特殊能力 {ability_name: duration}
        self.invincible = False       # 是否无敌（不会碰撞死亡）
        self.speed_multiplier = 1.0   # 速度倍率
        self.is_shield_active = False # 是否有护盾
    
    def get_head_position(self):
        """
        获取蛇头位置
        
        返回:
            tuple: 蛇头坐标 (x, y)
        """
        return self.positions[0]
    
    def update_direction(self, direction):
        """
        更新蛇的移动方向
        不能直接向相反方向移动，例如向右移动时不能直接向左移动
        
        参数:
            direction (tuple): 新方向
        """
        # 检查是否是相反方向
        opposite_direction = (direction[0] * -1, direction[1] * -1)
        if opposite_direction != self.direction:
            self.next_direction = direction
    
    def move(self):
        """
        移动蛇
        
        返回:
            bool: 如果游戏结束则返回True，否则返回False
        """
        # 更新当前方向
        self.direction = self.next_direction
        
        # 获取蛇头位置
        head = self.get_head_position()
        
        # 计算新的蛇头位置
        new_head = (
            (head[0] + self.direction[0]) % GRID_WIDTH,  # 如果超出边界则从另一侧出现
            (head[1] + self.direction[1]) % GRID_HEIGHT
        )
        
        # 检查是否碰到自己
        if new_head in self.positions[1:] and not self.invincible:
            return True  # 游戏结束
        
        # 更新蛇的位置
        self.positions.insert(0, new_head)  # 在列表头部添加新的蛇头
        
        # 如果没有吃到食物，则移除蛇尾；否则保留蛇尾（蛇长度+1）
        if not self.grew:
            self.positions.pop()  # 移除蛇尾
        else:
            self.grew = False  # 重置生长标志
        
        # 更新动画偏移量
        self.animation_offset = (self.animation_offset + 0.2) % 6.28  # 2π
        
        # 更新特殊能力状态
        self.update_abilities()
        
        return False  # 游戏继续
    
    def grow(self):
        """蛇吃到食物后生长"""
        self.grew = True
    
    def add_ability(self, ability_name, duration):
        """
        添加特殊能力
        
        参数:
            ability_name (str): 能力名称
            duration (int): 持续时间（帧数）
        """
        # 更新或添加能力
        self.abilities[ability_name] = duration
        
        # 根据能力类型应用效果
        if ability_name == "shield":
            self.invincible = True
            self.is_shield_active = True
        elif ability_name == "speed_up":
            self.speed_multiplier = 1.5
    
    def update_abilities(self):
        """更新特殊能力状态"""
        # 需要移除的能力
        expired_abilities = []
        
        # 更新所有能力的持续时间
        for ability, duration in self.abilities.items():
            # 减少持续时间
            self.abilities[ability] = duration - 1
            
            # 检查能力是否已过期
            if self.abilities[ability] <= 0:
                expired_abilities.append(ability)
        
        # 移除过期的能力
        for ability in expired_abilities:
            if ability == "shield":
                self.invincible = False
                self.is_shield_active = False
            elif ability == "speed_up":
                self.speed_multiplier = 1.0
            
            del self.abilities[ability]
    
    def get_speed(self):
        """
        获取当前移动速度
        
        返回:
            float: 速度倍率
        """
        return self.speed_multiplier
    
    def is_invincible(self):
        """
        检查是否处于无敌状态
        
        返回:
            bool: 是否无敌
        """
        return self.invincible
    
    def draw(self, surface):
        """
        在屏幕上绘制蛇 - 采用PvZ豌豆射手风格
        
        参数:
            surface: 渲染目标表面
        """
        for i, position in enumerate(self.positions):
            # 计算蛇身体每一节的矩形位置
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            
            # 绘制圆形豌豆身体
            center_x = rect.centerx
            center_y = rect.centery
            radius = GRID_SIZE // 2 - 2
            
            if i == 0:  # 蛇头 - 豌豆射手头部
                # 头部稍大
                head_radius = radius + 2
                
                # 如果有护盾，绘制护盾效果
                if self.is_shield_active:
                    shield_radius = head_radius + 4
                    shield_color = (100, 200, 255, 150)  # 半透明蓝色
                    shield_surface = pygame.Surface((shield_radius*2, shield_radius*2), pygame.SRCALPHA)
                    pygame.draw.circle(shield_surface, shield_color, (shield_radius, shield_radius), shield_radius)
                    surface.blit(shield_surface, (center_x - shield_radius, center_y - shield_radius))
                
                # 绘制头部
                pygame.draw.circle(surface, PVZ_GREEN, (center_x, center_y), head_radius)
                pygame.draw.circle(surface, PVZ_DARK_GREEN, (center_x, center_y), head_radius, 2)
                
                # 绘制眼睛
                eye_offset_x = 4 * (1 if self.direction[0] >= 0 else -1)
                eye_offset_y = 4 * (1 if self.direction[1] >= 0 else -1)
                
                # 如果是横向移动，眼睛在水平方向上偏移
                if self.direction[0] != 0:
                    pygame.draw.circle(surface, WHITE, 
                                    (center_x + eye_offset_x, center_y - 3), 4)
                    pygame.draw.circle(surface, WHITE, 
                                    (center_x + eye_offset_x, center_y + 3), 4)
                    pygame.draw.circle(surface, BLACK, 
                                    (center_x + eye_offset_x + 1, center_y - 3), 2)
                    pygame.draw.circle(surface, BLACK, 
                                    (center_x + eye_offset_x + 1, center_y + 3), 2)
                # 如果是纵向移动，眼睛在垂直方向上偏移
                else:
                    pygame.draw.circle(surface, WHITE, 
                                    (center_x - 3, center_y + eye_offset_y), 4)
                    pygame.draw.circle(surface, WHITE, 
                                    (center_x + 3, center_y + eye_offset_y), 4)
                    pygame.draw.circle(surface, BLACK, 
                                    (center_x - 3, center_y + eye_offset_y + 1), 2)
                    pygame.draw.circle(surface, BLACK, 
                                    (center_x + 3, center_y + eye_offset_y + 1), 2)
            else:  # 蛇身 - 豌豆串成的身体
                # 根据位置添加轻微的波动效果
                wave_offset = math.sin(self.animation_offset + i * 0.5) * 2
                body_center_y = center_y + wave_offset
                
                # 绘制稍小的圆形身体
                body_radius = radius - 1
                
                # 绘制豌豆身体
                pygame.draw.circle(surface, PVZ_LIGHT_GREEN, (center_x, body_center_y), body_radius)
                pygame.draw.circle(surface, PVZ_GREEN, (center_x, body_center_y), body_radius, 1)
                
                # 添加叶子细节
                if i % 3 == 0:  # 每隔几节添加一片叶子
                    leaf_size = 4
                    leaf_x = center_x + (radius - 2)
                    leaf_y = body_center_y - (radius - 2)
                    pygame.draw.ellipse(surface, PVZ_DARK_GREEN, 
                                     pygame.Rect(leaf_x, leaf_y, leaf_size*2, leaf_size)) 