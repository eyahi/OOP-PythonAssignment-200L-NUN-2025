import pygame
import sys
import random
from snake import Snake
from food import Food

# list off sprites (objects on the screen)
sprites_list = pygame.sprite.Group()
game_over = False


class snakeGame:
    def __init__(self):
        self.snake = Snake()
        self.snake.rect.x = 400
        self.snake.rect.y = 300
        self.food = Food()
        self.food.rect.x = 500
        self.food.rect.y = 300
        sprites_list.add(self.snake)
        sprites_list.add(self.food)

    def move_food(self):
        self.food.rect.x = random.randrange(0, 776, 25)
        self.food.rect.y = random.randrange(0, 576, 25)
        if self.food.rect.colliderect(self.snake.rect):
            return self.move_food()
        for i in self.snake.body:
            if self.food.rect.colliderect(i.rect):
                return self.move_food()

    def render_snake_body(self):
        for i in self.snake.body:
            if i not in sprites_list:
                sprites_list.add(i)

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Snake Game")
        clock = pygame.time.Clock()
        score_font = pygame.font.Font(pygame.font.get_default_font(), 36)
        score_value = 0
        score = score_font.render(f'Score: {score_value}', True, "white")
        scoreRect = score.get_rect()
        scoreRect.x = 30
        scoreRect.y = 30
        game_over_font = pygame.font.Font(pygame.font.get_default_font(), 50)
        game_over_text = game_over_font.render("Game Over", True, "white")
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.center = screen.get_rect().center

        # game loop
        while True:
            screen.fill((45, 44, 44))
            screen.blit(score, scoreRect)
            if self.snake.game_over:
                screen.blit(game_over_text, game_over_text_rect)
            for i in self.snake.body:
                if self.snake.rect.colliderect(i.rect):
                    self.snake.game_over = True
                    screen.blit(game_over_text, game_over_text_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # checking if the up arrow key was pressed
                    if event.key == pygame.K_UP:
                        # if the snake has a body it cant move in the opposite direction
                        if self.snake.direction == "down" and self.snake.length > 1:
                            continue
                        self.snake.change_head_direction("up")

                    if event.key == pygame.K_DOWN:
                        if self.snake.direction == "up" and self.snake.length > 1:
                            continue
                        self.snake.change_head_direction("down")

                    if event.key == pygame.K_LEFT:
                        if self.snake.direction == "right" and self.snake.length > 1:
                            continue
                        self.snake.change_head_direction("left")

                    if event.key == pygame.K_RIGHT:
                        if self.snake.direction == "left" and self.snake.length > 1:
                            continue
                        self.snake.change_head_direction("right")

            if self.snake.rect.colliderect(self.food.rect):
                self.snake.grow()
                self.move_food()
                score_value += 1
                score = score_font.render(
                    f'Score: {score_value}', True, "white")
                screen.fill((45, 44, 44))
                screen.blit(score, scoreRect)

            self.render_snake_body()
            self.snake.move()
            sprites_list.update()
            sprites_list.draw(screen)

            pygame.display.flip()

            clock.tick(7)  # limits FPS

        pygame.quit()


instance = snakeGame()
instance.run()
