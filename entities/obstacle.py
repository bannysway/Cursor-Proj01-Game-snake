"""
障碍物类
包括静态和移动的障碍物
"""

import pygame
import random
import math
from config import (
    GRID_WIDTH, GRID_HEIGHT, GRID_SIZE, OBSTACLE_TYPES
)

class BaseObstacle:
    """
    基础障碍物类
    所有障碍物的基类
    """
    
    def __init__(self, position=None):
        """
        初始化障碍物
        
        参数:
            position (tuple): 障碍物初始位置，如果为None则随机生成
        """
        self.position = position or self.generate_position()
        self.damage = 1  # 障碍物造成的伤害
        self.is_static = True  # 是否静态障碍物
        self.animation_time = 0  # 动画计时器
    
    def generate_position(self):
        """
        生成随机位置
        
        返回:
            tuple: 位置坐标 (x, y)
        """
        # 避免在中央区域生成，给玩家留出初始空间
        center_x, center_y = GRID_WIDTH // 2, GRID_HEIGHT // 2
        safe_radius = 5  # 中央安全区域半径
        
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            # 检查是否在安全区域内
            distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)
            if distance > safe_radius:
                return (x, y)
    
    def update(self, delta_time):
        """
        更新障碍物状态
        
        参数:
            delta_time: 时间增量（秒）
        """
        self.animation_time += delta_time
    
    def check_collision(self, snake):
        """
        检查是否与蛇发生碰撞
        
        参数:
            snake: 蛇对象
        
        返回:
            bool: 是否碰撞
        """
        # 检查蛇头是否与障碍物碰撞
        if snake.get_head_position() == self.position:
            # 如果蛇不是无敌状态，则判定为碰撞
            if not snake.is_invincible():
                return True
        
        return False
    
    def draw(self, surface):
        """
        绘制障碍物
        
        参数:
            surface: 渲染目标表面
        """
        pass

class TombstoneObstacle(BaseObstacle):
    """
    坟墓障碍物类
    静态障碍物
    """
    
    def __init__(self, position=None):
        """初始化坟墓障碍物"""
        super().__init__(position)
        self.is_static = True
        self.tombstone_color = (150, 150, 150)
        self.border_color = (100, 100, 100)
    
    def draw(self, surface):
        """绘制坟墓障碍物"""
        # 计算障碍物位置
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        
        # 绘制坟墓
        # 底部（略大一些）
        base_height = GRID_SIZE // 3
        base_rect = pygame.Rect(
            rect.left + GRID_SIZE // 10,
            rect.bottom - base_height,
            rect.width - GRID_SIZE // 5,
            base_height
        )
        pygame.draw.rect(surface, self.tombstone_color, base_rect)
        pygame.draw.rect(surface, self.border_color, base_rect, 1)
        
        # 主体（上部分）
        top_width = int(rect.width * 0.7)
        top_height = int(rect.height * 0.8)
        top_rect = pygame.Rect(
            rect.centerx - top_width // 2,
            rect.top + GRID_SIZE // 10,
            top_width,
            top_height
        )
        pygame.draw.rect(surface, self.tombstone_color, top_rect, border_radius=5)
        pygame.draw.rect(surface, self.border_color, top_rect, 1, border_radius=5)
        
        # 添加裂纹装饰
        for _ in range(2):
            start_x = random.randint(int(top_rect.left + 2), int(top_rect.right - 2))
            start_y = random.randint(int(top_rect.top + 2), int(top_rect.bottom - 2))
            length = random.randint(3, 8)
            angle = random.randint(0, 360)
            end_x = start_x + math.cos(math.radians(angle)) * length
            end_y = start_y + math.sin(math.radians(angle)) * length
            pygame.draw.line(surface, self.border_color, (start_x, start_y), (end_x, end_y), 1)

class ZombieObstacle(BaseObstacle):
    """
    僵尸障碍物类
    缓慢移动的障碍物
    """
    
    def __init__(self, position=None):
        """初始化僵尸障碍物"""
        super().__init__(position)
        self.is_static = False
        self.speed = OBSTACLE_TYPES["zombie"]["speed"]
        self.damage = OBSTACLE_TYPES["zombie"]["damage"]
        self.direction = self._choose_direction()
        self.position = list(self.position)  # 转换为列表以支持浮点位置
        
        # 僵尸外观颜色
        self.zombie_colors = {
            'body': (100, 140, 100),  # 僵尸身体颜色（灰绿色）
            'head': (150, 170, 150),  # 僵尸头部颜色
            'eyes': (255, 0, 0),      # 僵尸眼睛颜色（红色）
            'detail': (70, 90, 70)    # 细节颜色
        }
        
        # 头部摆动状态
        self.head_tilt = 0
    
    def _choose_direction(self):
        """
        选择随机移动方向
        
        返回:
            tuple: 方向向量 (dx, dy)
        """
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        return random.choice(directions)
    
    def update(self, delta_time):
        """更新僵尸位置和动画"""
        super().update(delta_time)
        
        # 移动僵尸
        self.position[0] += self.direction[0] * self.speed * delta_time
        self.position[1] += self.direction[1] * self.speed * delta_time
        
        # 检查边界，如果碰到边界则反向移动
        if self.position[0] < 0:
            self.position[0] = 0
            self.direction = (-self.direction[0], self.direction[1])
        elif self.position[0] >= GRID_WIDTH:
            self.position[0] = GRID_WIDTH - 0.01
            self.direction = (-self.direction[0], self.direction[1])
            
        if self.position[1] < 0:
            self.position[1] = 0
            self.direction = (self.direction[0], -self.direction[1])
        elif self.position[1] >= GRID_HEIGHT:
            self.position[1] = GRID_HEIGHT - 0.01
            self.direction = (self.direction[0], -self.direction[1])
        
        # 更新头部摆动动画
        self.head_tilt = math.sin(self.animation_time * 3) * 0.2
    
    def check_collision(self, snake):
        """检查是否与蛇发生碰撞"""
        # 获取整数位置用于碰撞检测
        grid_position = (int(self.position[0]), int(self.position[1]))
        
        # 检查蛇头是否与僵尸碰撞
        if snake.get_head_position() == grid_position:
            # 如果蛇不是无敌状态，则判定为碰撞
            if not snake.is_invincible():
                return True
        
        return False
    
    def draw(self, surface):
        """绘制僵尸障碍物"""
        # 计算障碍物位置
        x = int(self.position[0] * GRID_SIZE)
        y = int(self.position[1] * GRID_SIZE)
        
        # 绘制僵尸身体
        body_width = int(GRID_SIZE * 0.7)
        body_height = int(GRID_SIZE * 0.9)
        body_rect = pygame.Rect(
            x + (GRID_SIZE - body_width) // 2,
            y + (GRID_SIZE - body_height) // 2,
            body_width,
            body_height
        )
        pygame.draw.rect(surface, self.zombie_colors['body'], body_rect)
        pygame.draw.rect(surface, self.zombie_colors['detail'], body_rect, 1)
        
        # 绘制僵尸头部（稍微歪斜一些，增加摇晃效果）
        head_size = int(GRID_SIZE * 0.6)
        head_center_x = x + GRID_SIZE // 2
        head_center_y = y + GRID_SIZE // 3
        
        # 计算头部倾斜
        tilt_x = math.sin(self.head_tilt) * 3
        tilt_y = math.cos(self.head_tilt) * 1
        
        head_points = [
            (head_center_x - head_size//2 + tilt_x, head_center_y - head_size//2 - tilt_y),
            (head_center_x + head_size//2 + tilt_x, head_center_y - head_size//2 + tilt_y),
            (head_center_x + head_size//2 - tilt_x, head_center_y + head_size//2 + tilt_y),
            (head_center_x - head_size//2 - tilt_x, head_center_y + head_size//2 - tilt_y)
        ]
        pygame.draw.polygon(surface, self.zombie_colors['head'], head_points)
        pygame.draw.polygon(surface, self.zombie_colors['detail'], head_points, 1)
        
        # 绘制僵尸眼睛
        eye_size = 3
        left_eye_x = head_center_x - head_size//4 + tilt_x//2
        right_eye_x = head_center_x + head_size//4 + tilt_x//2
        eye_y = head_center_y - head_size//8
        
        pygame.draw.circle(surface, self.zombie_colors['eyes'], (int(left_eye_x), int(eye_y)), eye_size)
        pygame.draw.circle(surface, self.zombie_colors['eyes'], (int(right_eye_x), int(eye_y)), eye_size)
        
        # 绘制僵尸嘴（线条）
        mouth_y = head_center_y + head_size//4
        pygame.draw.line(
            surface, 
            self.zombie_colors['detail'],
            (int(head_center_x - head_size//3 + tilt_x), int(mouth_y)),
            (int(head_center_x + head_size//3 + tilt_x), int(mouth_y)),
            2
        )

class ObstacleManager:
    """
    障碍物管理器类
    负责生成和管理障碍物
    """
    
    def __init__(self, difficulty="medium"):
        """
        初始化障碍物管理器
        
        参数:
            difficulty (str): 难度级别
        """
        self.obstacles = []
        self.difficulty = difficulty
        self.spawn_timer = 0
        self.max_obstacles = self._get_max_obstacles()
    
    def _get_max_obstacles(self):
        """
        根据难度获取最大障碍物数量
        
        返回:
            int: 最大障碍物数量
        """
        if self.difficulty == "easy":
            return 3
        elif self.difficulty == "medium":
            return 5
        else:  # hard
            return 8
    
    def _get_spawn_interval(self):
        """
        获取障碍物生成间隔
        
        返回:
            float: 生成间隔（秒）
        """
        if self.difficulty == "easy":
            return 8.0
        elif self.difficulty == "medium":
            return 5.0
        else:  # hard
            return 3.0
    
    def update(self, delta_time, snake_positions):
        """
        更新所有障碍物
        
        参数:
            delta_time: 时间增量（秒）
            snake_positions: 蛇身体位置列表
        """
        # 更新现有障碍物
        for obstacle in self.obstacles:
            obstacle.update(delta_time)
        
        # 检查是否需要生成新障碍物
        self.spawn_timer += delta_time
        if (len(self.obstacles) < self.max_obstacles and 
            self.spawn_timer >= self._get_spawn_interval()):
            self.spawn_timer = 0
            self.spawn_obstacle(snake_positions)
    
    def spawn_obstacle(self, snake_positions):
        """
        生成新障碍物
        
        参数:
            snake_positions: 蛇身体位置列表，用于避免障碍物生成在蛇身上
        """
        # 选择障碍物类型
        if random.random() < 0.3:  # 30%几率生成僵尸
            obstacle = ZombieObstacle()
        else:  # 70%几率生成坟墓
            obstacle = TombstoneObstacle()
        
        # 确保障碍物不会生成在蛇身上
        attempts = 0
        grid_position = (int(obstacle.position[0]), int(obstacle.position[1]))
        while grid_position in snake_positions and attempts < 20:
            if isinstance(obstacle, ZombieObstacle):
                obstacle = ZombieObstacle()
            else:
                obstacle = TombstoneObstacle()
            grid_position = (int(obstacle.position[0]), int(obstacle.position[1]))
            attempts += 1
        
        # 添加到障碍物列表
        if attempts < 20:  # 如果找到合适位置
            self.obstacles.append(obstacle)
    
    def check_collisions(self, snake):
        """
        检查蛇是否与任何障碍物碰撞
        
        参数:
            snake: 蛇对象
        
        返回:
            bool: 是否有碰撞
        """
        for obstacle in self.obstacles:
            if obstacle.check_collision(snake):
                return True
        return False
    
    def draw(self, surface):
        """
        绘制所有障碍物
        
        参数:
            surface: 渲染目标表面
        """
        for obstacle in self.obstacles:
            obstacle.draw(surface)
    
    def set_difficulty(self, difficulty):
        """
        设置难度
        
        参数:
            difficulty (str): 难度级别
        """
        self.difficulty = difficulty
        self.max_obstacles = self._get_max_obstacles()
    
    def clear(self):
        """清除所有障碍物"""
        self.obstacles.clear()
        self.spawn_timer = 0 