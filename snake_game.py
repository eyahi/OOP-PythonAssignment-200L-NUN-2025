


import pygame
from setting import *
from snake import *
from food import *
from UI import *
import random
import os

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.mixer.init()
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.orientation = 0
        self.paused = False
        self.playing = True
        self.score = 0
        self.high_score = self.load_high_score()
        

    def load_high_score(self):
        try:
            with open ('high_score.txt', 'r') as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0
   
    def save_high_score(self):
          with open ('high_score.txt', 'w') as file:
              file.write(str(self.score))
        
    def new(self):
        self.all_snake = pygame.sprite.Group()
        self.head = Snake(self, 5, 5)
        self.snake_parts = []
        self.snake_parts.append(Snake(self, 4, 5))
        self.snake_parts.append(Snake(self, 3, 5))
        
        
        self.food = Food(self, 20, 5)

        #reset game state
        self.orientation = 0
        self.paused = False
        self.playing = True
        self.score = 0

    def is_body_part(self):
        # check coordinates against the body of the snake 
        x = random.randint(0, GRIDWIDTH - 1)
        y = random.randint(0, GRIDHEIGHT - 1)
        for body in self.snake_parts:
            if x == body.x and y == body.y:
                x, y = self.is_body_part()
        return x, y



    def run(self):
        # game loop - set self.playing to False to end the game
        self.playing = True
        while self.playing:
            self.clock.tick(SPEED)
            self.events()
            self.update()
            self.draw()


            # high score check and update
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            

    def quit(self):
        pygame.quit()
        quit(0)

    def update(self):
        if  not self.paused: 
          self.all_snake.update()
          
        # check if the snake eats the food (orange, banana and apple)
        if self.food.food_collision():
            x, y = self.is_body_part()
            self.food.kill()
            self.food = Food(self, x, y)
            self.all_snake.add(self.food) 
            self.snake_parts.append(Snake (self,self.snake_parts[-1].x, self.snake_parts[-1].y))
            sound = pygame.mixer.Sound('crunch.mp3')
            pygame.mixer.Sound.play(sound)
            self.score += 1
        
        # update all snake
            self.all_snake.update()
 
           
    # track and move body parts
        x, y = self.head.x, self.head.y
        for body in self.snake_parts:
            temp_x, temp_y = body.x, body.y
            body.x, body.y = x, y
            x, y = temp_x, temp_y
       

        if self.orientation == 0:
            self.head.x += 1
        elif self.orientation == 1:
            self.head.y -= 1
        elif self.orientation == 2:
            self.head.x -= 1
        elif self.orientation == 3:
            self.head.y += 1
    
        # check for body collision 
        for body in self.snake_parts:
            if body.body_collision():
                self.playing = False

        # game over if snake hits the wall
        if self.head.x < 0 or self.head.x >= GRIDWIDTH or self.head.y < 0 or self.head.y >= GRIDHEIGHT:
            self.playing = False
            sound = pygame.mixer.Sound('gameover.mp3')
            pygame.mixer.Sound.play(sound)
            
    


    def draw_grid(self):
        for row in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, SOFTGREY, (row, 0), (row, HEIGHT))
        for col in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, SOFTGREY, (0, col), (WIDTH, col))

    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.all_snake.draw(self.screen)
        self.draw_grid()
        if self.paused:
            UIElement(10, 10, 'PAUSED').draw(self.screen, 100)
        #display current score and high score
        UIElement(1, 1, f'Score: {self.score}').draw(self.screen, 30)
       
        pygame.display.flip()

    def events(self):
        # catch all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if not self.paused:
               

                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                       if not self.orientation == 3: 
                        self.orientation = 1
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                       if not self.orientation == 1:
                        self.orientation = 3
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                       if not self.orientation == 0:
                        self.orientation = 2
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                       if not self.orientation == 2:
                        self.orientation = 0
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused 
               
        

    def main_screen(self):
        self.screen.fill(BGCOLOUR)
        if not self.playing:
            UIElement(8, 7, 'GAME OVER!').draw(self.screen, 100)
            UIElement(14, 13, f'Score: {self.score}').draw(self.screen, 40)
            UIElement(13, 11, f'High Score: {self.high_score}').draw(self.screen, 40)

        else:
            UIElement(8, 7, 'SNAKE GAME').draw(self.screen, 100)


        # buttons
        self.start_button = Button(self, BGCOLOUR, WHITE, WIDTH/2 - (150/2),470,  150, 50, 'START')
        self.quit_button = Button(self, BGCOLOUR, WHITE, WIDTH/2 - (150/2),545,  150, 50, 'QUIT')
   
        self.wait()
                
    def wait(self):
        waiting = True
        while waiting:
            self.start_button.draw(self.screen)
            self.quit_button.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEMOTION:
                    if self.start_button.is_over(mouse_x, mouse_y):
                        self.start_button.colour = LAVENDER
                    else:
                        self.start_button.colour = BGCOLOUR
                    if self.quit_button.is_over(mouse_x, mouse_y):
                        self.quit_button.colour = LAVENDER
                    else:
                        self.quit_button.colour = BGCOLOUR
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button.is_over(mouse_x, mouse_y):
                        waiting = False
                    if self.quit_button.is_over(mouse_x, mouse_y):
                        self.quit()





game = Game()
while True:
    game.main_screen()
    game.new()
    game.run() 
    