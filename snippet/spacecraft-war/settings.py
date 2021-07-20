class Settings:
    """存储所有设置的类"""

    def __init__(self):
        """初始化游戏设置"""
        # 游戏难度
        self.easy = True
        self.normal = False
        self.hard = False

        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = '#66ccff'

        # 飞船设置
        self.ship_limit = 3

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # 外星人设置
        self.fleet_drop_speed = 10

        # 加快节奏速度
        self.speedup_scale = 1.1

        # self.initialize_dynamic_settings() # 省略初始化，在开始时选择难度

    def initialize_dynamic_settings(self):
        """
        初始化随游戏进行所变化的设置
        根据游戏不同等级难度初始化
        """
        if self.easy:
            self._easy_settings()
        elif self.normal:
            self._normal_settings()
        elif self.hard:
            self._hard_settings()

    def _easy_settings(self):
        """容易难度设置"""
        self.ship_speed = 0.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.5

        # fleet_direction 为 1 表示右移，-1 为向左移
        self.fleet_direction = 0.5

    def _normal_settings(self):
        """正常难度设置"""
        self.ship_speed = 1.0
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction 为 1 表示右移，-1 为向左移
        self.fleet_direction = 1.0

    def _hard_settings(self):
        """困难难度设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # fleet_direction 为 1 表示右移，-1 为向左移
        self.fleet_direction = 1.5

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
