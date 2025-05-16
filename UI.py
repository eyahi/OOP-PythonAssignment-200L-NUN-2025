
import pygame
from setting import *


class UIElement:
    def __init__(self, x, y, text):
        self.x, self.y = x * TILESIZE, y * TILESIZE
        self.text = text

    def draw(self, screen, font_size):
        font = pygame.font.SysFont('Arial', font_size)
        text = font.render(self.text, True, WHITE)
        screen.blit(text, (self.x, self.y))


class Button:
    def __init__(self, game, colour, outline,x, y, width, height, text):
        self.game = game
        self.colour, self.outline = colour, outline
        self.x, self.y = x, y
        self.width, self.height = width, height 
        self.text = text


    def draw(self, screen):
        pygame.draw.rect(screen, self.outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4))
        pygame.draw.rect(screen, self.colour, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont('Arial', 30)
        text = font.render(self.text, True, WHITE)
        draw_x = self.x + (self.width/2 - text.get_width()/2)
        draw_y = self.y + (self.height/2 - text.get_height()/2)
        screen.blit(text, (draw_x, draw_y))

    def is_over(self, mouse_x, mouse_y):
        return self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height





