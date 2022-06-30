# I don't own this code, I've only studied, written and edited it to work on Windows
# This code belongs to TokyoEdtech

import turtle
import math
from pygame import mixer  # For Sound

# Set up the screen
screen = turtle.Screen()
screen.setup(700, 700)
screen.bgcolor("black")
screen.title("Space Invaders")
screen.bgpic("background.gif")
screen.tracer(0)

# Register the shapes and sound
screen.register_shape("invader.gif")
screen.register_shape("player.gif")
mixer.init()
laser_sound = mixer.Sound("laser.wav")
explosion_sound = mixer.Sound("explosion.wav")

# Draw border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setpos(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.forward(600)
    border_pen.left(90)
border_pen.hideturtle()

# Create score
score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setpos(-290, 275)
scorestring = "Score: {}".format(score)  # or scorestring = f"Score: {score}"
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setpos(0, -250)
player.setheading(90)
player.speed = 0

# Choose number of enemies
number_of_enemies = 30
# Create an empty list of enemies
enemies = []
# Add enemies to the list
for i in range(number_of_enemies):
    # Create the enemy
    enemies.append(turtle.Turtle())

enemy_start_x = -225
enemy_start_y = 250
enemy_number = 0


for enemy in enemies:
    enemy.color("red")
    enemy.shape("invader.gif")
    enemy.penup()
    enemy.speed(0)
    x = enemy_start_x + (50 * enemy_number)
    y = enemy_start_y
    enemy.setpos(x, y)
    # Update the enemy number:
    enemy_number += 1
    if enemy_number == 10:
        enemy_start_y -= 50
        enemy_number = 0

enemyspeed = 0.1

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = 2
# Define bullet state
# ready - ready to fire
# fire - bullet is firing
bulletstate = "ready"


# Move the player left and right
def move_left():
    player.speed = -0.8

def move_right():
    player.speed = 0.8

def move_player():
    x = player.xcor()
    x += player.speed
    if x < -280:
        x = -280
    if x > 280:
        x = 280
    player.setx(x)

def fire_bullet():
    # Declare bulletstate as a global if it needs changed
    global bulletstate
    if bulletstate == "ready":
        bulletstate = "fire"
        # Move the bullet ot the just above the player
        x = player.xcor()
        y = player.ycor() + 10
        bullet.setpos(x, y)
        bullet.showturtle()
        laser_sound.play()


def is_collision(t1, t2):
    distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
    if distance < 15:
        return True
    else:
        return False


# Create keyboard bindings
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# Main game loop
while True:
    screen.update()
    move_player()

    for enemy in enemies:
        # Move the enemy
        x = enemy.xcor()
        x += enemyspeed
        enemy.setx(x)

        # Move the enemy back and down
        if enemy.xcor() > 280 or enemy.xcor() < -280:
            # Move all the enemies down
            for e in enemies:
                y = e.ycor()
                y -= 40
                e.sety(y)
            enemyspeed *= -1

        # Check for a collision between the bullet and the enemy
        if is_collision(bullet, enemy):
            # Reset the bullet
            bullet.hideturtle()
            bulletstate = "ready"
            bullet.setpos(0, -400)
            # Reset the enemy
            enemy.setpos(0, 10000)
            # Update the score
            score += 10
            scorestring = "Score: {}".format(score)
            score_pen.clear()
            score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
            explosion_sound.play()

        if is_collision(player, enemy):
            player.hideturtle()
            enemy.hideturtle()
            explosion_sound.play()
            print("Game Over")
            break

    # Move the bullet
    if bulletstate == "fire":
        y = bullet.ycor()
        y += bulletspeed
        bullet.sety(y)

    # Check to see if the bullet has gone to the top
    if bullet.ycor() > 275:
        bullet.hideturtle()
        bulletstate = "ready"
