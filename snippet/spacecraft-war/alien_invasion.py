import sys
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
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

        # 创建用于存储游戏统计信息的实例
        self.stats = GameStats(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()  # 存储编组，存储子弹，类似列表
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_aliens()
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

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""
        # 删除发生碰撞的子弹和外星人
        # sprite.groupcollide：将一个编组中每个元素的 rect 同另个编组中每个元素的 rect 比较
        # 返回字典添加键值对，实参 True，让pygame删除发生碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if not self.aliens:  # 检查编组是否为空
            # 删除现有子弹并新建一群外星人
            self.bullets.empty()  # 删除编组余下的 spirit
            self._create_fleet()  # 在屏幕上重新显示一群外星人

    def _create_fleet(self):
        """创建外星人群"""
        # 创建外星人并计算一行可容纳多少外星人
        # 外星人间距为外星人宽度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        # 确定一行容纳数量
        # 可用于放置的水平空间 = 屏幕宽度 - 外星人宽度 * 2
        available_space_x = self.settings.screen_width - (2 * alien_width)
        # 显示外星人所需的水平空间为 外星人宽度 * 2
        # 一行数量 = 可用空间 // 外星人所需的水平空间
        number_aliens_x = available_space_x // (2 * alien_width)

        # 计算屏幕可容纳多少行外星人
        ship_height = self.ship.rect.height
        # 可用垂直空间 = 屏幕宽度 - 第一行的上边距（高度）、飞船高度、外星人群最初与飞船之间的距离（外星人高度两倍）
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        # 可容纳行数 = 可用垂直空间 // 外星人高度的两倍
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建外星人，并将其放在当前行"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应措施"""
        for alien in self.aliens.sprites():  # 遍历并调用方法，当返回True表明相应外星人位于屏幕边缘
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群下移并改变方向"""
        for alien in self.aliens.sprites():  # 遍历所有外星人，将每个外星人下移设置值（当前值与 -1 的乘积）
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """响应飞船被外星人撞到的响应"""

        # 将 ships_left 减 1
        self.stats.ships_left -= 1

        # 清空余下外星人和子弹
        self.aliens.empty()
        self.bullets.empty()

        # 创建新的外星人群，并将飞船放到屏幕底端中央
        self._create_fleet()
        self.ship.center_ship()

        # 暂停
        sleep(0.5)

    def _update_aliens(self):
        """
        检查是否有外星人位于屏幕边缘，
        并更新整群外星人位置
        """
        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船之间的碰撞
        # sprite.spritecollideany：接受两个实参（sprite, group）
        # 检查编组是否有成员与 sprite 发生碰撞，并在找到与 sprite 发生碰撞的成员后停止遍历编组
        # 没有碰撞返回 None，if代码不执行
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检查是否有外星人到达屏幕底端
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达屏幕底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            # 判断外星人的rect.bottom大于或等于屏幕的rect.bottom
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理
                self._ship_hit()
                break

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
