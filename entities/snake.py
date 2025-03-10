"""
蛇实体
定义蛇的行为和渲染
"""

import pygame
import math
from config import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, 
    UP, DOWN, LEFT, RIGHT,
    PVZ_GREEN, PVZ_DARK_GREEN, WHITE
)

class Snake:
    """
    蛇类
    控制蛇的移动、生长和渲染
    """
    
    def __init__(self, game_engine):
        """
        初始化蛇
        
        参数:
            game_engine: 游戏引擎实例
        """
        self.game_engine = game_engine
        self.resource_loader = game_engine.resource_loader
        self.use_images = game_engine.settings.get("use_images", True)
        
        # 蛇的身体部分
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # 初始位置在中心
        self.direction = RIGHT  # 初始方向向右
        self.next_direction = RIGHT  # 下一步的方向
        self.growth_pending = 0  # 待增长的长度
        
        # 特殊能力
        self.shield_active = False  # 护盾是否激活
        self.shield_timer = 0  # 护盾持续时间
        self.speed_boost_active = False  # 速度提升是否激活
        self.speed_boost_timer = 0  # 速度提升持续时间
        self.speed_multiplier = 1.0  # 速度倍数
        
        # 动画参数
        self.animation_time = 0  # 动画计时器
        
        # 图像资源
        self.head_image = None
        self.body_image = None
        self.tail_image = None
        self.turn_image = None
        self.shield_effect_image = None
        self.speed_effect_image = None
        
        # 加载图像
        self._load_images()
    
    def _load_images(self):
        """加载蛇的图像资源"""
        if self.use_images and self.resource_loader:
            self.head_image = self.resource_loader.load_image("snake_head")
            self.body_image = self.resource_loader.load_image("snake_body")
            self.tail_image = self.resource_loader.load_image("snake_tail")
            self.turn_image = self.resource_loader.load_image("snake_turn")
            self.shield_effect_image = self.resource_loader.load_image("shield_effect")
            self.speed_effect_image = self.resource_loader.load_image("speed_effect")
    
    def reset(self):
        """重置蛇到初始状态"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.growth_pending = 0
        self.shield_active = False
        self.shield_timer = 0
        self.speed_boost_active = False
        self.speed_boost_timer = 0
        self.speed_multiplier = 1.0
    
    def set_direction(self, direction):
        """
        设置蛇的移动方向
        
        参数:
            direction: 方向元组 (dx, dy)
        """
        # 防止180度转弯
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def grow(self, amount=1):
        """
        增加蛇的长度
        
        参数:
            amount: 增加的长度
        """
        self.growth_pending += amount
    
    def move(self):
        """
        移动蛇
        
        返回:
            bool: 如果发生碰撞返回True，否则返回False
        """
        # 更新方向
        self.direction = self.next_direction
        
        # 获取头部位置
        head_x, head_y = self.positions[0]
        
        # 计算新的头部位置
        new_head = (
            (head_x + self.direction[0]) % GRID_WIDTH,
            (head_y + self.direction[1]) % GRID_HEIGHT
        )
        
        # 检查是否碰到自己
        if len(self.positions) > 1 and new_head in self.positions:
            return True  # 碰撞
        
        # 添加新的头部
        self.positions.insert(0, new_head)
        
        # 如果有待增长的长度，减少一个单位
        if self.growth_pending > 0:
            self.growth_pending -= 1
        else:
            # 否则移除尾部
            self.positions.pop()
        
        # 更新特殊能力计时器
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
        
        if self.speed_boost_active:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost_active = False
                self.speed_multiplier = 1.0
        
        return False  # 没有碰撞
    
    def activate_shield(self, duration=100):
        """
        激活护盾能力
        
        参数:
            duration: 护盾持续时间（帧数）
        """
        self.shield_active = True
        self.shield_timer = duration
    
    def activate_speed_boost(self, duration=150, multiplier=1.5):
        """
        激活速度提升能力
        
        参数:
            duration: 速度提升持续时间（帧数）
            multiplier: 速度倍数
        """
        self.speed_boost_active = True
        self.speed_boost_timer = duration
        self.speed_multiplier = multiplier
    
    def get_speed(self):
        """
        获取当前速度倍数
        
        返回:
            float: 速度倍数
        """
        return self.speed_multiplier
    
    def update(self, delta_time):
        """
        更新蛇的状态
        
        参数:
            delta_time: 时间增量
        """
        self.animation_time += delta_time
    
    def draw(self, surface):
        """
        在屏幕上绘制蛇
        
        参数:
            surface: 渲染目标表面
        """
        if self.use_images and self.head_image and self.body_image and self.tail_image:
            self._draw_with_images(surface)
        else:
            self._draw_with_shapes(surface)
    
    def _draw_with_images(self, surface):
        """
        使用图像绘制蛇
        
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
            
            # 确定使用哪个图像
            if i == 0:  # 蛇头
                image = self.head_image
                # 根据方向旋转图像
                if self.direction == UP:
                    angle = 0
                elif self.direction == RIGHT:
                    angle = 90
                elif self.direction == DOWN:
                    angle = 180
                elif self.direction == LEFT:
                    angle = 270
                
                rotated_image = pygame.transform.rotate(image, angle)
                image_rect = rotated_image.get_rect(center=rect.center)
                surface.blit(rotated_image, image_rect)
                
                # 如果有护盾，绘制护盾效果
                if self.shield_active and self.shield_effect_image:
                    shield_rect = self.shield_effect_image.get_rect(center=rect.center)
                    surface.blit(self.shield_effect_image, shield_rect)
                
                # 如果有速度提升，绘制速度效果
                if self.speed_boost_active and self.speed_effect_image:
                    speed_rect = self.speed_effect_image.get_rect(center=rect.center)
                    surface.blit(self.speed_effect_image, speed_rect)
                
            elif i == len(self.positions) - 1:  # 蛇尾
                image = self.tail_image
                # 计算尾部方向
                prev_pos = self.positions[i-1]
                tail_dir = (
                    position[0] - prev_pos[0],
                    position[1] - prev_pos[1]
                )
                # 处理环绕情况
                if tail_dir[0] > 1: tail_dir = (-1, 0)
                if tail_dir[0] < -1: tail_dir = (1, 0)
                if tail_dir[1] > 1: tail_dir = (0, -1)
                if tail_dir[1] < -1: tail_dir = (0, 1)
                
                # 根据方向旋转图像
                if tail_dir == UP:
                    angle = 180
                elif tail_dir == RIGHT:
                    angle = 270
                elif tail_dir == DOWN:
                    angle = 0
                elif tail_dir == LEFT:
                    angle = 90
                
                rotated_image = pygame.transform.rotate(image, angle)
                image_rect = rotated_image.get_rect(center=rect.center)
                surface.blit(rotated_image, image_rect)
                
            else:  # 蛇身
                # 检查是否是转弯部分
                prev_pos = self.positions[i-1]
                next_pos = self.positions[i+1]
                
                # 计算前后方向
                dir_from_prev = (
                    position[0] - prev_pos[0],
                    position[1] - prev_pos[1]
                )
                dir_to_next = (
                    next_pos[0] - position[0],
                    next_pos[1] - position[1]
                )
                
                # 处理环绕情况
                if dir_from_prev[0] > 1: dir_from_prev = (-1, 0)
                if dir_from_prev[0] < -1: dir_from_prev = (1, 0)
                if dir_from_prev[1] > 1: dir_from_prev = (0, -1)
                if dir_from_prev[1] < -1: dir_from_prev = (0, 1)
                
                if dir_to_next[0] > 1: dir_to_next = (-1, 0)
                if dir_to_next[0] < -1: dir_to_next = (1, 0)
                if dir_to_next[1] > 1: dir_to_next = (0, -1)
                if dir_to_next[1] < -1: dir_to_next = (0, 1)
                
                # 检查是否是转弯
                is_turn = dir_from_prev != dir_to_next and dir_from_prev != (-dir_to_next[0], -dir_to_next[1])
                
                if is_turn and self.turn_image:
                    image = self.turn_image
                    # 确定转弯类型和角度
                    if (dir_from_prev == RIGHT and dir_to_next == UP) or (dir_from_prev == DOWN and dir_to_next == LEFT):
                        angle = 0
                    elif (dir_from_prev == UP and dir_to_next == RIGHT) or (dir_from_prev == LEFT and dir_to_next == DOWN):
                        angle = 90
                    elif (dir_from_prev == LEFT and dir_to_next == UP) or (dir_from_prev == DOWN and dir_to_next == RIGHT):
                        angle = 270
                    else:
                        angle = 180
                    
                    rotated_image = pygame.transform.rotate(image, angle)
                    image_rect = rotated_image.get_rect(center=rect.center)
                    surface.blit(rotated_image, image_rect)
                else:
                    image = self.body_image
                    # 确定身体部分的方向
                    if dir_from_prev[0] != 0:  # 水平方向
                        angle = 90
                    else:  # 垂直方向
                        angle = 0
                    
                    rotated_image = pygame.transform.rotate(image, angle)
                    image_rect = rotated_image.get_rect(center=rect.center)
                    surface.blit(rotated_image, image_rect)
    
    def _draw_with_shapes(self, surface):
        """
        使用基本图形绘制蛇
        
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
                if self.shield_active:
                    shield_radius = head_radius + 4
                    shield_color = (100, 200, 255, 150)  # 半透明蓝色
                    shield_surface = pygame.Surface((shield_radius*2, shield_radius*2), pygame.SRCALPHA)
                    pygame.draw.circle(shield_surface, shield_color, (shield_radius, shield_radius), shield_radius)
                    surface.blit(shield_surface, (center_x - shield_radius, center_y - shield_radius))
                
                # 如果有速度提升，绘制速度效果
                if self.speed_boost_active:
                    speed_radius = head_radius + 6
                    speed_color = (255, 200, 0, 100)  # 半透明黄色
                    speed_surface = pygame.Surface((speed_radius*2, speed_radius*2), pygame.SRCALPHA)
                    
                    # 绘制速度线条
                    for angle in range(0, 360, 45):
                        rad_angle = math.radians(angle)
                        start_x = speed_radius + math.cos(rad_angle) * (head_radius + 2)
                        start_y = speed_radius + math.sin(rad_angle) * (head_radius + 2)
                        end_x = speed_radius + math.cos(rad_angle) * speed_radius
                        end_y = speed_radius + math.sin(rad_angle) * speed_radius
                        pygame.draw.line(speed_surface, speed_color, (start_x, start_y), (end_x, end_y), 2)
                    
                    surface.blit(speed_surface, (center_x - speed_radius, center_y - speed_radius))
                
                # 绘制头部
                pygame.draw.circle(surface, PVZ_GREEN, (center_x, center_y), head_radius)
                pygame.draw.circle(surface, PVZ_DARK_GREEN, (center_x, center_y), head_radius, 2)
                
                # 绘制眼睛
                eye_offset_x = 4 * (1 if self.direction[0] >= 0 else -1)
                eye_offset_y = 4 * (1 if self.direction[1] >= 0 else -1)
                
                # 如果是水平方向，眼睛在左右
                if self.direction[0] != 0:
                    pygame.draw.circle(surface, WHITE, (center_x + eye_offset_x, center_y - 3), 3)
                    pygame.draw.circle(surface, WHITE, (center_x + eye_offset_x, center_y + 3), 3)
                    pygame.draw.circle(surface, (0, 0, 0), (center_x + eye_offset_x, center_y - 3), 1)
                    pygame.draw.circle(surface, (0, 0, 0), (center_x + eye_offset_x, center_y + 3), 1)
                # 如果是垂直方向，眼睛在上下
                else:
                    pygame.draw.circle(surface, WHITE, (center_x - 3, center_y + eye_offset_y), 3)
                    pygame.draw.circle(surface, WHITE, (center_x + 3, center_y + eye_offset_y), 3)
                    pygame.draw.circle(surface, (0, 0, 0), (center_x - 3, center_y + eye_offset_y), 1)
                    pygame.draw.circle(surface, (0, 0, 0), (center_x + 3, center_y + eye_offset_y), 1)
                
            else:  # 蛇身
                body_radius = radius
                
                # 绘制身体
                pygame.draw.circle(surface, PVZ_GREEN, (center_x, center_y), body_radius)
                pygame.draw.circle(surface, PVZ_DARK_GREEN, (center_x, center_y), body_radius, 1)
                
                # 添加一些细节
                if i % 2 == 0:
                    detail_radius = body_radius // 2
                    pygame.draw.circle(surface, PVZ_DARK_GREEN, (center_x, center_y), detail_radius, 1)
    
    def add_ability(self, ability_name):
        """
        添加特殊能力
        
        参数:
            ability_name: 能力名称，如"shield"或"speed_up"
        """
        if ability_name == "shield":
            self.activate_shield()
            print("激活护盾能力")
        elif ability_name == "speed_up":
            self.activate_speed_boost()
            print("激活速度提升能力")
        else:
            print(f"未知能力: {ability_name}") 