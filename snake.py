
import pygame 
from setting import *




class Snake(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_snake
        pygame.sprite.Sprite.__init__(self, self.groups )
        self.game = game
        self.x, self.y = x, y
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE) 
        self.rect = self.image.get_rect()
        


    def body_collision(self,):
        if self.x == self.game.head.x and self.y == self.game.head.y:
            return True
        return False  
     

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
