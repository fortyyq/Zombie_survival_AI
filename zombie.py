import pygame
import random
from settings import *

class Zombie:
    def __init__(self):
        self.width = 50
        self.height = 50

        self.image = pygame.image.load("images/zombie.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.reset()

    def reset(self):
        self.x = random.randint(0, WIDTH - self.width)
        self.y = random.randint(-300, -50)
        self.speed = random.randint(2, 5)

    def move(self):
        self.y += self.speed

        if self.y > HEIGHT:
            self.reset()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def off_screen(self):
        return self.y > HEIGHT

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)