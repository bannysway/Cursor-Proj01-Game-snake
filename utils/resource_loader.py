"""
资源加载器
用于加载和管理游戏中使用的音频和图像资源
"""

import os
import pygame
from config import SOUNDS_DIR, SOUNDS

class ResourceLoader:
    """
    资源加载器类
    负责加载和管理游戏中使用的音频和图像资源
    """
    
    def __init__(self):
        """初始化资源加载器"""
        self.sounds = {}  # 存储已加载的音效 {name: sound_obj}
        self.music = None  # 当前加载的背景音乐
        self.music_volume = 0.7  # 背景音乐音量
        self.sfx_volume = 1.0    # 音效音量
        
        # 确保pygame混音器已初始化
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # 加载预设音效
        self._preload_sounds()
        
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
            name (str): 音效名称
            filename (str): 音效文件名
        
        返回:
            pygame.mixer.Sound: 加载的音效对象，加载失败返回None
        """
        # 如果音效已加载，直接返回
        if name in self.sounds:
            return self.sounds[name]
        
        # 构建完整文件路径
        file_path = os.path.join(SOUNDS_DIR, filename)
        
        try:
            if os.path.exists(file_path):
                sound = pygame.mixer.Sound(file_path)
                sound.set_volume(self.sfx_volume)
                self.sounds[name] = sound
                print(f"已加载音效: {name}")
                return sound
            else:
                print(f"音效文件不存在: {file_path}")
                return None
        except Exception as e:
            print(f"加载音效错误: {e}")
            return None
    
    def play_sound(self, name):
        """
        播放音效
        
        参数:
            name (str): 音效名称
        """
        if name in self.sounds:
            self.sounds[name].play()
        else:
            print(f"未找到音效: {name}")
    
    def load_music(self, filename):
        """
        加载背景音乐
        
        参数:
            filename (str): 音乐文件名
        
        返回:
            bool: 加载是否成功
        """
        # 构建完整文件路径
        file_path = os.path.join(SOUNDS_DIR, filename)
        
        try:
            if os.path.exists(file_path):
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.set_volume(self.music_volume)
                self.music = filename
                print(f"已加载背景音乐: {filename}")
                return True
            else:
                print(f"背景音乐文件不存在: {file_path}")
                return False
        except Exception as e:
            print(f"加载背景音乐错误: {e}")
            return False
    
    def play_music(self, loops=-1):
        """
        播放背景音乐
        
        参数:
            loops (int): 循环次数，-1表示无限循环
        """
        if self.music:
            pygame.mixer.music.play(loops)
        else:
            print("未加载背景音乐")
    
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
            volume (float): 音量大小，范围0.0-1.0
        """
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def set_sfx_volume(self, volume):
        """
        设置音效音量
        
        参数:
            volume (float): 音量大小，范围0.0-1.0
        """
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

# 创建全局资源加载器实例
resource_loader = None

def init_resource_loader():
    """初始化全局资源加载器"""
    global resource_loader
    resource_loader = ResourceLoader()
    return resource_loader

def get_resource_loader():
    """获取全局资源加载器实例"""
    global resource_loader
    if resource_loader is None:
        resource_loader = ResourceLoader()
    return resource_loader 