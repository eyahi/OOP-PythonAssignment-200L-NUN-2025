import pygame

class Snake:
    def __init__(self):
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = "RIGHT"
        self.change_to = self.direction

    def change_direction(self, direction):
        opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if direction != opposites.get(self.direction):
            self.change_to = direction

    def move(self):
        if self.change_to:
            self.direction = self.change_to

        head = self.body[0].copy()
        if self.direction == 'UP':
            head[1] -= 10
        elif self.direction == 'DOWN':
            head[1] += 10
        elif self.direction == 'LEFT':
            head[0] -= 10
        elif self.direction == 'RIGHT':
            head[0] += 10

        self.body.insert(0, head)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])

    def check_collision(self, width, height):
        head = self.body[0]
        if head in self.body[1:] or head[0] < 0 or head[0] >= width or head[1] < 0 or head[1] >= height:
            return True
        return False

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(segment[0], segment[1], 10, 10))
