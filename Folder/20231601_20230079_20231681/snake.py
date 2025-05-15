import pygame


class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([25, 25])
        self.image.fill((45, 44, 44))
        pygame.draw.rect(self.image, (1, 248, 1), pygame.Rect(2, 2, 21, 21))
        self.rect = self.image.get_rect()
        self.direction = None
        self.length = 1
        self.body = []
        self.is_growing = False
        self.game_over = False

    def move(self):
        if self.game_over:
            return
        body_segment = None
        if len(self.body) != 0:
            if self.is_growing:
                body_segment = Snake()
                body_segment.rect.x = self.body[-1].rect.x
                body_segment.rect.y = self.body[-1].rect.y
                self.length += 1
                self.is_growing = False
            # to creat a deep copy of the body list
            temp_array = []
            for i in range(len(self.body)):
                temp = {"x": self.body[i].rect.x, "y": self.body[i].rect.y}
                temp_array.append(temp)
                pass

            for i in range(len(self.body)):
                if i == 0:
                    self.body[i].rect.x = self.rect.x
                    self.body[i].rect.y = self.rect.y
                else:
                    self.body[i].rect.x = temp_array[i - 1]["x"]
                    self.body[i].rect.y = temp_array[i - 1]["y"]
        else:
            if self.is_growing:
                body_segment = Snake()
                body_segment.rect.x = self.rect.x
                body_segment.rect.y = self.rect.y
                self.length += 1
                self.is_growing = False
        if body_segment is not None:
            self.body.append(body_segment)

        if self.direction == "up":
            self.rect.y -= 25
            if self.rect.y <= -1:
                self.game_over = True
        elif self.direction == "down":
            self.rect.y += 25
            if self.rect.y >= 576:
                self.game_over = True
        elif self.direction == "left":
            self.rect.x -= 25
            if self.rect.x <= -1:
                self.game_over = True
        elif self.direction == "right":
            self.rect.x += 25
            if self.rect.x >= 776:
                self.game_over = True

    def change_head_direction(self, direction):
        self.direction = direction
        pass

    def grow(self):
        self.is_growing = True
        pass
