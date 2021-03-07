import random
from settings import *


class Player(pygame.sprite.Sprite):
    """Player class"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.grouping)
        self.grouping = None
        self.speed = 5  # moving speed
        self.reload = 10  # bullet reload time
        self.image = load_image("player.png")
        self.rect = self.image.get_rect()
        self.rect.bottom = SCR_RECT.bottom  # player bottom at bottom of screen
        self.reload_count = 0

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        self.rect.clamp_ip(SCR_RECT)

        if pressed_keys[K_SPACE]:
            if self.reload_count > 0:
                self.reload_count -= 1
            else:
                Bullet(self.rect.center)  # create bullet at center of player
                self.reload_count = self.reload
                load_sound("shot.wav").play()


class Enemy(pygame.sprite.Sprite):
    """Enemy class"""
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.grouping)
        self.grouping = None
        self.speed = 2  # moving speed of enemy
        self.anime_frame = 18  # animation frame
        self.frame = 0
        self.move_width = 250  # move left and right
        self.attack_probability = 0.005  # random attack by enemy
        self.images = split_image(load_image("enemy.png"), 2)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.left = position[0]
        self.right = self.left + self.move_width

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if self.rect.center[0] < self.left or self.rect.center[0] > self.right:
            self.speed = -self.speed  # change direction of move
        # enemy attack at random
        if self.attack_probability > random.random():
            Beam(self.rect.center)
        self.frame += 1
        self.image = self.images[(self.frame // self.anime_frame) % 2]


class Bullet(pygame.sprite.Sprite):
    """Bullet of Player"""
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.grouping)
        self.grouping = None
        self.image = load_image("laser.png")
        self.speed = 9  # speed of beam
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.rect.move_ip(0, -self.speed)  # move from bottom to top
        if self.rect.top < 0:  # once it reaches the top, disappear
            self.kill()


class Beam(pygame.sprite.Sprite):
    """Bullet of Enemy"""
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.grouping)
        self.grouping = None
        self.speed = 5
        self.image = load_image("e_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = position

    def update(self):
        self.rect.move_ip(0, self.speed)  # move from top to bottom
        if self.rect.bottom > SCR_RECT.height:
            # once it reaches bottom, disappear
            self.kill()


class Explosion(pygame.sprite.Sprite):
    """Enemy explosion"""
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self, self.grouping)
        self.grouping = None
        self.anime_frame = 2  # animation frame
        self.frame = 0
        self.images = split_image(load_image("explosion.png"), 16)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.max_frame = len(self.images) * self.anime_frame  # disappear

    def update(self):
        self.image = self.images[self.frame // self.anime_frame]
        self.frame += 1
        if self.frame == self.max_frame:
            self.kill()
