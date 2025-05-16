# simple snake game
# by ifon jason and prince

import turtle  # Turtle is used to create the graphics
import time  # For delays
import random  # To randomize food position
import pygame  # For music playback

pygame.mixer.init()  # Initialize pygame mixer
pygame.mixer.music.load("background.mp3")  # Load background music file
pygame.mixer.music.play(-1)  # Loop background music forever

delay = 0.1  # Initial game speed
score = 0  # Starting score
best_score = 0  # Highest score

# Set up the screen
wn = turtle.Screen()  # Create screen object
wn.title("slither.io")  # Set window title
wn.bgpic("back.gif")  # Set background image
wn.setup(width=600, height=600)  # Set size of the window
wn.tracer(0)  # Turn off automatic screen updates

# Create a turtle to display the menu
wn.addshape("menu.gif")  # Load menu image
menu_turtle = turtle.Turtle()  # Create turtle object
menu_turtle.speed(0)  # Max speed
menu_turtle.shape("menu.gif")  # Set menu image
menu_turtle.penup()  # Don’t draw lines
menu_turtle.goto(0, 0)  # Center menu image

game_started = False  # Flag to control when game starts

def start_game():
    global game_started
    game_started = True  # Change flag to start the game
    menu_turtle.hideturtle()  # Hide menu image

wn.listen()  # Listen for key presses
wn.onkey(start_game, "space")  # Start game when space is pressed

while not game_started:
    wn.update()  # Keep refreshing screen until game starts

# Register snake images
wn.addshape("head_up.gif")
wn.addshape("head_down.gif")
wn.addshape("head_left.gif")
wn.addshape("head_right.gif")

head = turtle.Turtle()  # Create snake head
head.speed(0)
head.shape("head_up.gif")
head.penup()
head.goto(0, 0)
head.direction = "start"  # Initial direction (not moving)

# Add food
wn.addshape("food.gif")
food = turtle.Turtle()
food.speed(0)
food.shape("food.gif")
food.penup()
food.goto(0, 100)

segments = []  # List to store body parts

# Create score display
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("red")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("score: 0 best score: 0", align="center", font=("courier", 24, "normal"))

# Add body part images
wn.addshape("tail_up.gif")
wn.addshape("tail_down.gif")
wn.addshape("tail_left.gif")
wn.addshape("tail_right.gif")
wn.addshape("body_horizontal.gif")
wn.addshape("body_vertical.gif")
wn.addshape("body_topleft.gif")
wn.addshape("body_topright.gif")
wn.addshape("body_bottomleft.gif")
wn.addshape("body_bottomright.gif")

# Movement controls
def go_up():
    if head.direction != "down":
        head.direction = "up"
        head.shape("head_up.gif")

def go_down():
    if head.direction != "up":
        head.direction = "down"
        head.shape("head_down.gif")

def go_left():
    if head.direction != "right":
        head.direction = "left"
        head.shape("head_left.gif")

def go_right():
    if head.direction != "left":
        head.direction = "right"
        head.shape("head_right.gif")

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Keyboard bindings (arrows + WASD)
wn.listen()
wn.onkey(go_up, "Up")
wn.onkey(go_down, "Down")
wn.onkey(go_left, "Left")
wn.onkey(go_right, "Right")
wn.onkey(go_up, "w")
wn.onkey(go_down, "s")
wn.onkey(go_left, "a")
wn.onkey(go_right, "d")

# Main game loop
while True:
    wn.update()

    # Border collision check
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
        time.sleep(1)
        head.goto(0, 0)
        head.direction = "stop"
        for segment in segments:
            segment.goto(1000, 1000)  # Move off-screen
        segments.clear()
        score = 0
        delay = 0.1
        pen.clear()
        pen.write("score: {} best score: {}".format(score, best_score), align="center", font=("courier", 24, "normal"))

    # Food collision
    if head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("body_horizontal.gif")
        new_segment.penup()
        segments.append(new_segment)

        delay -= 0.001
        score += 10

        if score > best_score:
            best_score = score

        pen.clear()
        pen.write("score: {} best score: {}".format(score, best_score), align="center", font=("courier", 24, "normal"))

    # Move body segments
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # --- Body image updating (THIS was missing in the version I sent before) ---
    for i in range(len(segments)):
        if i == len(segments) - 1:
            # Tail direction based on previous segment
            if segments[i - 1].xcor() < segments[i].xcor():
                segments[i].shape("tail_left.gif")
            elif segments[i - 1].xcor() > segments[i].xcor():
                segments[i].shape("tail_right.gif")
            elif segments[i - 1].ycor() < segments[i].ycor():
                segments[i].shape("tail_down.gif")
            elif segments[i - 1].ycor() > segments[i].ycor():
                segments[i].shape("tail_up.gif")
        else:
            # Body segment logic
            prev_seg = head if i == 0 else segments[i - 1]
            next_seg = segments[i + 1]

            x1 = prev_seg.xcor() - segments[i].xcor()
            y1 = prev_seg.ycor() - segments[i].ycor()
            x2 = segments[i].xcor() - next_seg.xcor()
            y2 = segments[i].ycor() - next_seg.ycor()

            if (x1 == 20 and y2 == 20) or (x2 == 20 and y1 == 20):
                segments[i].shape("body_bottomleft.gif")
            elif (x1 == -20 and y2 == 20) or (x2 == -20 and y1 == 20):
                segments[i].shape("body_bottomright.gif")
            elif (x1 == 20 and y2 == -20) or (x2 == 20 and y1 == -20):
                segments[i].shape("body_topleft.gif")
            elif (x1 == -20 and y2 == -20) or (x2 == -20 and y1 == -20):
                segments[i].shape("body_topright.gif")
            elif x1 == 0 and x2 == 0:
                segments[i].shape("body_vertical.gif")
            elif y1 == 0 and y2 == 0:
                segments[i].shape("body_horizontal.gif")

    # Collision with self
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.goto(0, 0)
            head.direction = "stop"
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0
            delay = 0.1
            pen.clear()
            pen.write("score: {} best score: {}".format(score, best_score), align="center", font=("courier", 24, "normal"))

    time.sleep(delay)  # Wait between frames

wn.mainloop()  # Keep window open
