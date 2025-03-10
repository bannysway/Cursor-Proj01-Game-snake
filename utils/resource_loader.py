"""
资源加载器
用于加载和管理游戏中使用的音频和图像资源
"""

import os
import pygame
from config import (
    SOUNDS_DIR, SOUNDS, IMAGES_DIR, IMAGES, 
    SNAKE_IMAGES_DIR, FOOD_IMAGES_DIR, OBSTACLES_IMAGES_DIR, 
    BACKGROUNDS_IMAGES_DIR, UI_IMAGES_DIR
)

class ResourceLoader:
    """
    资源加载器类
    负责加载和管理游戏中使用的音频和图像资源
    """
    
    def __init__(self):
        """初始化资源加载器"""
        self.sounds = {}  # 存储已加载的音效 {name: sound_obj}
        self.images = {}  # 存储已加载的图像 {name: image_obj}
        self.music = None  # 当前加载的背景音乐
        self.music_volume = 0.7  # 背景音乐音量
        self.sfx_volume = 1.0    # 音效音量
        self.game_engine = None  # 游戏引擎引用，将在游戏引擎初始化时设置
        
        # 确保pygame混音器已初始化
        if not pygame.mixer.get_init():
            pygame.mixer.init()
            
        # 确保pygame显示模块已初始化
        if not pygame.display.get_surface():
            pygame.display.init()
        
        # 加载预设音效
        self._preload_sounds()
        
        # 加载背景音乐
        if "background_music" in SOUNDS:
            self.load_music(SOUNDS["background_music"])
    
    def set_game_engine(self, game_engine):
        """
        设置游戏引擎引用
        
        参数:
            game_engine: 游戏引擎实例
        """
        self.game_engine = game_engine
    
    def load_sounds(self):
        """加载所有预设音效和背景音乐"""
        # 加载预设音效
        for sound_name, sound_file in SOUNDS.items():
            if sound_name != "background_music":  # 背景音乐单独处理
                self.load_sound(sound_name, sound_file)
        
        # 加载背景音乐
        if "background_music" in SOUNDS:
            self.load_music(SOUNDS["background_music"])
    
    def _preload_sounds(self):
        """预加载常用音效"""
        for sound_name, sound_file in SOUNDS.items():
            if sound_name != "background_music":  # 背景音乐单独处理
                self.load_sound(sound_name, sound_file)
    
    def load_sound(self, name, filename):
        """
        加载音效
        
        参数:
            name: 音效名称
            filename: 音效文件名
        
        返回:
            加载的音效对象
        """
        try:
            sound_path = os.path.join(SOUNDS_DIR, filename)
            if os.path.exists(sound_path):
                sound = pygame.mixer.Sound(sound_path)
                sound.set_volume(self.sfx_volume)
                self.sounds[name] = sound
                return sound
            else:
                print(f"警告: 音效文件 {sound_path} 不存在")
                return None
        except Exception as e:
            print(f"加载音效 {name} 时出错: {e}")
            return None
    
    def load_image(self, name, directory=None, scale=None, convert_alpha=True):
        """
        加载图像
        
        参数:
            name: 图像名称或文件名
            directory: 图像所在目录，如果为None则根据图像名称自动选择目录
            scale: 缩放比例，如果为None则不缩放
            convert_alpha: 是否转换alpha通道
            
        返回:
            加载的图像对象
        """
        # 如果图像已加载，直接返回
        if name in self.images:
            return self.images[name]
            
        try:
            # 确定图像文件路径
            if directory is None:
                # 根据图像名称自动选择目录
                if name.startswith("snake_"):
                    directory = SNAKE_IMAGES_DIR
                elif name.startswith(("sun", "sunflower", "walnut", "peashooter")):
                    directory = FOOD_IMAGES_DIR
                elif name.startswith(("zombie", "tombstone")):
                    directory = OBSTACLES_IMAGES_DIR
                elif name.endswith("_background"):
                    directory = BACKGROUNDS_IMAGES_DIR
                elif name.startswith(("button", "menu", "game_over", "icon")):
                    directory = UI_IMAGES_DIR
                else:
                    directory = IMAGES_DIR
            
            # 如果name是IMAGES中的键，获取对应的文件名
            if name in IMAGES:
                filename = IMAGES[name]
            else:
                filename = name  # 否则直接使用name作为文件名
                
            image_path = os.path.join(directory, filename)
            
            # 检查文件是否存在
            if not os.path.exists(image_path):
                print(f"警告: 图像文件 {image_path} 不存在")
                return None
                
            # 加载图像
            if convert_alpha:
                image = pygame.image.load(image_path).convert_alpha()
            else:
                image = pygame.image.load(image_path).convert()
                
            # 缩放图像
            if scale:
                original_size = image.get_size()
                new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                image = pygame.transform.scale(image, new_size)
                
            # 存储并返回图像
            self.images[name] = image
            return image
            
        except Exception as e:
            print(f"加载图像 {name} 时出错: {e}")
            return None
    
    def get_image(self, name):
        """
        获取已加载的图像
        
        参数:
            name: 图像名称
            
        返回:
            图像对象，如果不存在则返回None
        """
        return self.images.get(name)
    
    def play_sound(self, name):
        """
        播放音效
        
        参数:
            name: 音效名称
        """
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"警告: 音效 {name} 未加载")
    
    def load_music(self, filename):
        """
        加载背景音乐
        
        参数:
            filename: 音乐文件名
        """
        try:
            music_path = os.path.join(SOUNDS_DIR, filename)
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(self.music_volume)
                self.music = filename
            else:
                print(f"警告: 音乐文件 {music_path} 不存在")
        except Exception as e:
            print(f"加载音乐 {filename} 时出错: {e}")
    
    def play_music(self, loops=-1):
        """
        播放背景音乐
        
        参数:
            loops: 循环次数，-1表示无限循环
        """
        if self.music:
            pygame.mixer.music.play(loops)
        else:
            print("警告: 没有加载背景音乐")
    
    def stop_music(self):
        """停止背景音乐"""
        pygame.mixer.music.stop()
    
    def pause_music(self):
        """暂停背景音乐"""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """恢复背景音乐"""
        pygame.mixer.music.unpause()
    
    def set_music_volume(self, volume):
        """
        设置背景音乐音量
        
        参数:
            volume: 音量值，范围0.0-1.0
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        """
        设置音效音量
        
        参数:
            volume: 音量值，范围0.0-1.0
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def create_sprite_sheet(self, image, sprite_width, sprite_height):
        """
        从精灵表中提取精灵图像
        
        参数:
            image: 精灵表图像
            sprite_width: 单个精灵宽度
            sprite_height: 单个精灵高度
            
        返回:
            精灵图像列表
        """
        sprites = []
        image_width, image_height = image.get_size()
        
        for y in range(0, image_height, sprite_height):
            for x in range(0, image_width, sprite_width):
                sprite = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
                sprite.blit(image, (0, 0), (x, y, sprite_width, sprite_height))
                sprites.append(sprite)
                
        return sprites

# 单例模式
_resource_loader = None

def init_resource_loader():
    """初始化资源加载器"""
    global _resource_loader
    _resource_loader = ResourceLoader()
    return _resource_loader

def get_resource_loader():
    """获取资源加载器实例"""
    global _resource_loader
    if _resource_loader is None:
        _resource_loader = ResourceLoader()
    return _resource_loader 