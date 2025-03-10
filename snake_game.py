"""
贪吃蛇游戏 - Snake Game
一个简单的贪吃蛇游戏，使用Python和Pygame库开发。
采用植物大战僵尸卡通风格设计。

操作方法：
- 方向键：控制蛇的移动
- 空格键：暂停/继续游戏
- ESC键：退出游戏
- 回车键：开始游戏/重新开始
"""

import pygame
import sys
import random
import time
import math
import os

# 初始化Pygame
pygame.init()

# 定义颜色（RGB值）- 植物大战僵尸风格
BLACK = (0, 0, 0)           # 黑色
WHITE = (255, 255, 255)     # 白色
PVZ_GREEN = (87, 183, 59)   # PVZ风格草地绿
PVZ_DARK_GREEN = (58, 121, 39)  # PVZ深绿色
PVZ_LIGHT_GREEN = (129, 212, 75)  # PVZ浅绿色
PVZ_BROWN = (145, 102, 39)  # PVZ土壤棕色
PVZ_SKY_BLUE = (157, 209, 255)  # PVZ天空蓝
PVZ_SUN_YELLOW = (250, 233, 80)  # PVZ阳光黄
PVZ_CHERRY_RED = (255, 68, 68)  # PVZ樱桃炸弹红
PVZ_BLUE = (60, 160, 255)   # PVZ蓝色

# 游戏设置
WINDOW_WIDTH = 800        # 窗口宽度
WINDOW_HEIGHT = 600       # 窗口高度
GRID_SIZE = 30            # 网格大小（增大以提高可视性）
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE  # 网格宽度（列数）
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE  # 网格高度（行数）
GAME_SPEED = 10           # 游戏速度（帧率）

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 创建游戏窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('植物大战僵尸风格贪吃蛇')  # 设置窗口标题

# 创建时钟对象（用于控制游戏帧率）
clock = pygame.time.Clock()

# 字体设置 - 解决中文显示问题
def init_fonts():
    """初始化字体，解决中文显示问题"""
    # 定义可能可用的中文字体列表（Windows系统）
    chinese_fonts = [
        'SimHei',           # 黑体
        'Microsoft YaHei',  # 微软雅黑
        'SimSun',           # 宋体
        'NSimSun',          # 新宋体
        'FangSong',         # 仿宋
        'KaiTi',            # 楷体
        'Arial Unicode MS'  # 通用Unicode字体
    ]
    
    # 获取系统中可用的字体列表
    available_fonts = pygame.font.get_fonts()
    
    # 从中文字体列表中选择第一个可用的字体
    font_name = None
    for chinese_font in chinese_fonts:
        if chinese_font.lower() in available_fonts:
            font_name = chinese_font
            print(f"使用中文字体: {font_name}")
            break
    
    # 如果没有可用的中文字体，尝试默认字体或使用文件路径
    if font_name is None:
        # 尝试使用系统默认字体
        print("无法找到支持中文的字体，尝试使用默认字体")
        try:
            # 尝试使用pygame默认字体
            default_font = pygame.font.get_default_font()
            font = pygame.font.Font(default_font, 30)
            title_font = pygame.font.Font(default_font, 60)
            subtitle_font = pygame.font.Font(default_font, 24)
            
            # 检查字体是否支持中文（测试渲染中文字符）
            test_render = font.render("测试中文", True, (0, 0, 0))
            if test_render.get_width() > 10:  # 如果宽度合理，说明渲染成功
                print(f"使用默认字体: {default_font}")
                return font, title_font, subtitle_font
        except:
            pass
        
        # 最后尝试在Windows系统常见路径中查找字体文件
        font_paths = [
            "C:\\Windows\\Fonts\\simhei.ttf",  # 黑体
            "C:\\Windows\\Fonts\\msyh.ttc",    # 微软雅黑
            "C:\\Windows\\Fonts\\simsun.ttc",  # 宋体
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = pygame.font.Font(font_path, 30)
                    title_font = pygame.font.Font(font_path, 60)
                    subtitle_font = pygame.font.Font(font_path, 24)
                    print(f"使用字体文件: {font_path}")
                    return font, title_font, subtitle_font
                except:
                    continue
    
    # 如果找到了可用的中文字体，使用SysFont
    try:
        font = pygame.font.SysFont(font_name, 30)
        title_font = pygame.font.SysFont(font_name, 60, bold=True)
        subtitle_font = pygame.font.SysFont(font_name, 24)
    except:
        # 如果加载失败，使用默认字体
        print("加载中文字体失败，使用默认字体")
        font = pygame.font.Font(None, 30)
        title_font = pygame.font.Font(None, 60)
        subtitle_font = pygame.font.Font(None, 24)
    
    return font, title_font, subtitle_font

# 初始化字体
font, title_font, subtitle_font = init_fonts()

# 绘制PvZ风格的草坪背景
def draw_pvz_background(surface):
    """绘制植物大战僵尸风格的草坪背景"""
    # 绘制天空背景
    pygame.draw.rect(surface, PVZ_SKY_BLUE, pygame.Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # 绘制草坪
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            # 棋盘格草地样式
            if (x + y) % 2 == 0:
                color = PVZ_GREEN
            else:
                color = PVZ_LIGHT_GREEN
                
            pygame.draw.rect(surface, color, pygame.Rect(
                x * GRID_SIZE, 
                y * GRID_SIZE, 
                GRID_SIZE, 
                GRID_SIZE
            ))
            
            # 添加草地纹理细节 - 小草点缀
            if random.random() < 0.1:  # 随机在部分格子上绘制小草
                grass_height = random.randint(2, 5)
                grass_width = 2
                grass_x = x * GRID_SIZE + random.randint(5, GRID_SIZE - 5)
                grass_y = y * GRID_SIZE + GRID_SIZE - grass_height
                pygame.draw.rect(surface, PVZ_DARK_GREEN, pygame.Rect(
                    grass_x, grass_y, grass_width, grass_height
                ))

class Snake:
    """蛇类，负责蛇的移动、生长和碰撞检测 - PvZ风格"""
    
    def __init__(self):
        """初始化蛇"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # 蛇的位置，初始在屏幕中央
        self.direction = RIGHT  # 初始方向向右
        self.next_direction = RIGHT  # 下一步的方向
        self.grew = False  # 是否刚吃了食物需要生长
        self.animation_offset = 0  # 动画偏移量，用于制作摆动效果
    
    def get_head_position(self):
        """获取蛇头位置"""
        return self.positions[0]
    
    def update_direction(self, direction):
        """更新蛇的移动方向"""
        # 不能直接向相反方向移动，例如向右移动时不能直接向左移动
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction
    
    def move(self):
        """移动蛇"""
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
        if new_head in self.positions[1:]:
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
            
        return False  # 游戏继续
    
    def grow(self):
        """蛇吃到食物后生长"""
        self.grew = True
    
    def draw(self, surface):
        """在屏幕上绘制蛇 - PvZ豌豆射手风格"""
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
                pygame.draw.circle(surface, PVZ_LIGHT_GREEN, (center_x, body_center_y), body_radius)
                pygame.draw.circle(surface, PVZ_GREEN, (center_x, body_center_y), body_radius, 1)
                
                # 添加叶子细节
                if i % 3 == 0:  # 每隔几节添加一片叶子
                    leaf_size = 4
                    leaf_x = center_x + (radius - 2)
                    leaf_y = body_center_y - (radius - 2)
                    pygame.draw.ellipse(surface, PVZ_DARK_GREEN, 
                                       pygame.Rect(leaf_x, leaf_y, leaf_size*2, leaf_size))

class Food:
    """食物类，负责食物的生成和绘制 - PvZ阳光风格"""
    
    def __init__(self):
        """初始化食物"""
        self.position = (0, 0)  # 食物位置
        self.animation_offset = 0  # 动画偏移量
        self.spawn()  # 生成新食物
        
    def spawn(self):
        """随机生成新的食物位置"""
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
        # 重置动画
        self.animation_offset = 0
    
    def update_animation(self):
        """更新食物的动画效果"""
        self.animation_offset = (self.animation_offset + 0.1) % 6.28  # 2π
    
    def draw(self, surface):
        """在屏幕上绘制食物 - PvZ阳光风格"""
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
        
        # 更新动画
        self.update_animation()

def draw_grid(surface):
    """绘制PvZ风格的网格线"""
    # 在PvZ风格的背景上，网格线只需要轻微可见
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, (0, 0, 0, 30), (x, 0), (x, WINDOW_HEIGHT), 1)
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, (0, 0, 0, 30), (0, y), (WINDOW_WIDTH, y), 1)

def show_score(surface, score):
    """显示当前分数 - PvZ风格"""
    # 创建分数背景图案（类似PvZ的信息栏）
    score_bg = pygame.Rect(10, 10, 160, 40)
    pygame.draw.rect(surface, (0, 0, 0, 128), score_bg, border_radius=10)
    pygame.draw.rect(surface, PVZ_DARK_GREEN, score_bg, 2, border_radius=10)

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
    score_text = font.render(f'阳光: {score}', True, WHITE)
    surface.blit(score_text, (50, 15))

def show_start_screen(surface):
    """显示游戏开始界面 - PvZ风格"""
    # 绘制PvZ风格的草坪背景
    draw_pvz_background(surface)
    
    # 添加PvZ风格的阳光装饰
    for _ in range(8):  # 添加几个随机位置的阳光装饰
        sun_x = random.randint(50, WINDOW_WIDTH - 50)
        sun_y = random.randint(50, WINDOW_HEIGHT - 50)
        sun_radius = random.randint(15, 25)
        
        # 主体阳光
        pygame.draw.circle(surface, PVZ_SUN_YELLOW, (sun_x, sun_y), sun_radius)
        
        # 光芒
        ray_length = sun_radius + 4
        for angle in range(0, 360, 45):
            rad_angle = math.radians(angle)
            end_x = sun_x + math.cos(rad_angle) * ray_length
            end_y = sun_y + math.sin(rad_angle) * ray_length
            pygame.draw.line(surface, PVZ_SUN_YELLOW, (sun_x, sun_y), 
                           (end_x, end_y), 2)
    
    # 添加PvZ风格的标题背景板
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
    title_text = title_font.render('植物大战僵尸风格', True, WHITE)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4 - 10))
    surface.blit(title_text, title_rect)
    
    subtitle_text = title_font.render('贪吃蛇游戏', True, WHITE)
    subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4 + 50))
    surface.blit(subtitle_text, subtitle_rect)
    
    # 绘制操作说明背景
    instructions_bg = pygame.Rect(
        (WINDOW_WIDTH - 500) // 2,
        WINDOW_HEIGHT // 2 - 20,
        500,
        250
    )
    pygame.draw.rect(surface, (0, 0, 0, 160), instructions_bg, border_radius=15)
    pygame.draw.rect(surface, PVZ_DARK_GREEN, instructions_bg, 3, border_radius=15)
    
    # 绘制操作说明
    instructions = [
        '游戏说明:',
        '用方向键控制豌豆射手移动',
        '收集阳光可以得分并变长',
        '撞到自己会导致游戏结束',
        '',
        '按回车键开始游戏',
        '按ESC键退出游戏'
    ]
    
    for i, instruction in enumerate(instructions):
        if i == 0:  # 标题使用较大字体
            instruction_text = font.render(instruction, True, PVZ_LIGHT_GREEN)
        else:
            instruction_text = subtitle_font.render(instruction, True, WHITE)
        instruction_rect = instruction_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 35)
        )
        surface.blit(instruction_text, instruction_rect)
    
    # 绘制闪烁的开始提示 - PvZ风格的按钮
    current_time = pygame.time.get_ticks()
    if (current_time // 500) % 2 == 0:  # 每500毫秒闪烁一次
        # 绘制PvZ风格的按钮
        start_button = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT - 100, 300, 60)
        pygame.draw.rect(surface, PVZ_GREEN, start_button, border_radius=15)
        pygame.draw.rect(surface, PVZ_DARK_GREEN, start_button, 3, border_radius=15)
        
        # 添加按钮文字
        start_text = font.render('按回车键开始游戏', True, WHITE)
        start_rect = start_text.get_rect(center=start_button.center)
        surface.blit(start_text, start_rect)
    
    # 绘制版本信息
    version_text = subtitle_font.render('版本: 2.0 PvZ风格', True, (150, 150, 150))
    version_rect = version_text.get_rect(bottomright=(WINDOW_WIDTH - 10, WINDOW_HEIGHT - 10))
    surface.blit(version_text, version_rect)
    
    pygame.display.update()
    
    # 等待玩家按下回车键开始游戏或ESC键退出游戏
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # 回车键开始游戏
                    waiting = False
                elif event.key == pygame.K_ESCAPE:  # ESC键退出游戏
                    pygame.quit()
                    sys.exit()
        
        # 重新绘制闪烁文本
        current_time = pygame.time.get_ticks()
        if (current_time // 500) % 2 == 0:
            # 绘制PvZ风格的按钮
            start_button = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT - 100, 300, 60)
            pygame.draw.rect(surface, PVZ_GREEN, start_button, border_radius=15)
            pygame.draw.rect(surface, PVZ_DARK_GREEN, start_button, 3, border_radius=15)
            
            # 添加按钮文字
            start_text = font.render('按回车键开始游戏', True, WHITE)
            start_rect = start_text.get_rect(center=start_button.center)
            surface.blit(start_text, start_rect)
        else:
            # 清除按钮区域
            pygame.draw.rect(surface, PVZ_SKY_BLUE, 
                           pygame.Rect(WINDOW_WIDTH // 2 - 160, WINDOW_HEIGHT - 110, 320, 80))
            # 重新绘制该区域的背景
            for y in range(WINDOW_HEIGHT - 110, WINDOW_HEIGHT - 30, GRID_SIZE):
                for x in range(WINDOW_WIDTH // 2 - 160, WINDOW_WIDTH // 2 + 160, GRID_SIZE):
                    grid_x = x // GRID_SIZE
                    grid_y = y // GRID_SIZE
                    if (grid_x + grid_y) % 2 == 0:
                        color = PVZ_GREEN
                    else:
                        color = PVZ_LIGHT_GREEN
                    
                    rect_x = max(x, WINDOW_WIDTH // 2 - 160)
                    rect_y = max(y, WINDOW_HEIGHT - 110)
                    rect_width = min(GRID_SIZE, WINDOW_WIDTH // 2 + 160 - rect_x)
                    rect_height = min(GRID_SIZE, WINDOW_HEIGHT - 30 - rect_y)
                    
                    pygame.draw.rect(surface, color, pygame.Rect(
                        rect_x, rect_y, rect_width, rect_height
                    ))
        
        pygame.display.update(pygame.Rect(WINDOW_WIDTH // 2 - 160, WINDOW_HEIGHT - 110, 320, 80))
        clock.tick(GAME_SPEED)

def show_game_over(surface, score):
    """显示游戏结束画面 - PvZ风格"""
    # 绘制半透明的黑色背景
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    
    # 绘制PvZ风格的坟墓图像
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
    for i in range(5):
        crack_x = grave_x + random.randint(20, grave_width - 40)
        crack_y = grave_y + random.randint(20, grave_height - 90)
        crack_length = random.randint(10, 30)
        crack_angle = random.randint(0, 360)
        end_x = crack_x + math.cos(math.radians(crack_angle)) * crack_length
        end_y = crack_y + math.sin(math.radians(crack_angle)) * crack_length
        pygame.draw.line(surface, (100, 100, 100), (crack_x, crack_y), (end_x, end_y), 2)
    
    # 绘制游戏结束文本
    game_over_text = title_font.render('游戏结束!', True, PVZ_CHERRY_RED)
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
                       (skull_x - mouth_width//2 + i*mouth_width//2, skull_y + skull_radius//2),
                       2)
    
    # 绘制分数文本
    score_text = font.render(f'最终阳光数: {score}', True, WHITE)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, grave_y + 180))
    surface.blit(score_text, score_rect)
    
    # 绘制重新开始和退出按钮
    restart_button = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 130, 300, 50)
    exit_button = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 200, 300, 50)
    
    # PvZ风格的按钮
    pygame.draw.rect(surface, PVZ_GREEN, restart_button, border_radius=10)
    pygame.draw.rect(surface, PVZ_DARK_GREEN, restart_button, 3, border_radius=10)
    
    pygame.draw.rect(surface, PVZ_CHERRY_RED, exit_button, border_radius=10)
    pygame.draw.rect(surface, (150, 0, 0), exit_button, 3, border_radius=10)
    
    # 绘制按钮文本
    restart_text = font.render('重新开始 (回车)', True, WHITE)
    exit_text = font.render('退出游戏 (ESC)', True, WHITE)
    
    restart_text_rect = restart_text.get_rect(center=restart_button.center)
    exit_text_rect = exit_text.get_rect(center=exit_button.center)
    
    surface.blit(restart_text, restart_text_rect)
    surface.blit(exit_text, exit_text_rect)
    
    pygame.display.update()
    
    # 等待玩家按下回车键重新开始或ESC键退出游戏
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):  # 回车键或空格键重新开始
                    return True
                elif event.key == pygame.K_ESCAPE:  # ESC键退出游戏
                    pygame.quit()
                    sys.exit()
            # 鼠标点击按钮
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    return True
                elif exit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        clock.tick(GAME_SPEED)

def pause_game(surface):
    """暂停游戏 - PvZ风格"""
    # 绘制半透明的背景
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    
    # 创建暂停菜单背景
    menu_width = 400
    menu_height = 200
    menu_rect = pygame.Rect(
        (WINDOW_WIDTH - menu_width) // 2,
        (WINDOW_HEIGHT - menu_height) // 2,
        menu_width,
        menu_height
    )
    
    # 绘制木质标志牌风格的背景
    pygame.draw.rect(surface, PVZ_BROWN, menu_rect, border_radius=15)
    pygame.draw.rect(surface, (101, 67, 33), menu_rect, 4, border_radius=15)
    
    # 添加木纹细节
    for i in range(3):
        wood_line_y = menu_rect.top + 30 + i * 45
        pygame.draw.line(surface, (101, 67, 33), 
                       (menu_rect.left + 20, wood_line_y),
                       (menu_rect.right - 20, wood_line_y),
                       2)
    
    # 绘制暂停标题
    pause_title = font.render('游戏已暂停', True, WHITE)
    pause_title_rect = pause_title.get_rect(center=(WINDOW_WIDTH // 2, menu_rect.top + 50))
    surface.blit(pause_title, pause_title_rect)
    
    # 绘制继续游戏提示
    continue_text = font.render('按空格键继续游戏', True, WHITE)
    continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH // 2, menu_rect.top + 120))
    surface.blit(continue_text, continue_rect)
    
    pygame.display.update()
    
    # 等待玩家按下空格键
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        clock.tick(GAME_SPEED)

def run_game():
    """运行游戏主循环"""
    # 显示开始界面
    show_start_screen(window)
    
    # 初始化游戏
    snake = Snake()  # 创建蛇对象
    food = Food()    # 创建食物对象
    score = 0        # 初始化分数
    game_over = False  # 游戏是否结束的标志
    
    # 游戏主循环
    while True:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # 关闭窗口
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:  # 按键事件
                if event.key == pygame.K_ESCAPE:  # ESC键退出游戏
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE:  # 空格键暂停/继续游戏
                    if not game_over:
                        # 暂停游戏
                        pause_game(window)
                elif not game_over:  # 游戏进行中才处理方向键
                    if event.key == pygame.K_UP:
                        snake.update_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.update_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.update_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.update_direction(RIGHT)
        
        if not game_over:
            # 绘制PvZ风格背景
            draw_pvz_background(window)
            
            # 绘制网格和装饰
            draw_grid(window)
            
            # 移动蛇
            game_over = snake.move()
            
            # 检查是否吃到食物
            if snake.get_head_position() == food.position:
                snake.grow()       # 蛇生长
                food.spawn()       # 生成新食物
                score += 10        # 增加分数
                
                # 确保食物不会出现在蛇身上
                while food.position in snake.positions:
                    food.spawn()
            
            # 绘制蛇和食物
            snake.draw(window)
            food.draw(window)
            
            # 显示分数
            show_score(window, score)
            
            # 更新屏幕
            pygame.display.update()
        
        # 如果游戏结束，显示游戏结束画面
        if game_over:
            restart = show_game_over(window, score)
            if restart:
                return run_game()  # 重新开始游戏
        
        # 控制游戏速度
        clock.tick(GAME_SPEED)

# 启动游戏
if __name__ == "__main__":
    run_game() 