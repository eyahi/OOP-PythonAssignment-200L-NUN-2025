import pygame
import random

class Food:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = self.generate()

    def generate(self):
        return [random.randrange(1, self.width // 10) * 10,
                random.randrange(1, self.height // 10) * 10]

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), pygame.Rect(self.position[0], self.position[1], 10, 10))
