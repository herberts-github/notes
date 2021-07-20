import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        # 全屏模式
        # self.screen = pygame.display.set_mode(
        #     (0,0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption('外星人入侵')

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  # 存储编组，存储子弹，类似列表
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def _create_fleet(self):
        """创建外星人群"""
        # 创建外星人并计算一行可容纳多少外星人
        # 外星人间距为外星人宽度
        alien = Alien(self)
        alien_width = alien.rect.width
        # 确定一行容纳数量
        # 可用于放置的水平空间 = 屏幕宽度 - 外星人宽度 * 2
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # 显示外星人所需的水平空间为 外星人宽度 * 2
        # 一行数量 = 可用空间 // 外星人所需的水平空间
        number_aliens_x = available_space_x // (2 * alien_width)

        # 创建第一行外星人
        for alien_number in range(number_aliens_x):
            # 创建一个并将其加入当前行
            alien = Alien(self)
            alien.x = alien_width + 2 * alien_width * alien_number
            alien.rect.x = alien.x
            self.aliens.add(alien)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self._update_bullets()
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件"""
        # 监视键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        """响应松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建子弹，并将其加入编组中"""
        if len(self.bullets) < self.settings.bullets_allowed:  # 检查长度，限制子弹
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹位置并删除消失的子弹"""
        # 更新子弹的位置
        self.bullets.update()

        # 删除消失的子弹
        for bullet in self.bullets.copy():  # 遍历编组副本，检查每颗子弹，是否从屏幕顶端消失将其删除
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """更新屏幕上的图像，并切换新屏幕"""
        # 每次循环时都重绘屏幕
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == '__main__':
    # 创建游戏实例并运行游戏
    ai = AlienInvasion()
    ai.run_game()
