import pygame  # Import the pygame module for drawing
import random  # Import the random module to generate random positions

class Food:  # Define the Food class to represent food in the snake game
    def __init__(self):  # Constructor method to initialize the food object
        # Set a random position on a 600x400 grid (multiples of 10 pixels)
        self.position = [random.randrange(1, 60) * 10, random.randrange(1, 40) * 10]

    def draw(self, win):  # Method to draw the food on the game window
        # Draw a red square (10x10 pixels) at the food's position
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.position[0], self.position[1], 10, 10))

    def respawn(self):  # Method to generate a new random position for the food
        # Assign a new random position on the grid
        self.position = [random.randrange(1, 60) * 10, random.randrange(1, 40) * 10]
