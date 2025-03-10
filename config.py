"""
贪吃蛇游戏配置文件
包含所有游戏常量、颜色设置和游戏参数
"""

import os

# 路径配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")

# 窗口设置
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "植物大战僵尸风格贪吃蛇"
FPS = 60

# 游戏设置
GRID_SIZE = 30
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE
GAME_SPEED = 10  # 较低的值表示较慢的蛇移动速度

# 颜色设置 - 植物大战僵尸风格
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PVZ_GREEN = (87, 183, 59)        # PVZ风格草地绿
PVZ_DARK_GREEN = (58, 121, 39)   # PVZ深绿色
PVZ_LIGHT_GREEN = (129, 212, 75) # PVZ浅绿色
PVZ_BROWN = (145, 102, 39)       # PVZ土壤棕色
PVZ_SKY_BLUE = (157, 209, 255)   # PVZ天空蓝
PVZ_SUN_YELLOW = (250, 233, 80)  # PVZ阳光黄
PVZ_CHERRY_RED = (255, 68, 68)   # PVZ樱桃炸弹红
PVZ_BLUE = (60, 160, 255)        # PVZ蓝色

# 方向常量
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# 食物设置
FOOD_TYPES = {
    "sun": {
        "weight": 70,  # 生成权重
        "score": 10,   # 得分
        "effect": None # 特殊效果
    },
    "sunflower": {
        "weight": 20,
        "score": 20,
        "effect": None
    },
    "walnut": {
        "weight": 10,
        "score": 5,
        "effect": "shield"
    }
}

# 障碍物设置
OBSTACLE_TYPES = {
    "zombie": {
        "speed": 0.5,   # 移动速度
        "damage": 1     # 造成的伤害
    },
    "tombstone": {
        "speed": 0,     # 静止障碍物
        "damage": 1
    }
}

# 场景设置
SCENES = {
    "day": {
        "background": PVZ_SKY_BLUE,
        "grid_colors": [PVZ_GREEN, PVZ_LIGHT_GREEN],
        "special_rules": None
    },
    "night": {
        "background": (30, 30, 60),
        "grid_colors": [(30, 80, 30), (20, 60, 20)],
        "special_rules": "reduced_visibility"
    },
    "pool": {
        "background": (100, 180, 255),
        "grid_colors": [PVZ_GREEN, PVZ_LIGHT_GREEN],
        "special_rules": "water_tiles"
    }
}

# 音频设置
SOUNDS = {
    "background_music": "simple_background.wav",
    "eat_food": "eat_food.wav",
    "game_over": "game_over.wav",
    "menu_click": "menu_click.wav",
    "ability_activated": "ability_activated.wav",
    "zombie_groan": "zombie_groan.wav"
}

# 特殊能力设置
ABILITIES = {
    "shield": {
        "duration": 100,  # 持续时间(帧数)
        "effect": "invincible"
    },
    "speed_up": {
        "duration": 150,
        "effect": "increase_speed"
    }
}

# 字体设置
FONT_SIZES = {
    "small": 24,
    "medium": 30,
    "large": 60
}

# 游戏难度设置
DIFFICULTY_LEVELS = {
    "easy": {
        "speed": 8,
        "obstacle_frequency": 0.01
    },
    "medium": {
        "speed": 10,
        "obstacle_frequency": 0.02
    },
    "hard": {
        "speed": 12,
        "obstacle_frequency": 0.03
    }
}

# 默认游戏设置
DEFAULT_SETTINGS = {
    "difficulty": "medium",
    "scene": "day",
    "music_volume": 0.7,
    "sfx_volume": 1.0
} 