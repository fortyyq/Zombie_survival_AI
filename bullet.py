import pygame
from settings import *

class Bullet:

    def __init__(self):
        self.width = 20
        self.height = 40

        self.image = pygame.image.load("images/bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 40))

        self.x = 0
        self.y = 0
        self.active = False

    def shoot(self, player):
        if not self.active:
            self.x = player.x + player.width // 2 - self.width // 2
            self.y = player.y
            self.active = True

    def move(self):
        if self.active:
            self.y -= BULLET_SPEED

            if self.y < 0:
                self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, (self.x, self.y))