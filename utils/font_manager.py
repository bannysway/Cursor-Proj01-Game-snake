"""
字体管理器
用于加载和管理游戏中使用的字体
"""

import os
import pygame
from config import FONTS_DIR, FONT_SIZES

class FontManager:
    """
    字体管理器类
    负责加载和管理游戏中使用的字体
    """
    
    def __init__(self):
        """初始化字体管理器"""
        self.fonts = {}  # 存储已加载的字体 {(font_name, size, bold): font_obj}
        pygame.font.init()  # 确保pygame字体模块已初始化
        
        # 尝试找到系统中可用的中文字体
        self.system_font = self._find_chinese_font()
        
        # 加载预设大小的默认字体
        self.small_font = self.get_font(self.system_font, FONT_SIZES["small"])
        self.medium_font = self.get_font(self.system_font, FONT_SIZES["medium"])
        self.large_font = self.get_font(self.system_font, FONT_SIZES["large"], bold=True)
    
    def _find_chinese_font(self):
        """
        在系统中查找支持中文的字体
        返回找到的字体名称或默认字体路径
        """
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
        for chinese_font in chinese_fonts:
            if chinese_font.lower() in available_fonts:
                print(f"使用中文字体: {chinese_font}")
                return chinese_font
        
        # 如果没有找到系统字体，检查字体目录中是否有字体文件
        font_files = [f for f in os.listdir(FONTS_DIR) if f.endswith(('.ttf', '.ttc'))] if os.path.exists(FONTS_DIR) else []
        
        if font_files:
            font_path = os.path.join(FONTS_DIR, font_files[0])
            print(f"使用字体文件: {font_path}")
            return font_path
        
        # 最后尝试在Windows系统常见路径中查找字体文件
        font_paths = [
            "C:\\Windows\\Fonts\\simhei.ttf",  # 黑体
            "C:\\Windows\\Fonts\\msyh.ttc",    # 微软雅黑
            "C:\\Windows\\Fonts\\simsun.ttc",  # 宋体
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                print(f"使用系统字体文件: {font_path}")
                return font_path
        
        # 如果所有尝试都失败，返回None，将使用pygame默认字体
        print("未找到中文字体，使用默认字体")
        return None
    
    def get_font(self, font_name, size, bold=False):
        """
        获取指定名称和大小的字体
        如果字体已加载，则返回缓存的字体对象
        否则加载并缓存字体
        
        参数:
            font_name (str): 字体名称或路径
            size (int): 字体大小
            bold (bool): 是否粗体
        
        返回:
            pygame.font.Font: 字体对象
        """
        key = (font_name, size, bold)
        
        # 如果字体已经加载，直接返回
        if key in self.fonts:
            return self.fonts[key]
        
        try:
            # 如果是文件路径，直接加载字体文件
            if font_name and (os.path.isfile(font_name) or font_name.endswith(('.ttf', '.ttc'))):
                font = pygame.font.Font(font_name, size)
                if bold:
                    font.set_bold(True)
            # 否则使用系统字体
            elif font_name:
                font = pygame.font.SysFont(font_name, size, bold=bold)
            # 如果没有指定字体，使用默认字体
            else:
                default_font = pygame.font.get_default_font()
                font = pygame.font.Font(default_font, size)
                if bold:
                    font.set_bold(True)
            
            # 缓存字体
            self.fonts[key] = font
            return font
        
        except Exception as e:
            print(f"加载字体错误: {e}")
            # 出错时使用备用字体
            fallback_font = pygame.font.Font(None, size)  # None表示默认字体
            self.fonts[key] = fallback_font
            return fallback_font
    
    def render_text(self, text, font, color, antialias=True):
        """
        渲染文本
        
        参数:
            text (str): 要渲染的文本
            font (pygame.font.Font): 使用的字体
            color (tuple): RGB颜色值
            antialias (bool): 是否使用抗锯齿
        
        返回:
            pygame.Surface: 渲染后的文本表面
        """
        try:
            return font.render(text, antialias, color)
        except Exception as e:
            print(f"渲染文本错误: {e}")
            # 尝试使用默认字体渲染
            fallback_font = pygame.font.Font(None, font.get_height())
            return fallback_font.render(text, antialias, color)

# 创建全局字体管理器实例
font_manager = None

def init_font_manager():
    """初始化全局字体管理器"""
    global font_manager
    font_manager = FontManager()
    return font_manager

def get_font_manager():
    """获取全局字体管理器实例"""
    global font_manager
    if font_manager is None:
        font_manager = FontManager()
    return font_manager 