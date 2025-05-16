import pygame  # Import the pygame module for game development
from snake import Snake  # Import the Snake class from snake module
from food import Food  # Import the Food class from food module

pygame.init()  # Initialize all imported pygame modules
win = pygame.display.set_mode((600, 400))  # Create a game window of size 600x400
pygame.display.set_caption("Snake Game")  # Set the title of the game window
clock = pygame.time.Clock()  # Create a clock object to manage game speed
font = pygame.font.SysFont('Arial', 25)  # Set the font and size for rendering text

snake = Snake()  # Create a Snake object
food = Food()  # Create a Food object
score = 0  # Initialize the score to 0
running = True  # Boolean to control the main game loop

while running:  # Main game loop
    clock.tick(10)  # Limit the game loop to 10 frames per second
    win.fill((0, 0, 0))  # Clear the screen by filling it with black

    for event in pygame.event.get():  # Handle events
        if event.type == pygame.QUIT:  # If the window close button is clicked
            running = False  # Exit the game loop

    keys = pygame.key.get_pressed()  # Get the state of all keyboard keys
    if keys[pygame.K_LEFT] and snake.direction != 'RIGHT':  # Change direction to LEFT if not moving RIGHT
        snake.direction = 'LEFT'
    elif keys[pygame.K_RIGHT] and snake.direction != 'LEFT':  # Change direction to RIGHT if not moving LEFT
        snake.direction = 'RIGHT'
    elif keys[pygame.K_UP] and snake.direction != 'DOWN':  # Change direction to UP if not moving DOWN
        snake.direction = 'UP'
    elif keys[pygame.K_DOWN] and snake.direction != 'UP':  # Change direction to DOWN if not moving UP
        snake.direction = 'DOWN'

    snake.move()  # Move the snake in the current direction

    if snake.body[0] == food.position:  # Check if the snake's head collides with the food
        snake.grow()  # Increase the length of the snake
        score += 1  # Increment the score
        food = Food()  # Generate a new food item

    if snake.check_collision():  # Check for collision with walls or itself
        running = False  # End the game if collision occurs

    for block in snake.body:  # Draw each segment of the snake
        pygame.draw.rect(win, (0, 255, 0), pygame.Rect(block[0], block[1], 10, 10))  # Green blocks for snake

    food.draw(win)  # Draw the food on the screen
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))  # Render score text
    win.blit(score_text, [10, 10])  # Display score text at the top-left corner
    pygame.display.update()  # Update the full display surface to the screen

pygame.quit()  # Uninitialize all pygame modules and quit the game
