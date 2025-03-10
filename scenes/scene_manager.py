"""
场景管理器
用于管理游戏中的不同场景
"""

import pygame
from scenes.base_scene import Scene
# 延迟导入具体场景类，避免循环导入
# 导入将在_register_scenes方法中进行

class SceneManager:
    """
    场景管理器类
    负责场景的注册、切换、更新和渲染
    """
    
    def __init__(self, game_engine):
        """初始化场景管理器"""
        self.game_engine = game_engine
        self.scenes = {}  # 场景字典 {name: scene_instance}
        self.current_scene = None  # 当前活跃场景
        self.current_scene_name = None  # 当前场景名称
        
        # 注册场景
        self._register_scenes()
    
    def start(self):
        """启动场景管理器，进入主菜单场景"""
        self.change_scene("menu")
    
    def _register_scenes(self):
        """注册所有游戏场景"""
        # 这里导入场景类，避免循环导入
        from scenes.menu_scene import MenuScene
        from scenes.game_scene import GameScene
        from scenes.game_over_scene import GameOverScene
        
        # 创建并注册场景实例
        self.register_scene("menu", MenuScene(self.game_engine))
        self.register_scene("game", GameScene(self.game_engine))
        self.register_scene("game_over", GameOverScene(self.game_engine))
    
    def register_scene(self, name, scene):
        """
        注册场景
        
        参数:
            name (str): 场景名称
            scene (Scene): 场景实例
        """
        if not isinstance(scene, Scene):
            raise TypeError(f"场景必须是Scene类型，而不是 {type(scene).__name__}")
        
        self.scenes[name] = scene
    
    def change_scene(self, scene_name, **kwargs):
        """
        切换到指定场景
        
        参数:
            scene_name (str): 场景名称
            **kwargs: 传递给新场景的参数
        """
        # 检查场景是否存在
        if scene_name not in self.scenes:
            raise ValueError(f"场景 '{scene_name}' 不存在")
        
        # 退出当前场景
        if self.current_scene:
            self.current_scene.exit()
        
        # 切换到新场景
        self.current_scene_name = scene_name
        self.current_scene = self.scenes[scene_name]
        
        # 进入新场景
        self.current_scene.enter(**kwargs)
    
    def handle_event(self, event):
        """
        处理事件
        
        参数:
            event (pygame.event.Event): Pygame事件对象
        """
        if self.current_scene:
            return self.current_scene.handle_event(event)
        return False
    
    def update(self, delta_time):
        """
        更新当前场景
        
        参数:
            delta_time (float): 帧间隔时间（秒）
        """
        if self.current_scene:
            self.current_scene.update(delta_time)
    
    def render(self, surface):
        """
        渲染当前场景
        
        参数:
            surface (pygame.Surface): 要渲染到的表面
        """
        if self.current_scene:
            self.current_scene.render(surface)
    
    def on_pause_changed(self, paused):
        """
        游戏暂停状态变化时调用
        
        参数:
            paused (bool): 游戏是否暂停
        """
        if self.current_scene:
            self.current_scene.on_pause_changed(paused) 