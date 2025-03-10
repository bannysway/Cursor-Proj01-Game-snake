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
    PVZ_GREEN, PVZ_LIGHT_GREEN, PVZ_SKY_BLUE, PVZ_SUN_YELLOW, WHITE
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
        
        # 场景设置
        self.scene_type = self.game_engine.settings.get("scene", "day")
        self.scene_config = SCENES[self.scene_type]
        
        # 动画时间
        self.animation_time = 0
    
    def enter(self, **kwargs):
        """进入游戏场景"""
        # 重置游戏状态
        self.score = 0
        self.move_timer = 0
        self.game_over = False
        self.animation_time = 0
        
        # 创建游戏实体
        self.snake = Snake()
        self.food_manager = FoodManager()
        
        # 根据难度创建障碍物管理器
        difficulty = self.game_engine.settings.get("difficulty", "medium")
        self.obstacle_manager = ObstacleManager(difficulty)
        
        # 生成初始食物
        self.food_manager.spawn_food([self.snake.get_head_position()])
        
        # 随机选择场景类型（如果没有指定）
        if "scene_type" in kwargs:
            self.scene_type = kwargs["scene_type"]
            self.scene_config = SCENES[self.scene_type]
        
        # 播放背景音乐
        if self.resource_loader.load_music(self.game_engine.settings.get("background_music", "simple_background.wav")):
            self.resource_loader.play_music()
    
    def exit(self):
        """退出游戏场景"""
        # 停止背景音乐
        self.resource_loader.stop_music()
    
    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.KEYDOWN:
            # 方向键控制蛇的移动
            if event.key == pygame.K_UP:
                self.snake.update_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                self.snake.update_direction((0, 1))
            elif event.key == pygame.K_LEFT:
                self.snake.update_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                self.snake.update_direction((1, 0))
    
    def update(self, delta_time):
        """更新游戏状态"""
        if self.game_over:
            return
        
        # 更新动画时间
        self.animation_time += delta_time
        
        # 更新食物动画
        self.food_manager.update(delta_time)
        
        # 更新障碍物
        self.obstacle_manager.update(delta_time, self.snake.positions)
        
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
            self.food_manager.check_collision(self.snake, self)
            
            # 检查障碍物碰撞
            if self.obstacle_manager.check_collisions(self.snake):
                self.game_over = True
                self.on_game_over()
                return
    
    def render(self, surface):
        """渲染游戏画面"""
        # 绘制背景
        self._draw_background(surface)
        
        # 绘制食物
        self.food_manager.draw(surface)
        
        # 绘制障碍物
        self.obstacle_manager.draw(surface)
        
        # 绘制蛇
        self.snake.draw(surface)
        
        # 绘制分数
        self._draw_score(surface)
        
        # 绘制特殊能力状态
        self._draw_abilities(surface)
    
    def on_pause_changed(self, paused):
        """
        游戏暂停状态变化时调用
        
        参数:
            paused (bool): 游戏是否暂停
        """
        if paused:
            # 游戏暂停时的处理
            if self.resource_loader:
                self.resource_loader.pause_music()
            
            # 创建暂停菜单
            if hasattr(self, 'ui_manager') and self.ui_manager:
                self.ui_manager.set_active_group("pause_menu")
        else:
            # 游戏恢复时的处理
            if self.resource_loader:
                self.resource_loader.unpause_music()
            
            # 移除暂停菜单
            if hasattr(self, 'ui_manager') and self.ui_manager:
                self.ui_manager.set_active_group("game")
    
    def on_game_over(self):
        """游戏结束时调用"""
        # 播放游戏结束音效
        try:
            self.resource_loader.play_sound("game_over")
        except:
            pass
        
        # 切换到游戏结束场景
        self.game_engine.change_scene("game_over", score=self.score)
    
    def _draw_background(self, surface):
        """绘制游戏背景"""
        # 绘制天空或背景颜色
        surface.fill(self.scene_config["background"])
        
        # 绘制草坪棋盘格
        grid_colors = self.scene_config["grid_colors"]
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if (x + y) % 2 == 0:
                    color = grid_colors[0]
                else:
                    color = grid_colors[1]
                
                pygame.draw.rect(surface, color, pygame.Rect(
                    x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE
                ))
                
                # 根据场景类型添加不同的装饰
                if self.scene_type == "day" and random.random() < 0.02:
                    # 白天场景添加小草
                    grass_height = random.randint(2, 5)
                    grass_width = 2
                    grass_x = x * GRID_SIZE + random.randint(5, GRID_SIZE - 5)
                    grass_y = y * GRID_SIZE + GRID_SIZE - grass_height
                    pygame.draw.rect(surface, (58, 121, 39), pygame.Rect(
                        grass_x, grass_y, grass_width, grass_height
                    ))
                elif self.scene_type == "night" and random.random() < 0.005:
                    # 夜晚场景添加星星
                    star_x = x * GRID_SIZE + random.randint(5, GRID_SIZE - 5)
                    star_y = y * GRID_SIZE + random.randint(5, GRID_SIZE - 5)
                    star_size = random.randint(1, 3)
                    pygame.draw.circle(surface, (255, 255, 200), (star_x, star_y), star_size)
                elif self.scene_type == "pool" and random.random() < 0.1 and (x + y) % 3 == 0:
                    # 泳池场景添加水波纹
                    ripple_x = x * GRID_SIZE + GRID_SIZE // 2
                    ripple_y = y * GRID_SIZE + GRID_SIZE // 2
                    ripple_radius = 3 + math.sin(self.animation_time * 2 + (x + y) * 0.1) * 2
                    pygame.draw.circle(surface, (100, 150, 255, 100), (ripple_x, ripple_y), ripple_radius, 1)
    
    def _draw_score(self, surface):
        """绘制分数"""
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
        """绘制特殊能力状态"""
        # 如果有活跃的能力，绘制能力图标
        y_offset = 60
        
        for ability, duration in self.snake.abilities.items():
            ability_bg = pygame.Rect(10, y_offset, 40, 40)
            pygame.draw.rect(surface, (0, 0, 0, 128), ability_bg, border_radius=5)
            pygame.draw.rect(surface, (58, 121, 39), ability_bg, 2, border_radius=5)
            
            # 根据能力类型绘制不同图标
            if ability == "shield":
                # 护盾图标
                shield_radius = 15
                center_x, center_y = ability_bg.centerx, ability_bg.centery
                pygame.draw.circle(surface, (100, 200, 255), (center_x, center_y), shield_radius)
                pygame.draw.circle(surface, (50, 150, 255), (center_x, center_y), shield_radius, 2)
            elif ability == "speed_up":
                # 加速图标
                center_x, center_y = ability_bg.centerx, ability_bg.centery
                # 绘制速度箭头
                pygame.draw.polygon(surface, (0, 200, 0), [
                    (center_x - 10, center_y + 5),
                    (center_x, center_y - 10),
                    (center_x + 10, center_y + 5),
                    (center_x, center_y)
                ])
            
            # 绘制剩余时间条
            max_duration = 100 if ability == "shield" else 150
            time_ratio = min(1.0, duration / max_duration)
            time_width = int(36 * time_ratio)
            pygame.draw.rect(surface, (200, 200, 200), pygame.Rect(
                ability_bg.left + 2, ability_bg.bottom - 7, 36, 5
            ))
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(
                ability_bg.left + 2, ability_bg.bottom - 7, time_width, 5
            ))
            
            y_offset += 45 