import pygame
import random
from pygame import mixer

# Initialization of pygame
pygame.init()

# setting the screen and giving a title
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# importing background image, scaling it and setting it as icon
bg = pygame.image.load('spacebg.png')
background = pygame.transform.scale(bg, (800, 600))

# background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# importing an icon, scaling it and setting it as icon
icon = pygame.image.load('ufo.png')
resized_icon = pygame.transform.scale(icon, (32, 32))
pygame.display.set_icon(resized_icon)

# setting the player image
player_img = pygame.image.load("player.png")
re_player_img = pygame.transform.scale(player_img, (64, 64))
player_x = 370
player_y = 480
player_x_change = 0

# setting the enemy image
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
no_of_enemies = 6
for i in range(no_of_enemies):
    e_img = pygame.image.load("enemy.png")
    enemy_img.append(pygame.transform.scale(e_img, (64, 64)))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(0, 200))
    enemy_x_change.append(1.5)
    enemy_y_change.append(20)

# setting the bullet image
bullet_img = pygame.image.load("bullet.png")
re_bullet_img = pygame.transform.scale(bullet_img, (32, 32))

# Bullet
# ready: You cant see the bullet on screen
# fire: The bullet is moving now
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 3
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("gametext.ttf", 36)
textX = 10
textY = 20

# game_over
gamex = 170
gamey = 250
game_over_font = pygame.font.Font("gametext.ttf", 90)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (212, 175, 55))
    screen.blit(score, (x, y))


def game_over_text(x, y):
    game = game_over_font.render("Game Over", True, (220, 192, 203))
    screen.blit(game, (x, y))


def player(x, y):
    screen.blit(re_player_img, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(re_bullet_img, (x + 16, y + 10))


# CHECKING IF THE BULLET COLLIDED THE ENEMY
def iscollided(enemyx, enemyy, bulletx, bullety):
    a = pow((enemyx - bulletx), 2)
    b = pow((enemyy - bullety), 2)
    distance = pow((a + b), 0.5)
    if distance < 30:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 255, 255))

    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # pressing the key condition this increasing the change vale and moves the icon
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                player_x_change = -2

            if event.key == pygame.K_RIGHT:
                player_x_change = 2

            if event.key == pygame.K_SPACE:
                # only when the bullet state is ready bullet will be fired
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    # get the current x value which acts as x coor to the bullet
                    bullet_x = player_x
                    bullet(bullet_x, bullet_y)

        # key releasing condition
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    player_x += player_x_change
    # setting boundary for the icon
    if player_x <= 0:
        player_x = 0
        player_x_change = 0
    if player_x >= 800 - 64:
        player_x = 800 - 64
        player_x_change = 0

    # enemy movement
    for i in range(no_of_enemies):
        if enemy_y[i] > 420:
            for j in range(no_of_enemies):
                enemy_y[j] = 8000
            game_over_text(gamex, gamey)
            break
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 1.5
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 800 - 64:
            enemy_x_change[i] = -1.5
            enemy_y[i] += enemy_y_change[i]
        # checking collisions for every single enemy
        collision = iscollided(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_sound = mixer.Sound("explosion.wav")
            bullet_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 736)
            enemy_y[i] = random.randint(0, 250)
        enemy(enemy_x[i], enemy_y[i], i)

    player(player_x, player_y)
    show_score(textX, textY)
    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state != "ready":
        bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    pygame.display.update()
