"""
Tutorial followed from
https://www.youtube.com/watch?v=FfWpgLFMI7w
I don't own any of the artwork or sounds in this project, credit goes to their respective owners.
"""

import pygame
import random
import math
from pygame import mixer

# Initialise the pygame library
pygame.init()

# create the screen, 800 on x axis (wide) and 600 on y axis (tall)
screen = pygame.display.set_mode((800, 600))

# adding background
background = pygame.image.load("background.png")
# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)  # the -1 allows it to play on a loop

# Title and Icon
pygame.display.set_caption("Space Invaders")
# Icon from flat icon https://www.flaticon.com/authors/pixel-buddha
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load("space-invaders.png")
playerX = 370  # starting x coordinate
playerY = 480  # starting y coordinate
playerX_change = 0  # this will help move the user left or right

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
# This will allow us to have multiple enemies (6 in this case)
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 736))  # randomised starting x coordinate
    enemyY.append(random.randint(50, 150))  # randomised starting y coordinate
    enemyX_change.append(3)  # this will help move the enemy left or right
    enemyY_change.append(40)  # this will help move the enemy up or down

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480  # spawns at the top of the spaceship
bulletX_change = 0  # this will help move the enemy left or right
bulletY_change = 10  # this will help move the enemy up or down
bullet_state = "ready"
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently fired and moving

# Score tracking
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
# this is for where the score will be shown
textX = 10
textY = 10
# for more fonts place TTF files in your project folder and you can use it in the above code

# Game Over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    # this draws the players image (in this case, a little spaceship dude)
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    # this draws the players image (in this case, a little spaceship dude)
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Keeps the game window running
running = True

while running:

    # This fills in the screen using RGB allowing you to change the background colours
    screen.fill((0, 0, 0))
    # adding the background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            # This basically closes the program if you should click the close button on the window

        # if keystroke is pressed check whether it is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # this handles when the left arrow is pressed
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                # this handles when the right arrow is pressed
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()  # adds the sound and plays it once, not in a loop
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # this handles when the left or right arrow has been released
                playerX_change = 0

    playerX += playerX_change
    # test of boundaries / creating boundaries
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)  # randomised starting x coordinate
            enemyY[i] = random.randint(50, 150)  # randomised starting y coordinate

        enemy(enemyX[i], enemyY[i])

    # Bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Calling the player method has to be after the screen.fill otherwise it'll be covered
    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

# All gameplay functions must be inside of this while loop
