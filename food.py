
import pygame
from setting import *
import random


import pygame 




class Food(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_snake
        pygame.sprite.Sprite.__init__(self, self.groups )
        self.game = game
        self.x, self.y = x, y
        self.image = pygame.image.load(random.choice(['orange.png.png', 'banana.png.png', 'apple.png.png']))
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE)) 

        # load a random fruit image and scale it to 32 x 32
        fruit_image = random.choice(['orange.png.png', 'banana.png.png', 'apple.png.png'])
        self.image = pygame.image.load(fruit_image)
        self.image = pygame.transform.scale(self.image, (TILESIZE, TILESIZE)) 

        self.rect = self.image.get_rect()


    def food_collision(self):
        if self.game.head.x == self.x and self.game.head.y == self.y:
            return True
        return False   

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
