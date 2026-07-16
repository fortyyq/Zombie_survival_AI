import pygame
from settings import *

class Player:
    def __init__(self):
        self.width = 50
        self.height = 50

        self.image = pygame.image.load("images/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 80

    def move(self, x):
        if x is not None:
            self.x = int((x / 640) * WIDTH)

        if self.x < 0:
            self.x = 0

        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))