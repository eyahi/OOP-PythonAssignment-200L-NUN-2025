import pygame
import random
import sqlite3

# --- Global Config ---
CONFIG = {
    "snake_color": (0, 255, 0),
    "bg_color": (0, 0, 0),
    "food_color": (255, 0, 0)
}

# --- Database Functions ---
def init_db():
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS scores (score INTEGER)')
    conn.commit()
    conn.close()

def add_score(score):
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('INSERT INTO scores (score) VALUES (?)', (score,))
    conn.commit()
    conn.close()

def get_top_scores(limit=5):
    conn = sqlite3.connect('highscores.db')
    c = conn.cursor()
    c.execute('SELECT score FROM scores ORDER BY score DESC LIMIT ?', (limit,))
    scores = c.fetchall()
    conn.close()
    return [s[0] for s in scores]

# --- Snake Class ---
class Snake:
    def __init__(self):
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.direction = 'RIGHT'
        self.change_to = self.direction

    def change_direction(self, direction):
        opposites = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if direction != opposites[self.direction]:
            self.change_to = direction

    def move(self):
        self.direction = self.change_to
        head = self.body[0][:]
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

    def collided(self, width, height):
        head = self.body[0]
        return (
            head in self.body[1:] or
            head[0] < 0 or head[0] >= width or
            head[1] < 0 or head[1] >= height
        )

    def draw(self, surface):
        for block in self.body:
            pygame.draw.rect(surface, CONFIG["snake_color"], pygame.Rect(block[0], block[1], 10, 10))

# --- Food Class ---
class Food:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.position = self._generate()

    def _generate(self):
        return [
            random.randint(0, (self.width - 10) // 10) * 10,
            random.randint(0, (self.height - 10) // 10) * 10
        ]

    def respawn(self):
        self.position = self._generate()

    def draw(self, surface):
        pygame.draw.rect(surface, CONFIG["food_color"], pygame.Rect(self.position[0], self.position[1], 10, 10))

# --- Snake Game Class ---
class SnakeGame:
    def __init__(self, width=600, height=400):
        pygame.init()
        init_db()
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.snake = Snake()
        self.food = Food(width, height)
        self.score = 0
        self.font = pygame.font.SysFont(None, 30)

    def draw_text(self, text, x, y, color=(255, 255, 255)):
        render = self.font.render(text, True, color)
        self.window.blit(render, (x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction('RIGHT')

    def update(self):
        self.snake.move()
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.respawn()
            self.score += 10
        if self.snake.collided(self.width, self.height):
            add_score(self.score)
            self.running = False

    def draw(self):
        self.window.fill(CONFIG["bg_color"])
        self.snake.draw(self.window)
        self.food.draw(self.window)
        self.draw_text(f'Score: {self.score}', 10, 10)
        pygame.display.flip()

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(15)

        self.show_game_over()
        pygame.quit()

    def show_game_over(self):
        font = pygame.font.SysFont(None, 36)
        waiting = True
        while waiting:
            self.window.fill((0, 0, 0))
            self.draw_text("GAME OVER", 230, 120, (255, 0, 0))
            self.draw_text(f"Score: {self.score}", 240, 160, (255, 255, 255))
            self.draw_text("Press R to Restart or M for Menu", 110, 220)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        waiting = False
                        SnakeGame().run()
                    elif event.key == pygame.K_m:
                        waiting = False
                        show_menu()

# --- Settings Menu ---
def show_settings(screen, font):
    options = ["Change Snake Color", "Change Background", "Change Food Color", "Back"]
    index = 0
    while True:
        screen.fill((0, 0, 0))
        for i, opt in enumerate(options):
            color = (255, 255, 0) if i == index else (255, 255, 255)
            render = font.render(opt, True, color)
            screen.blit(render, (180, 100 + i * 40))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    index = (index + 1) % len(options)
                elif event.key == pygame.K_UP:
                    index = (index - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[index] == "Change Snake Color":
                        CONFIG["snake_color"] = random_color()
                    elif options[index] == "Change Background":
                        CONFIG["bg_color"] = random_color()
                    elif options[index] == "Change Food Color":
                        CONFIG["food_color"] = random_color()
                    elif options[index] == "Back":
                        return

# --- Helpers ---
def random_color():
    return (random.randint(30, 255), random.randint(30, 255), random.randint(30, 255))

# --- Menu ---
def show_menu():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Snake Game Menu")
    font = pygame.font.SysFont(None, 36)
    init_db()

    options = ["Start Game", "High Scores", "Settings", "Quit"]
    index = 0

    while True:
        screen.fill((0, 0, 0))
        for i, opt in enumerate(options):
            color = (255, 255, 0) if i == index else (255, 255, 255)
            render = font.render(opt, True, color)
            screen.blit(render, (200, 100 + i * 50))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    index = (index + 1) % len(options)
                elif event.key == pygame.K_UP:
                    index = (index - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    choice = options[index]
                    if choice == "Start Game":
                        SnakeGame().run()
                    elif choice == "High Scores":
                        show_scores(screen, font)
                    elif choice == "Settings":
                        show_settings(screen, font)
                    elif choice == "Quit":
                        pygame.quit()
                        return

def show_scores(screen, font):
    scores = get_top_scores()
    screen.fill((0, 0, 0))
    for i, score in enumerate(scores):
        text = font.render(f"{i+1}. {score}", True, (255, 255, 0))
        screen.blit(text, (200, 100 + i * 40))
    pygame.display.flip()
    pygame.time.wait(3000)

# --- Start the Game ---
if __name__ == '__main__':
    show_menu()
    