"""
食物实体
包含各种类型的食物及其效果
"""

import random
import pygame
import math
from config import FOOD_TYPES, FOOD_IMAGES_DIR, PVZ_SUN_YELLOW, PVZ_GREEN, PVZ_BROWN

class BaseFood:
    """
    基础食物类
    所有食物类型的父类
    """
    
    def __init__(self, position=None, food_type="sun", game_engine=None):
        """
        初始化食物
        
        参数:
            position: 食物位置 (x, y)，如果为None则随机生成
            food_type: 食物类型
            game_engine: 游戏引擎实例
        """
        self.game_engine = game_engine
        self.food_type = food_type
        self.position = position
        self.grid_position = None  # 网格位置，将在spawn方法中设置
        
        # 确保food_type是字符串类型
        if not isinstance(food_type, str):
            print(f"警告: food_type不是字符串类型: {food_type}, 使用默认值'sun'")
            self.food_type = "sun"
        
        try:
            self.score = FOOD_TYPES[self.food_type]["score"]
            self.effect = FOOD_TYPES[self.food_type]["effect"]
            self.image_name = FOOD_TYPES[self.food_type]["image"]
        except KeyError as e:
            print(f"警告: 无法获取食物类型'{self.food_type}'的属性: {e}, 使用默认值")
            self.score = 10
            self.effect = None
            self.image_name = None
        
        self.image = None
        
        # 动画参数
        self.animation_offset = random.random() * math.pi * 2  # 随机初始偏移
        self.animation_speed = 0.05
        self.hover_range = 3  # 悬浮范围
        
        # 如果位置为None，则在spawn方法中生成随机位置
        if position is not None:
            self.grid_position = position
    
    def spawn(self, grid_width, grid_height, avoid_positions=None):
        """
        在随机位置生成食物
        
        参数:
            grid_width: 网格宽度
            grid_height: 网格高度
            avoid_positions: 需要避开的位置列表
            
        返回:
            bool: 是否成功生成
        """
        if avoid_positions is None:
            avoid_positions = []
        
        # 尝试最多10次找到一个可用位置
        for _ in range(10):
            x = random.randint(0, grid_width - 1)
            y = random.randint(0, grid_height - 1)
            
            # 检查位置是否可用
            if (x, y) not in avoid_positions:
                self.grid_position = (x, y)
                return True
        
        # 如果尝试10次都失败，返回False
        return False
    
    def update(self, delta_time):
        """
        更新食物状态
        
        参数:
            delta_time: 时间增量
        """
        # 更新动画
        self.animation_offset = (self.animation_offset + self.animation_speed) % (math.pi * 2)
    
    def check_collision(self, snake_head_pos):
        """
        检查是否与蛇头碰撞
        
        参数:
            snake_head_pos: 蛇头位置
            
        返回:
            bool: 是否碰撞
        """
        return self.grid_position == snake_head_pos
    
    def apply_effect(self, snake):
        """
        应用食物效果
        
        参数:
            snake: 蛇实体
            
        返回:
            int: 得分
        """
        # 基础食物只增加分数，不应用特殊效果
        return self.score
    
    def draw(self, surface, grid_size, use_images=True):
        """
        绘制食物
        
        参数:
            surface: 绘制表面
            grid_size: 网格大小
            use_images: 是否使用图像
        """
        if self.grid_position is None:
            return
        
        # 计算实际像素位置
        x, y = self.grid_position
        pixel_x = x * grid_size
        pixel_y = y * grid_size
        
        # 添加悬浮动画效果
        hover_offset = int(math.sin(self.animation_offset) * self.hover_range)
        pixel_y += hover_offset
        
        # 如果有图像并且设置使用图像，则绘制图像
        if self.image is not None and use_images:
            # 居中绘制图像
            image_rect = self.image.get_rect(center=(pixel_x + grid_size // 2, pixel_y + grid_size // 2))
            surface.blit(self.image, image_rect)
        else:
            # 否则绘制简单图形
            color = PVZ_SUN_YELLOW  # 默认为阳光黄色
            
            # 根据食物类型选择不同颜色
            if self.food_type == "sunflower":
                color = (255, 200, 0)  # 向日葵黄色
            elif self.food_type == "walnut":
                color = PVZ_BROWN  # 坚果棕色
            elif self.food_type == "peashooter":
                color = PVZ_GREEN  # 豌豆射手绿色
            
            # 绘制圆形食物
            pygame.draw.circle(
                surface,
                color,
                (pixel_x + grid_size // 2, pixel_y + grid_size // 2),
                grid_size // 3
            )

class SunflowerFood(BaseFood):
    """
    向日葵食物
    提供更高的分数
    """
    
    def __init__(self, position=None, food_type="sunflower", game_engine=None):
        """初始化向日葵食物"""
        super().__init__(position=position, food_type=food_type, game_engine=game_engine)
        
        # 向日葵特有参数
        self.hover_range = 5  # 更大的悬浮范围
    
    def draw(self, surface, grid_size, use_images=True):
        """绘制向日葵食物"""
        if self.image is not None and use_images:
            super().draw(surface, grid_size, use_images)
        else:
            if self.grid_position is None:
                return
            
            # 计算实际像素位置
            x, y = self.grid_position
            pixel_x = x * grid_size
            pixel_y = y * grid_size
            
            # 添加悬浮动画效果
            hover_offset = int(math.sin(self.animation_offset) * self.hover_range)
            pixel_y += hover_offset
            
            # 绘制向日葵
            center_x = pixel_x + grid_size // 2
            center_y = pixel_y + grid_size // 2
            
            # 绘制花盘
            pygame.draw.circle(
                surface,
                (255, 200, 0),  # 向日葵黄色
                (center_x, center_y),
                grid_size // 3
            )
            
            # 绘制花瓣
            for i in range(8):
                angle = i * math.pi / 4
                petal_x = center_x + int(math.cos(angle) * grid_size // 2.5)
                petal_y = center_y + int(math.sin(angle) * grid_size // 2.5)
                
                pygame.draw.circle(
                    surface,
                    (255, 220, 0),  # 花瓣黄色
                    (petal_x, petal_y),
                    grid_size // 6
                )

class WalnutFood(BaseFood):
    """
    坚果食物
    提供护盾效果
    """
    
    def __init__(self, position=None, food_type="walnut", game_engine=None):
        """初始化坚果食物"""
        super().__init__(position=position, food_type=food_type, game_engine=game_engine)
        
        # 坚果特有参数
        self.hover_range = 2  # 较小的悬浮范围
    
    def apply_effect(self, snake):
        """应用坚果效果 - 提供护盾"""
        if snake:
            snake.add_ability("shield")
        return self.score
    
    def draw(self, surface, grid_size, use_images=True):
        """绘制坚果食物"""
        if self.image is not None and use_images:
            super().draw(surface, grid_size, use_images)
        else:
            if not self.grid_position:
                return
                
            # 计算实际像素位置
            x, y = self.grid_position
            pixel_x = x * grid_size
            pixel_y = y * grid_size
            
            # 添加悬浮动画效果
            hover_offset = int(math.sin(self.animation_offset) * self.hover_range)
            pixel_y += hover_offset
            
            # 绘制坚果
            center_x = pixel_x + grid_size // 2
            center_y = pixel_y + grid_size // 2
            
            # 绘制坚果主体
            pygame.draw.ellipse(
                surface,
                PVZ_BROWN,  # 坚果棕色
                pygame.Rect(
                    center_x - grid_size // 3,
                    center_y - grid_size // 2.5,
                    grid_size // 1.5,
                    grid_size // 1.25
                )
            )
            
            # 绘制坚果脸部
            pygame.draw.ellipse(
                surface,
                (220, 200, 180),  # 浅棕色
                pygame.Rect(
                    center_x - grid_size // 4,
                    center_y - grid_size // 3,
                    grid_size // 2,
                    grid_size // 2
                )
            )

class PeashooterFood(BaseFood):
    """
    豌豆射手食物
    提供速度提升效果
    """
    
    def __init__(self, position=None, food_type="peashooter", game_engine=None):
        """初始化豌豆射手食物"""
        super().__init__(position=position, food_type=food_type, game_engine=game_engine)
        
        # 豌豆射手特有参数
        self.hover_range = 4
    
    def apply_effect(self, snake):
        """应用豌豆射手效果 - 提供速度提升"""
        if snake:
            snake.add_ability("speed_up")
        return self.score
    
    def draw(self, surface, grid_size, use_images=True):
        """绘制豌豆射手食物"""
        if self.image is not None and use_images:
            super().draw(surface, grid_size, use_images)
        else:
            if self.grid_position is None:
                return
            
            # 计算实际像素位置
            x, y = self.grid_position
            pixel_x = x * grid_size
            pixel_y = y * grid_size
            
            # 添加悬浮动画效果
            hover_offset = int(math.sin(self.animation_offset) * self.hover_range)
            pixel_y += hover_offset
            
            # 绘制豌豆射手
            center_x = pixel_x + grid_size // 2
            center_y = pixel_y + grid_size // 2
            
            # 绘制头部
            pygame.draw.circle(
                surface,
                PVZ_GREEN,  # 豌豆射手绿色
                (center_x, center_y),
                grid_size // 3
            )
            
            # 绘制豌豆
            pygame.draw.circle(
                surface,
                (100, 200, 100),  # 浅绿色
                (center_x + grid_size // 3, center_y),
                grid_size // 5
            )

class FoodManager:
    """
    食物管理器
    负责生成和管理食物实体
    """
    
    def __init__(self, game_engine=None):
        """
        初始化食物管理器
        
        参数:
            game_engine: 游戏引擎实例
        """
        self.game_engine = game_engine
        self.foods = []  # 当前场景中的食物列表
        self.food_images = {}  # 食物图像 {food_type: image}
        self.grid_width = 0
        self.grid_height = 0
        
        # 食物类型映射
        self.food_classes = {
            "sun": BaseFood,
            "sunflower": SunflowerFood,
            "walnut": WalnutFood,
            "peashooter": PeashooterFood
        }
    
    def load_images(self, resource_loader):
        """
        加载食物图像
        
        参数:
            resource_loader: 资源加载器
        """
        # 检查是否使用图像
        use_images = self.game_engine.config.DEFAULT_SETTINGS.get("use_images", True) if self.game_engine else True
        
        if not use_images:
            return
        
        # 获取食物图像目录
        food_images_dir = FOOD_IMAGES_DIR
        
        # 加载每种食物的图像
        for food_type, food_info in FOOD_TYPES.items():
            image_name = food_info["image"]
            if image_name:
                image_path = f"{food_images_dir}/{image_name}"
                self.food_images[food_type] = resource_loader.load_image(image_path)
    
    def set_grid_size(self, width, height):
        """
        设置网格大小
        
        参数:
            width: 网格宽度
            height: 网格高度
        """
        self.grid_width = width
        self.grid_height = height
    
    def spawn_food(self, food_type=None, position=None, avoid_positions=None):
        """
        生成食物
        
        参数:
            food_type: 食物类型，如果为None则随机选择
            position: 食物位置，如果为None则随机生成
            avoid_positions: 需要避开的位置列表
            
        返回:
            BaseFood: 生成的食物实体
        """
        # 如果没有指定食物类型，根据权重随机选择
        if food_type is None:
            food_type = self._random_food_type()
        
        print(f"尝试生成食物类型: {food_type}")
        
        # 创建食物实例
        food_class = self.food_classes.get(food_type, BaseFood)
        # 注意参数顺序：position, food_type, game_engine
        food = food_class(position=position, food_type=food_type, game_engine=self.game_engine)
        
        # 如果没有指定位置，随机生成位置
        if position is None:
            # 获取蛇身体位置列表
            snake_positions = []
            if avoid_positions:
                snake_positions = avoid_positions
            
            # 尝试生成食物
            if not food.spawn(self.grid_width, self.grid_height, snake_positions):
                print(f"无法生成食物: 找不到合适的位置")
                return None  # 如果无法生成食物，返回None
        
        # 设置食物图像
        if food.food_type in self.food_images:
            food.image = self.food_images[food.food_type]
        
        # 添加到食物列表
        self.foods.append(food)
        
        print(f"成功生成食物: {food.food_type}, 位置: {food.grid_position}")
        return food
    
    def _random_food_type(self):
        """
        根据权重随机选择食物类型
        
        返回:
            str: 食物类型
        """
        # 计算总权重
        total_weight = sum(food_info["weight"] for food_info in FOOD_TYPES.values())
        
        # 随机选择
        r = random.uniform(0, total_weight)
        current_weight = 0
        
        for food_type, food_info in FOOD_TYPES.items():
            current_weight += food_info["weight"]
            if r <= current_weight:
                return food_type
        
        # 默认返回阳光
        return "sun"
    
    def update(self, delta_time):
        """
        更新所有食物
        
        参数:
            delta_time: 时间增量
        """
        for food in self.foods:
            food.update(delta_time)
    
    def check_collisions(self, snake_head_pos):
        """
        检查是否有食物与蛇头碰撞
        
        参数:
            snake_head_pos: 蛇头位置
            
        返回:
            BaseFood: 碰撞的食物，如果没有碰撞则返回None
        """
        for food in self.foods:
            if food.check_collision(snake_head_pos):
                return food
        return None
    
    def remove_food(self, food):
        """
        移除食物
        
        参数:
            food: 要移除的食物
        """
        if food in self.foods:
            self.foods.remove(food)
    
    def clear(self):
        """清空所有食物"""
        self.foods.clear()
    
    def draw(self, surface, grid_size):
        """
        绘制所有食物
        
        参数:
            surface: 绘制表面
            grid_size: 网格大小
        """
        use_images = self.game_engine.config.DEFAULT_SETTINGS.get("use_images", True) if self.game_engine else True
        
        for food in self.foods:
            food.draw(surface, grid_size, use_images) 