"""
游戏场景
实现游戏的主要逻辑
"""

import pygame
import random
import math
from scenes.base_scene import Scene
from entities.snake import Snake
from entities.food import FoodManager
from entities.obstacle import ObstacleManager
from config import (
    GRID_WIDTH, GRID_HEIGHT, GRID_SIZE, GAME_SPEED, SCENES,
    PVZ_GREEN, PVZ_LIGHT_GREEN, PVZ_SKY_BLUE, PVZ_SUN_YELLOW, WHITE, BACKGROUNDS_IMAGES_DIR,
    UP, DOWN, LEFT, RIGHT  # 添加方向常量的导入
)

class GameScene(Scene):
    """
    游戏场景类
    实现游戏的主要逻辑
    """
    
    def __init__(self, game_engine):
        """初始化游戏场景"""
        super().__init__(game_engine)
        
        # 游戏实体
        self.snake = None
        self.food_manager = None
        self.obstacle_manager = None
        
        # 游戏状态
        self.score = 0
        self.move_timer = 0
        self.game_over = False
        
        # 食物生成计时器
        self.food_spawn_timer = 0
        self.min_food_count = 3  # 场景中最少的食物数量
        
        # 场景设置
        self.scene_type = self.game_engine.settings.get("scene", "day")
        self.scene_config = SCENES[self.scene_type]
        
        # 动画时间
        self.animation_time = 0
        
        # 背景图像
        self.background_image = None
        self.use_background_image = self.game_engine.settings.get("use_images", True)
    
    def enter(self, **kwargs):
        """
        进入游戏场景
        
        参数:
            **kwargs: 可选参数
        """
        # 重置游戏状态
        self.score = 0
        self.move_timer = 0
        self.game_over = False
        self.animation_time = 0
        
        # 清除UI管理器的活动按钮
        self.ui_manager.active_buttons = []
        self.ui_manager.active_group = None
        
        # 创建蛇
        self.snake = Snake(self.game_engine)
        
        # 创建食物管理器
        self.food_manager = FoodManager(self.game_engine)
        self.food_manager.set_grid_size(GRID_WIDTH, GRID_HEIGHT)
        self.food_manager.load_images(self.resource_loader)
        
        # 创建障碍物管理器
        self.obstacle_manager = ObstacleManager(self.game_engine)
        
        # 加载背景图像
        if self.use_background_image:
            background_image_name = self.scene_config.get("background_image")
            if background_image_name:
                self.background_image = self.resource_loader.load_image(
                    background_image_name, 
                    directory=BACKGROUNDS_IMAGES_DIR
                )
        
        # 生成初始食物（生成3个食物，确保游戏开始时有足够的食物）
        for _ in range(3):
            self.food_manager.spawn_food(avoid_positions=self.snake.positions)
        
        # 播放背景音乐
        self.resource_loader.play_music()
    
    def exit(self):
        """离开游戏场景"""
        # 停止背景音乐
        self.resource_loader.stop_music()
    
    def handle_event(self, event):
        """
        处理游戏事件
        
        参数:
            event: Pygame事件对象
        """
        if event.type == pygame.KEYDOWN:
            # 方向键控制
            if event.key == pygame.K_UP:
                self.snake.set_direction(UP)
            elif event.key == pygame.K_DOWN:
                self.snake.set_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                self.snake.set_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                self.snake.set_direction(RIGHT)
    
    def update(self, delta_time):
        """
        更新游戏状态
        
        参数:
            delta_time: 时间增量
        """
        if self.game_over:
            return
        
        # 更新动画时间
        self.animation_time += delta_time
        
        # 更新蛇的状态
        self.snake.update(delta_time)
        
        # 更新食物动画
        self.food_manager.update(delta_time)
        
        # 更新障碍物
        self.obstacle_manager.update(delta_time, self.snake.positions)
        
        # 食物生成计时器
        self.food_spawn_timer += delta_time
        
        # 确保场景中始终有足够的食物
        if len(self.food_manager.foods) < self.min_food_count and self.food_spawn_timer >= 2.0:
            self.food_spawn_timer = 0
            self.food_manager.spawn_food(avoid_positions=self.snake.positions)
        
        # 蛇移动计时器
        self.move_timer += delta_time
        move_interval = 1.0 / (GAME_SPEED * self.snake.get_speed())
        
        if self.move_timer >= move_interval:
            self.move_timer = 0
            
            # 移动蛇
            if self.snake.move():
                self.game_over = True
                self.on_game_over()
                return
            
            # 检查食物碰撞
            food = self.food_manager.check_collisions(self.snake.positions[0])
            if food:
                # 应用食物效果
                self.score += food.apply_effect(self.snake)
                
                # 播放音效
                try:
                    self.resource_loader.play_sound("eat_food")
                except Exception as e:
                    print(f"播放音效失败: {e}")
                
                # 移除食物
                self.food_manager.remove_food(food)
                
                # 蛇增长
                self.snake.grow()
                
                # 立即生成新的食物
                self.food_manager.spawn_food(avoid_positions=self.snake.positions)
            
            # 检查障碍物碰撞
            try:
                if self.obstacle_manager and self.obstacle_manager.check_collisions(self.snake):
                    self.game_over = True
                    self.on_game_over()
                    return
            except Exception as e:
                print(f"检查障碍物碰撞时出错: {e}")
                import traceback
                traceback.print_exc()
    
    def render(self, surface):
        """
        渲染游戏画面
        
        参数:
            surface: 渲染目标表面
        """
        # 绘制背景
        self._draw_background(surface)
        
        # 绘制食物
        self.food_manager.draw(surface, GRID_SIZE)
        
        # 绘制障碍物
        self.obstacle_manager.draw(surface)
        
        # 绘制蛇
        self.snake.draw(surface)
        
        # 绘制分数
        self._draw_score(surface)
        
        # 绘制能力图标
        self._draw_abilities(surface)
    
    def on_pause_changed(self, paused):
        """
        处理游戏暂停状态变化
        
        参数:
            paused: 是否暂停
        """
        if paused:
            # 暂停背景音乐
            self.resource_loader.pause_music()
            
            # 绘制暂停提示
            pause_font = self.font_manager.large_font
            pause_text = self.font_manager.render_text("游戏暂停", pause_font, WHITE)
            pause_rect = pause_text.get_rect(center=(self.window.get_width() // 2, self.window.get_height() // 2))
            
            # 创建半透明背景
            overlay = pygame.Surface((self.window.get_width(), self.window.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.window.blit(overlay, (0, 0))
            
            # 显示暂停文本
            self.window.blit(pause_text, pause_rect)
            pygame.display.update()
        else:
            # 恢复背景音乐
            self.resource_loader.unpause_music()
    
    def on_game_over(self):
        """处理游戏结束"""
        try:
            # 播放游戏结束音效
            self.resource_loader.play_sound("game_over")
            
            # 延迟一会儿，让玩家看到游戏结束状态
            pygame.time.delay(1000)
            
            # 切换到游戏结束场景
            self.game_engine.change_scene("game_over", score=self.score)
        except Exception as e:
            print(f"处理游戏结束时出错: {e}")
            import traceback
            traceback.print_exc()
            
            # 如果出错，直接返回主菜单
            try:
                self.game_engine.change_scene("menu")
            except:
                pass
    
    def _draw_background(self, surface):
        """
        绘制游戏背景
        
        参数:
            surface: 渲染目标表面
        """
        if self.use_background_image and self.background_image:
            # 使用图像绘制背景
            surface.blit(self.background_image, (0, 0))
        else:
            # 使用基本图形绘制背景
            # 绘制天空背景
            background_color = self.scene_config["background"]
            surface.fill(background_color)
            
            # 绘制草坪网格
            grid_colors = self.scene_config["grid_colors"]
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    # 棋盘格草地样式
                    color = grid_colors[0] if (x + y) % 2 == 0 else grid_colors[1]
                    
                    pygame.draw.rect(surface, color, pygame.Rect(
                        x * GRID_SIZE, 
                        y * GRID_SIZE, 
                        GRID_SIZE, 
                        GRID_SIZE
                    ))
                    
                    # 添加场景特定的装饰
                    if self.scene_type == "day" and random.random() < 0.05:
                        # 白天场景添加小草
                        grass_height = random.randint(2, 5)
                        grass_width = 2
                        grass_x = x * GRID_SIZE + random.randint(5, GRID_SIZE - 5)
                        grass_y = y * GRID_SIZE + GRID_SIZE - grass_height
                        pygame.draw.rect(surface, (58, 121, 39), pygame.Rect(
                            grass_x, grass_y, grass_width, grass_height
                        ))
                    elif self.scene_type == "night" and random.random() < 0.02:
                        # 夜晚场景添加星星
                        star_x = x * GRID_SIZE + GRID_SIZE // 2
                        star_y = y * GRID_SIZE + GRID_SIZE // 2
                        star_radius = random.randint(1, 2)
                        star_color = (255, 255, 200)
                        pygame.draw.circle(surface, star_color, (star_x, star_y), star_radius)
                    elif self.scene_type == "pool" and random.random() < 0.1 and (x + y) % 3 == 0:
                        # 泳池场景添加水波纹
                        ripple_x = x * GRID_SIZE + GRID_SIZE // 2
                        ripple_y = y * GRID_SIZE + GRID_SIZE // 2
                        ripple_radius = 3 + math.sin(self.animation_time * 2 + (x + y) * 0.1) * 2
                        pygame.draw.circle(surface, (100, 150, 255, 100), (ripple_x, ripple_y), ripple_radius, 1)
    
    def _draw_score(self, surface):
        """
        绘制分数
        
        参数:
            surface: 渲染目标表面
        """
        # 创建分数背景图案（类似PvZ的信息栏）
        score_bg = pygame.Rect(10, 10, 160, 40)
        pygame.draw.rect(surface, (0, 0, 0, 128), score_bg, border_radius=10)
        pygame.draw.rect(surface, (58, 121, 39), score_bg, 2, border_radius=10)
        
        # 绘制阳光图标（小版本）
        sun_icon_radius = 15
        sun_x, sun_y = 30, score_bg.centery
        pygame.draw.circle(surface, PVZ_SUN_YELLOW, (sun_x, sun_y), sun_icon_radius)
        
        # 光芒效果
        for angle in range(0, 360, 60):
            rad_angle = math.radians(angle)
            end_x = sun_x + math.cos(rad_angle) * (sun_icon_radius + 3)
            end_y = sun_y + math.sin(rad_angle) * (sun_icon_radius + 3)
            pygame.draw.line(surface, PVZ_SUN_YELLOW, (sun_x, sun_y), (end_x, end_y), 2)
        
        # 显示分数文本
        score_text = self.font_manager.render_text(f'阳光: {self.score}', self.font_manager.medium_font, WHITE)
        surface.blit(score_text, (50, 15))
    
    def _draw_abilities(self, surface):
        """
        绘制特殊能力状态
        
        参数:
            surface: 渲染目标表面
        """
        abilities_bg = pygame.Rect(10, 60, 160, 40)
        pygame.draw.rect(surface, (0, 0, 0, 128), abilities_bg, border_radius=10)
        pygame.draw.rect(surface, (58, 121, 39), abilities_bg, 2, border_radius=10)
        
        # 绘制护盾状态
        shield_x, shield_y = 40, abilities_bg.centery
        shield_radius = 15
        shield_color = (100, 200, 255) if self.snake.shield_active else (100, 100, 100)
        shield_text_color = WHITE if self.snake.shield_active else (150, 150, 150)
        
        # 绘制护盾图标
        pygame.draw.circle(surface, shield_color, (shield_x, shield_y), shield_radius, 2)
        pygame.draw.circle(surface, shield_color, (shield_x, shield_y), shield_radius - 4, 1)
        
        # 绘制速度状态
        speed_x, speed_y = 120, abilities_bg.centery
        speed_radius = 15
        speed_color = (255, 200, 0) if self.snake.speed_boost_active else (100, 100, 100)
        speed_text_color = WHITE if self.snake.speed_boost_active else (150, 150, 150)
        
        # 绘制速度图标
        for i in range(3):
            start_x = speed_x - 10 + i * 10
            pygame.draw.line(surface, speed_color, (start_x, speed_y - 5), (start_x + 5, speed_y), 2)
            pygame.draw.line(surface, speed_color, (start_x + 5, speed_y), (start_x, speed_y + 5), 2)
        
        # 绘制能力文本
        shield_text = self.font_manager.render_text("护盾", self.font_manager.small_font, shield_text_color)
        speed_text = self.font_manager.render_text("加速", self.font_manager.small_font, speed_text_color)
        
        surface.blit(shield_text, (shield_x - shield_text.get_width() // 2, shield_y + 20))
        surface.blit(speed_text, (speed_x - speed_text.get_width() // 2, speed_y + 20)) 