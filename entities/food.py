"""
食物类
包括基础食物和特殊食物
"""

import pygame
import random
import math
from config import (
    GRID_WIDTH, GRID_HEIGHT, GRID_SIZE, FOOD_TYPES,
    PVZ_SUN_YELLOW, PVZ_GREEN, PVZ_LIGHT_GREEN, PVZ_DARK_GREEN
)

class BaseFood:
    """
    基础食物类
    所有食物类的基类
    """
    
    def __init__(self):
        """初始化基础食物"""
        self.position = (0, 0)        # 食物位置
        self.animation_offset = 0      # 动画偏移量
        self.worth = 10                # 食物价值（得分）
        self.effect = None             # 特殊效果
        self.spawn()                   # 生成食物
    
    def spawn(self):
        """随机生成食物位置"""
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
        # 重置动画
        self.animation_offset = random.random() * 6.28  # 随机初相位
    
    def update_animation(self, delta_time):
        """更新动画效果"""
        self.animation_offset = (self.animation_offset + delta_time * 5) % 6.28  # 2π
    
    def apply_effect(self, snake, game_state):
        """
        应用食物效果
        
        参数:
            snake: 蛇对象
            game_state: 游戏状态对象
        """
        # 基础效果：蛇生长，分数增加
        snake.grow()
        game_state.score += self.worth
    
    def draw(self, surface):
        """
        在屏幕上绘制食物
        
        参数:
            surface: 渲染目标表面
        """
        # 计算食物的位置和中心点
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        center_x = rect.centerx
        center_y = rect.centery
        
        # 添加浮动效果
        float_offset = math.sin(self.animation_offset) * 3
        center_y += float_offset
        
        # 绘制PvZ风格的阳光
        radius = GRID_SIZE // 2 - 2
        
        # 外部发光效果
        for i in range(3):
            glow_radius = radius + (3-i)*2
            glow_alpha = 100 - i*30
            glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 255, 0, glow_alpha), 
                             (glow_radius, glow_radius), glow_radius)
            surface.blit(glow_surface, 
                       (center_x - glow_radius, center_y - glow_radius))
        
        # 主体阳光
        pygame.draw.circle(surface, PVZ_SUN_YELLOW, (center_x, center_y), radius)
        
        # 添加阳光光芒细节
        ray_length = radius + 4
        for angle in range(0, 360, 45):
            rad_angle = math.radians(angle)
            end_x = center_x + math.cos(rad_angle) * ray_length
            end_y = center_y + math.sin(rad_angle) * ray_length
            pygame.draw.line(surface, PVZ_SUN_YELLOW, (center_x, center_y), 
                           (end_x, end_y), 2)

class SunflowerFood(BaseFood):
    """
    向日葵食物类
    给予双倍分数
    """
    
    def __init__(self):
        """初始化向日葵食物"""
        super().__init__()
        self.worth = 20
    
    def draw(self, surface):
        """绘制向日葵食物"""
        # 计算食物的位置和中心点
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        center_x = rect.centerx
        center_y = rect.centery
        
        # 添加浮动效果
        float_offset = math.sin(self.animation_offset) * 3
        center_y += float_offset
        
        # 绘制向日葵头部（主体）
        radius = GRID_SIZE // 2 - 2
        pygame.draw.circle(surface, (255, 200, 0), (center_x, center_y), radius)
        
        # 绘制向日葵花瓣
        petal_color = (255, 220, 0)
        for angle in range(0, 360, 30):
            rad_angle = math.radians(angle)
            petal_x = center_x + math.cos(rad_angle) * (radius - 2)
            petal_y = center_y + math.sin(rad_angle) * (radius - 2)
            petal_radius = radius // 2
            pygame.draw.circle(surface, petal_color, (int(petal_x), int(petal_y)), petal_radius)
        
        # 绘制向日葵中心（褐色）
        pygame.draw.circle(surface, (139, 69, 19), (center_x, center_y), radius // 2)

class WalnutFood(BaseFood):
    """
    坚果食物类
    给予临时护盾
    """
    
    def __init__(self):
        """初始化坚果食物"""
        super().__init__()
        self.worth = 5
        self.effect = "shield"
    
    def apply_effect(self, snake, game_state):
        """应用坚果食物效果"""
        super().apply_effect(snake, game_state)
        
        # 添加护盾能力，持续100帧
        snake.add_ability("shield", 100)
    
    def draw(self, surface):
        """绘制坚果食物"""
        # 计算食物的位置和中心点
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        center_x = rect.centerx
        center_y = rect.centery
        
        # 添加浮动效果
        float_offset = math.sin(self.animation_offset) * 2
        center_y += float_offset
        
        # 绘制坚果主体（椭圆形）
        walnut_color = (210, 170, 100)
        walnut_width = int(GRID_SIZE * 0.8)
        walnut_height = int(GRID_SIZE * 0.9)
        walnut_rect = pygame.Rect(
            center_x - walnut_width // 2,
            center_y - walnut_height // 2,
            walnut_width, walnut_height
        )
        pygame.draw.ellipse(surface, walnut_color, walnut_rect)
        pygame.draw.ellipse(surface, (160, 120, 60), walnut_rect, 2)
        
        # 绘制坚果的眼睛
        eye_y = center_y - walnut_height // 6
        left_eye_x = center_x - walnut_width // 4
        right_eye_x = center_x + walnut_width // 4
        
        # 白色部分
        pygame.draw.ellipse(surface, (255, 255, 255), 
                         pygame.Rect(left_eye_x - 3, eye_y - 3, 6, 6))
        pygame.draw.ellipse(surface, (255, 255, 255), 
                         pygame.Rect(right_eye_x - 3, eye_y - 3, 6, 6))
        
        # 黑色瞳孔
        pygame.draw.ellipse(surface, (0, 0, 0), 
                         pygame.Rect(left_eye_x - 1, eye_y - 1, 3, 3))
        pygame.draw.ellipse(surface, (0, 0, 0), 
                         pygame.Rect(right_eye_x - 1, eye_y - 1, 3, 3))

class PeashooterFood(BaseFood):
    """
    豌豆射手食物类
    增加移动速度
    """
    
    def __init__(self):
        """初始化豌豆射手食物"""
        super().__init__()
        self.worth = 15
        self.effect = "speed_up"
    
    def apply_effect(self, snake, game_state):
        """应用豌豆射手食物效果"""
        super().apply_effect(snake, game_state)
        
        # 添加加速能力，持续150帧
        snake.add_ability("speed_up", 150)
    
    def draw(self, surface):
        """绘制豌豆射手食物"""
        # 计算食物的位置和中心点
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        center_x = rect.centerx
        center_y = rect.centery
        
        # 添加浮动效果
        float_offset = math.sin(self.animation_offset) * 3
        center_y += float_offset
        
        # 绘制豌豆射手头部
        radius = GRID_SIZE // 2 - 2
        pygame.draw.circle(surface, PVZ_GREEN, (center_x, center_y), radius)
        pygame.draw.circle(surface, PVZ_DARK_GREEN, (center_x, center_y), radius, 2)
        
        # 绘制眼睛
        pygame.draw.circle(surface, (255, 255, 255), (center_x - 3, center_y - 2), 3)
        pygame.draw.circle(surface, (255, 255, 255), (center_x + 3, center_y - 2), 3)
        pygame.draw.circle(surface, (0, 0, 0), (center_x - 3, center_y - 2), 1)
        pygame.draw.circle(surface, (0, 0, 0), (center_x + 3, center_y - 2), 1)
        
        # 绘制嘴（豌豆发射口）
        pygame.draw.circle(surface, (0, 100, 0), (center_x + radius - 2, center_y), radius // 2)
        pygame.draw.circle(surface, (0, 0, 0), (center_x + radius - 2, center_y), radius // 2, 1)

class FoodManager:
    """
    食物管理器类
    负责生成和管理食物
    """
    
    def __init__(self):
        """初始化食物管理器"""
        self.foods = []
        
        # 食物类型映射
        self.food_types = {
            "sun": {"class": BaseFood, "weight": FOOD_TYPES["sun"]["weight"]},
            "sunflower": {"class": SunflowerFood, "weight": FOOD_TYPES["sunflower"]["weight"]},
            "walnut": {"class": WalnutFood, "weight": FOOD_TYPES["walnut"]["weight"]},
            "peashooter": {"class": PeashooterFood, "weight": 15}
        }
    
    def spawn_food(self, snake_positions=None):
        """
        生成食物
        
        参数:
            snake_positions: 蛇身体位置列表，用于避免食物生成在蛇身上
        
        返回:
            Food: 生成的食物对象
        """
        # 根据权重随机选择食物类型
        weights = [food_info["weight"] for food_info in self.food_types.values()]
        food_type = random.choices(list(self.food_types.keys()), weights=weights)[0]
        
        # 创建对应类型的食物
        food = self.food_types[food_type]["class"]()
        
        # 确保食物不出现在蛇身上
        if snake_positions:
            while food.position in snake_positions:
                food.spawn()
        
        # 清除之前的食物
        self.foods.clear()
        
        # 添加新食物
        self.foods.append(food)
        
        return food
    
    def update(self, delta_time):
        """
        更新所有食物
        
        参数:
            delta_time: 时间增量（秒）
        """
        for food in self.foods:
            food.update_animation(delta_time)
    
    def check_collision(self, snake, game_state):
        """
        检查蛇是否碰到食物
        
        参数:
            snake: 蛇对象
            game_state: 游戏状态对象
        
        返回:
            bool: 是否有碰撞发生
        """
        head_position = snake.get_head_position()
        for food in list(self.foods):
            if head_position == food.position:
                # 应用食物效果
                food.apply_effect(snake, game_state)
                
                # 播放吃食物音效
                try:
                    game_state.resource_loader.play_sound("eat_food")
                except:
                    pass
                
                # 移除被吃掉的食物
                self.foods.remove(food)
                
                # 生成新食物
                self.spawn_food(snake.positions)
                
                return True
        
        return False
    
    def draw(self, surface):
        """
        绘制所有食物
        
        参数:
            surface: 渲染目标表面
        """
        for food in self.foods:
            food.draw(surface) 