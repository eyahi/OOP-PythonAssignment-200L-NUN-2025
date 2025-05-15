import pygame


class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([25, 25])
        pygame.draw.rect(self.image, (255, 36, 1), pygame.Rect(0, 0, 25, 25))
        self.rect = self.image.get_rect()
