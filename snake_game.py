"""
贪吃蛇游戏 - Snake Game
一个简单的贪吃蛇游戏，使用Python和Pygame库开发。

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

# 初始化Pygame
pygame.init()

# 定义颜色（RGB值）
BLACK = (0, 0, 0)         # 黑色 - 背景
WHITE = (255, 255, 255)   # 白色 - 网格线
GREEN = (0, 255, 0)       # 绿色 - 蛇
RED = (255, 0, 0)         # 红色 - 食物
BLUE = (0, 0, 255)        # 蓝色 - 分数显示
YELLOW = (255, 255, 0)    # 黄色 - 标题

# 游戏设置
WINDOW_WIDTH = 800        # 窗口宽度
WINDOW_HEIGHT = 600       # 窗口高度
GRID_SIZE = 20            # 网格大小
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
pygame.display.set_caption('贪吃蛇游戏')  # 设置窗口标题

# 创建时钟对象（用于控制游戏帧率）
clock = pygame.time.Clock()

# 定义字体
font = pygame.font.SysFont('simhei', 30)  # 使用黑体，大小30
title_font = pygame.font.SysFont('simhei', 60, bold=True)  # 使用黑体，大小60，加粗
subtitle_font = pygame.font.SysFont('simhei', 24)  # 使用黑体，大小24

class Snake:
    """蛇类，负责蛇的移动、生长和碰撞检测"""
    
    def __init__(self):
        """初始化蛇"""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  # 蛇的位置，初始在屏幕中央
        self.direction = RIGHT  # 初始方向向右
        self.next_direction = RIGHT  # 下一步的方向
        self.grew = False  # 是否刚吃了食物需要生长
    
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
            
        return False  # 游戏继续
    
    def grow(self):
        """蛇吃到食物后生长"""
        self.grew = True
    
    def draw(self, surface):
        """在屏幕上绘制蛇"""
        for i, position in enumerate(self.positions):
            # 计算蛇身体每一节的矩形位置
            rect = pygame.Rect(
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE,
                GRID_SIZE, GRID_SIZE
            )
            
            # 绘制蛇的身体，头部颜色深一些
            if i == 0:  # 蛇头
                pygame.draw.rect(surface, (0, 200, 0), rect)  # 深绿色
            else:  # 蛇身
                pygame.draw.rect(surface, GREEN, rect)
                
            # 添加内部边框，使蛇的每一节看起来更清晰
            pygame.draw.rect(surface, (0, 150, 0), rect, 1)

class Food:
    """食物类，负责食物的生成和绘制"""
    
    def __init__(self):
        """初始化食物"""
        self.position = (0, 0)  # 食物位置
        self.spawn()  # 生成新食物
        
    def spawn(self):
        """随机生成新的食物位置"""
        self.position = (
            random.randint(0, GRID_WIDTH - 1),
            random.randint(0, GRID_HEIGHT - 1)
        )
    
    def draw(self, surface):
        """在屏幕上绘制食物"""
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        # 绘制食物（红色小圆点）
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, (150, 0, 0), rect, 1)  # 添加深红色边框

def draw_grid(surface):
    """绘制网格线"""
    # 绘制竖线
    for x in range(0, WINDOW_WIDTH, GRID_SIZE):
        pygame.draw.line(surface, (50, 50, 50), (x, 0), (x, WINDOW_HEIGHT))
    # 绘制横线
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, (50, 50, 50), (0, y), (WINDOW_WIDTH, y))

def show_score(surface, score):
    """显示当前分数"""
    score_text = font.render(f'分数: {score}', True, BLUE)
    surface.blit(score_text, (10, 10))

def show_start_screen(surface):
    """显示游戏开始界面"""
    # 绘制渐变背景
    for i in range(60):
        color_value = min(255, i * 4)
        pygame.draw.rect(surface, (0, color_value // 3, color_value // 2), 
                        pygame.Rect(0, i * 10, WINDOW_WIDTH, 10))
    
    # 绘制游戏标题
    title_text = title_font.render('贪吃蛇游戏', True, YELLOW)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    surface.blit(title_text, title_rect)
    
    # 绘制游戏副标题
    subtitle_text = subtitle_font.render('经典游戏，简单有趣', True, WHITE)
    subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 70))
    surface.blit(subtitle_text, subtitle_rect)
    
    # 绘制操作说明
    instructions = [
        '游戏说明:',
        '用方向键控制蛇的移动',
        '吃到食物可以得分并变长',
        '撞到自己会导致游戏结束',
        '',
        '按回车键开始游戏',
        '按ESC键退出游戏'
    ]
    
    for i, instruction in enumerate(instructions):
        if i == 0:  # 标题使用较大字体
            instruction_text = font.render(instruction, True, GREEN)
        else:
            instruction_text = subtitle_font.render(instruction, True, WHITE)
        instruction_rect = instruction_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + i * 35)
        )
        surface.blit(instruction_text, instruction_rect)
    
    # 绘制闪烁的开始提示
    current_time = pygame.time.get_ticks()
    if (current_time // 500) % 2 == 0:  # 每500毫秒闪烁一次
        start_text = font.render('按回车键开始游戏', True, YELLOW)
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
        surface.blit(start_text, start_rect)
    
    # 绘制版本信息
    version_text = subtitle_font.render('版本: 1.1', True, (100, 100, 100))
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
            surface.fill((0, 0, 0), (0, WINDOW_HEIGHT - 130, WINDOW_WIDTH, 60))
            start_text = font.render('按回车键开始游戏', True, YELLOW)
            start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
            surface.blit(start_text, start_rect)
            pygame.display.update((0, WINDOW_HEIGHT - 130, WINDOW_WIDTH, 60))
        else:
            surface.fill((0, 0, 0), (0, WINDOW_HEIGHT - 130, WINDOW_WIDTH, 60))
            pygame.display.update((0, WINDOW_HEIGHT - 130, WINDOW_WIDTH, 60))
        
        clock.tick(GAME_SPEED)

def show_game_over(surface, score):
    """显示游戏结束画面"""
    # 绘制半透明的黑色背景
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    
    # 绘制游戏结束文本
    game_over_text = title_font.render('游戏结束!', True, RED)
    score_text = font.render(f'最终分数: {score}', True, WHITE)
    
    # 计算文本位置（居中）
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 80))
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    
    # 显示文本
    surface.blit(game_over_text, game_over_rect)
    surface.blit(score_text, score_rect)
    
    # 绘制重新开始和退出按钮
    restart_button = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 60, 300, 50)
    exit_button = pygame.Rect(WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 + 130, 300, 50)
    
    pygame.draw.rect(surface, (0, 100, 0), restart_button)
    pygame.draw.rect(surface, (100, 0, 0), exit_button)
    
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
    """暂停游戏"""
    # 绘制半透明的黑色背景
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
    overlay.set_alpha(100)
    overlay.fill(BLACK)
    surface.blit(overlay, (0, 0))
    
    # 绘制暂停文本
    pause_text = font.render('游戏已暂停，按空格键继续', True, WHITE)
    pause_rect = pause_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
    surface.blit(pause_text, pause_rect)
    
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
            # 清空屏幕
            window.fill(BLACK)
            
            # 绘制网格
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