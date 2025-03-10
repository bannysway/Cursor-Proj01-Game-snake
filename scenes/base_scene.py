"""
基础场景类
定义场景的基本接口和共享功能
"""

class Scene:
    """
    基础场景类
    所有游戏场景都应继承此类并实现其方法
    """
    
    def __init__(self, game_engine):
        """初始化场景"""
        self.game_engine = game_engine
        self.window = game_engine.window
        self.font_manager = game_engine.font_manager
        self.resource_loader = game_engine.resource_loader
        self.ui_manager = game_engine.ui_manager
    
    def enter(self, **kwargs):
        """
        进入场景时调用
        可以接收来自前一个场景的参数
        """
        pass
    
    def exit(self):
        """退出场景时调用"""
        pass
    
    def update(self, delta_time):
        """
        更新场景状态
        
        参数:
            delta_time (float): 上一帧到这一帧的时间间隔（秒）
        """
        pass
    
    def render(self, surface):
        """
        渲染场景
        
        参数:
            surface (pygame.Surface): 要渲染到的表面
        """
        pass
    
    def handle_event(self, event):
        """
        处理事件
        
        参数:
            event (pygame.event.Event): Pygame事件对象
            
        返回:
            bool: 如果事件被处理，返回True
        """
        return False
    
    def on_pause_changed(self, paused):
        """
        游戏暂停状态变化时调用
        
        参数:
            paused (bool): 游戏是否暂停
        """
        pass 