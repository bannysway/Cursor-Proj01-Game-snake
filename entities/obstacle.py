"""
障碍物实体
定义游戏中的各种障碍物类型和行为
"""

import pygame
import random
import math
from config import (
    GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, OBSTACLE_TYPES,
    PVZ_GREEN, PVZ_DARK_GREEN, DIFFICULTY_LEVELS, OBSTACLES_IMAGES_DIR
)

class BaseObstacle:
    """
    基础障碍物类
    所有障碍物类型的父类
    """
    
    def __init__(self):
        """初始化障碍物"""
        self.position = (0, 0)  # 障碍物位置
        self.speed = 0  # 移动速度
        self.damage = 1  # 造成的伤害
        self.image = None  # 障碍物图像
        
        # 动画参数
        self.animation_offset = random.random() * math.pi * 2  # 随机初始偏移
        self.animation_speed = 0.05
    
    def spawn(self, avoid_positions=None):
        """
        在随机位置生成障碍物
        
        参数:
            avoid_positions: 需要避开的位置列表
            
        返回:
            bool: 是否成功生成
        """
        if avoid_positions is None:
            avoid_positions = []
        
        # 尝试最多10次找到一个可用位置
        for _ in range(10):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            
            # 检查位置是否可用
            if (x, y) not in avoid_positions:
                self.position = (x, y)
                return True
        
        # 如果尝试10次都失败，返回False
        return False
    
    def update(self, delta_time, avoid_positions=None):
        """
        更新障碍物状态
        
        参数:
            delta_time: 时间增量
            avoid_positions: 需要避开的位置列表
        """
        # 更新动画
        self.animation_offset = (self.animation_offset + self.animation_speed) % (math.pi * 2)
    
    def draw(self, surface, grid_size, use_images=True):
        """
        绘制障碍物
        
        参数:
            surface: 绘制表面
            grid_size: 网格大小
            use_images: 是否使用图像
        """
        if not self.position:
            return
            
        # 计算实际像素位置
        x, y = self.position
        pixel_x = x * grid_size
        pixel_y = y * grid_size
        
        # 如果有图像并且设置使用图像，则绘制图像
        if self.image is not None and use_images:
            # 居中绘制图像
            image_rect = self.image.get_rect(center=(pixel_x + grid_size // 2, pixel_y + grid_size // 2))
            surface.blit(self.image, image_rect)
        else:
            # 否则绘制简单图形
            pygame.draw.rect(
                surface,
                PVZ_DARK_GREEN,
                pygame.Rect(pixel_x + 5, pixel_y + 5, grid_size - 10, grid_size - 10)
            )


class TombstoneObstacle(BaseObstacle):
    """
    墓碑障碍物
    静止不动的障碍物
    """
    
    def __init__(self):
        """初始化墓碑障碍物"""
        super().__init__()
        self.speed = OBSTACLE_TYPES["tombstone"]["speed"]
        self.damage = OBSTACLE_TYPES["tombstone"]["damage"]
    
    def draw(self, surface, grid_size, use_images=True):
        """
        绘制墓碑障碍物
        
        参数:
            surface: 绘制表面
            grid_size: 网格大小
            use_images: 是否使用图像
        """
        if self.image is not None and use_images:
            super().draw(surface, grid_size, use_images)
        else:
            if not self.position:
                return
                
            # 计算实际像素位置
            x, y = self.position
            pixel_x = x * grid_size
            pixel_y = y * grid_size
            
            # 绘制墓碑
            # 墓碑底座
            pygame.draw.rect(
                surface,
                (100, 100, 100),  # 灰色
                pygame.Rect(
                    pixel_x + grid_size // 4,
                    pixel_y + grid_size // 2,
                    grid_size // 2,
                    grid_size // 3
                )
            )
            
            # 墓碑主体
            pygame.draw.rect(
                surface,
                (150, 150, 150),  # 浅灰色
                pygame.Rect(
                    pixel_x + grid_size // 4,
                    pixel_y + grid_size // 6,
                    grid_size // 2,
                    grid_size // 2
                ),
                border_radius=3
            )
            
            # 墓碑纹理
            pygame.draw.line(
                surface,
                (100, 100, 100),  # 深灰色
                (pixel_x + grid_size // 3, pixel_y + grid_size // 4),
                (pixel_x + 2 * grid_size // 3, pixel_y + grid_size // 4),
                1
            )
            
            pygame.draw.line(
                surface,
                (100, 100, 100),  # 深灰色
                (pixel_x + grid_size // 3, pixel_y + grid_size // 3),
                (pixel_x + 2 * grid_size // 3, pixel_y + grid_size // 3),
                1
            )


class ZombieObstacle(BaseObstacle):
    """
    僵尸障碍物
    会缓慢移动的障碍物
    """
    
    def __init__(self):
        """初始化僵尸障碍物"""
        super().__init__()
        self.speed = OBSTACLE_TYPES["zombie"]["speed"]
        self.damage = OBSTACLE_TYPES["zombie"]["damage"]
        self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])  # 随机初始方向
        self.move_timer = 0
        self.move_interval = 1.0 / self.speed if self.speed > 0 else float('inf')
    
    def update(self, delta_time, avoid_positions=None):
        """
        更新僵尸障碍物状态
        
        参数:
            delta_time: 时间增量
            avoid_positions: 需要避开的位置列表
        """
        super().update(delta_time, avoid_positions)
        
        # 如果速度为0，不移动
        if self.speed <= 0:
            return
        
        # 更新移动计时器
        self.move_timer += delta_time
        
        # 移动僵尸
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            
            # 计算新位置
            new_x = (self.position[0] + self.direction[0]) % GRID_WIDTH
            new_y = (self.position[1] + self.direction[1]) % GRID_HEIGHT
            new_position = (new_x, new_y)
            
            # 检查新位置是否可用
            if avoid_positions and new_position in avoid_positions:
                # 如果新位置不可用，改变方向
                self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
            else:
                # 更新位置
                self.position = new_position
                
                # 有小概率改变方向
                if random.random() < 0.1:
                    self.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
    
    def draw(self, surface, grid_size, use_images=True):
        """
        绘制僵尸障碍物
        
        参数:
            surface: 绘制表面
            grid_size: 网格大小
            use_images: 是否使用图像
        """
        if self.image is not None and use_images:
            super().draw(surface, grid_size, use_images)
        else:
            if not self.position:
                return
                
            # 计算实际像素位置
            x, y = self.position
            pixel_x = x * grid_size
            pixel_y = y * grid_size
            
            # 添加动画效果
            wobble = math.sin(self.animation_offset * 2) * 2
            
            # 绘制僵尸
            center_x = pixel_x + grid_size // 2
            center_y = pixel_y + grid_size // 2
            
            # 绘制僵尸身体
            body_color = (100, 100, 100)  # 灰色
            pygame.draw.rect(
                surface,
                body_color,
                pygame.Rect(
                    center_x - grid_size // 3,
                    center_y - grid_size // 4,
                    grid_size // 1.5,
                    grid_size // 2
                )
            )
            
            # 绘制僵尸头部
            head_color = (150, 150, 150)  # 浅灰色
            pygame.draw.circle(
                surface,
                head_color,
                (center_x, center_y - grid_size // 3),
                grid_size // 4
            )
            
            # 绘制僵尸眼睛
            eye_color = (255, 0, 0)  # 红色
            pygame.draw.circle(
                surface,
                eye_color,
                (center_x - grid_size // 8, center_y - grid_size // 3),
                grid_size // 10
            )
            pygame.draw.circle(
                surface,
                eye_color,
                (center_x + grid_size // 8, center_y - grid_size // 3),
                grid_size // 10
            )
            
            # 绘制僵尸手臂
            arm_color = body_color
            # 左臂
            pygame.draw.line(
                surface,
                arm_color,
                (center_x - grid_size // 3, center_y),
                (center_x - grid_size // 2, center_y + wobble),
                3
            )
            # 右臂
            pygame.draw.line(
                surface,
                arm_color,
                (center_x + grid_size // 3, center_y),
                (center_x + grid_size // 2, center_y - wobble),
                3
            )


class ObstacleManager:
    """
    障碍物管理器
    负责生成和管理障碍物
    """
    
    def __init__(self, game_engine):
        """
        初始化障碍物管理器
        
        参数:
            game_engine: 游戏引擎实例
        """
        self.game_engine = game_engine
        self.obstacles = []  # 障碍物列表
        self.spawn_timer = 0  # 生成计时器
        self.obstacle_images = {}  # 障碍物图像 {type: image}
        self.grid_width = GRID_WIDTH
        self.grid_height = GRID_HEIGHT
        self.game_time = 0  # 游戏运行时间，用于延迟障碍物生成
        self.max_obstacles = 5  # 最大障碍物数量
        
        # 加载障碍物图像
        self.load_images()
        
        # 获取游戏难度
        try:
            self.difficulty = self.game_engine.settings.get("difficulty", "medium")
            self.spawn_frequency = DIFFICULTY_LEVELS[self.difficulty]["obstacle_frequency"]
        except Exception as e:
            print(f"初始化障碍物管理器时出错: {e}")
            # 使用默认值
            self.difficulty = "medium"
            self.spawn_frequency = 0.02
    
    def load_images(self):
        """加载障碍物图像"""
        # 检查是否使用图像
        use_images = self.game_engine.settings.get("use_images", True)
        
        if not use_images:
            return
        
        # 加载每种障碍物的图像
        for obstacle_type, obstacle_info in OBSTACLE_TYPES.items():
            image_name = obstacle_info["image"]
            if image_name:
                image_path = f"{OBSTACLES_IMAGES_DIR}/{image_name}"
                self.obstacle_images[obstacle_type] = self.game_engine.resource_loader.load_image(image_path)
    
    def spawn_obstacle(self, obstacle_type=None, position=None, avoid_positions=None):
        """
        生成障碍物
        
        参数:
            obstacle_type: 障碍物类型，如果为None则随机选择
            position: 障碍物位置，如果为None则随机生成
            avoid_positions: 需要避开的位置列表
            
        返回:
            BaseObstacle: 生成的障碍物
        """
        # 如果没有指定障碍物类型，随机选择
        if obstacle_type is None:
            obstacle_type = random.choice(list(OBSTACLE_TYPES.keys()))
        
        # 创建障碍物实例
        if obstacle_type == "zombie":
            obstacle = ZombieObstacle()
        else:
            obstacle = TombstoneObstacle()
        
        # 设置障碍物属性
        obstacle.speed = OBSTACLE_TYPES[obstacle_type]["speed"]
        obstacle.damage = OBSTACLE_TYPES[obstacle_type]["damage"]
        
        # 设置障碍物图像
        if obstacle_type in self.obstacle_images:
            obstacle.image = self.obstacle_images[obstacle_type]
        
        # 如果没有指定位置，随机生成位置
        if position is None:
            # 确保障碍物不会生成在蛇身上或其他障碍物上
            existing_positions = []
            
            # 添加其他障碍物的位置
            for existing_obstacle in self.obstacles:
                existing_positions.append(existing_obstacle.position)
            
            # 添加需要避开的位置
            if avoid_positions:
                existing_positions.extend(avoid_positions)
            
            # 尝试生成障碍物
            if not obstacle.spawn(existing_positions):
                return None  # 如果无法生成障碍物，返回None
        else:
            obstacle.position = position
        
        # 添加到障碍物列表
        self.obstacles.append(obstacle)
        
        return obstacle
    
    def update(self, delta_time, avoid_positions=None):
        """
        更新所有障碍物
        
        参数:
            delta_time: 时间增量
            avoid_positions: 需要避开的位置列表
        """
        # 更新游戏时间
        self.game_time += delta_time
        
        # 更新现有障碍物
        for obstacle in self.obstacles:
            obstacle.update(delta_time, avoid_positions)
        
        # 障碍物生成计时器
        self.spawn_timer += delta_time
        
        # 只有在游戏开始10秒后才开始生成障碍物
        if self.game_time < 10.0:
            return
        
        # 限制障碍物的最大数量
        if len(self.obstacles) >= self.max_obstacles:
            return
        
        # 根据难度和计时器决定是否生成新的障碍物
        if self.spawn_timer >= 3.0 and random.random() < self.spawn_frequency:
            self.spawn_timer = 0
            self.spawn_obstacle(avoid_positions=avoid_positions)
    
    def check_collisions(self, snake):
        """
        检查蛇与障碍物的碰撞
        
        参数:
            snake: 蛇对象
            
        返回:
            bool: 是否发生碰撞
        """
        try:
            # 获取蛇头位置
            if not snake or not hasattr(snake, 'positions') or not snake.positions:
                return False
                
            head_pos = snake.positions[0]
            
            # 检查是否与任何障碍物碰撞
            for obstacle in self.obstacles:
                if head_pos == obstacle.position:
                    # 如果蛇有护盾，不会碰撞
                    if hasattr(snake, 'shield_active') and snake.shield_active:
                        return False
                    
                    return True
            
            return False
        except Exception as e:
            print(f"检查障碍物碰撞时出错: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def draw(self, surface):
        """
        绘制所有障碍物
        
        参数:
            surface: 渲染目标表面
        """
        for obstacle in self.obstacles:
            obstacle.draw(surface, GRID_SIZE, self.game_engine.settings.get("use_images", True)) 