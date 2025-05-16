# simple snake game
# by ifon jason and prince

import turtle  # turtle enables users to create pictures and shapes by providing them with a virtual canvas.
import time    # create a delay
import random
import pygame  # for background music

# Initialize mixer
pygame.mixer.init()

# importing music
# Load music file
pygame.mixer.music.load("background.mp3")  # put your music file name here
pygame.mixer.music.play(-1)  # -1 means loop forever

delay = 0.1

# Score
score = 0
best_score = 0

# set the screen, wn = window
wn = turtle.Screen()
wn.title("slither.io")
wn.bgpic("back.gif")
wn.setup(width=600, height=600)
wn.tracer(0)  # turns off screen updates

# --- MENU SETUP ---
# Register and create a start menu
wn.addshape("menu.gif")
menu_turtle = turtle.Turtle()
menu_turtle.speed(0)
menu_turtle.shape("menu.gif")
menu_turtle.penup()
menu_turtle.goto(0, 0)

# Game state
game_started = False

# function to start game
def start_game():
    global game_started
    game_started = True
    menu_turtle.hideturtle()  # hide the menu

# Listen for space key to start
wn.listen()
wn.onkey(start_game, "space")

# wait for the player to press space
while not game_started:
    wn.update()

# --- AFTER SPACE, GAME STARTS ---

# snake head
wn.addshape("head_up.gif")
wn.addshape("head_down.gif")
wn.addshape("head_left.gif")
wn.addshape("head_right.gif")

head = turtle.Turtle()
head.speed(0)
head.shape("head_up.gif")
head.penup()
head.goto(0, 0)
head.direction = "stop"

# snake food
wn.addshape("food.gif")
food = turtle.Turtle()
food.speed(0)
food.shape("food.gif")
food.penup()
food.goto(0, 100)

segments = []

# pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("red")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("score: 0 best score: 0", align="center", font=("courier", 24, "normal"))

# register body and tail shapes
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

# functions for snake movement
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

# keyboard bindings
wn.listen()
wn.onkey(go_up, "Up")
wn.onkey(go_down, "Down")
wn.onkey(go_left, "Left")
wn.onkey(go_right, "Right")
wn.onkey(go_up, "w")
wn.onkey(go_down, "s")
wn.onkey(go_left, "a")
wn.onkey(go_right, "d")

# main game loop
while True:
    wn.update()

    # check for collision with the border
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290:
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

    # check for collision with the food
    if head.distance(food) < 20:
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x, y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("body_horizontal.gif")  # default shape
        new_segment.penup()
        segments.append(new_segment)

        delay -= 0.001
        score += 10
        if score > best_score:
            best_score = score

        pen.clear()
        pen.write("score: {} best score: {}".format(score, best_score), align="center", font=("courier", 24, "normal"))

    # move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)

    # move segment 0 to follow head
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    move()

    # update body parts shape
    for i in range(len(segments)):
        if i == len(segments) - 1:
            # tail
            if segments[i - 1].xcor() < segments[i].xcor():
                segments[i].shape("tail_left.gif")
            elif segments[i - 1].xcor() > segments[i].xcor():
                segments[i].shape("tail_right.gif")
            elif segments[i - 1].ycor() < segments[i].ycor():
                segments[i].shape("tail_down.gif")
            elif segments[i - 1].ycor() > segments[i].ycor():
                segments[i].shape("tail_up.gif")
        else:
            # body
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

    # check for head collision with the body
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

    time.sleep(delay)

wn.mainloop()
