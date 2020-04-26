import pygame
from pygame import mixer
import math
import random


pygame.init()

screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load("space2.png")

#backgroun sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title of the window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)



# Player
playerImg = pygame.image.load('space-ship.png')
playerX = 370
playerY = 480
playerX_change = 0
player_step_change = 5
bullet_offset = 480

# ufo
ufoImg = []
ufoX = []
ufoY= []
ufo_step_X_change = []
ufo_step_Y_change= []
ufoX_change = []
ufoY_change = []
num_of_enemies = 6

ufoX_offset = 735
ufoX_jump = 5
ufoY_jump = 50
for i in range(num_of_enemies):
    ufoImg.append(pygame.image.load('ufo.png'))
    ufoX.append(random.randint(0,ufoX_offset))
    ufoY.append(random.randint(5,150))
    ufo_step_X_change.append(ufoX_jump)
    ufo_step_Y_change.append(ufoY_jump)
    ufoX_change.append(ufo_step_X_change[i])
    ufoY_change.append(ufo_step_X_change[i])




#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = bullet_offset
bulletX_change = 0
bulletY_change = 0
#"ready" you can't see the bullet
#"fired" you see the bullet
bullet_state = "ready"
bullet_step_Y_change = 10

bulletY_change = bullet_step_Y_change



def player(x, y):
    screen.blit(playerImg, (x, y))

def ufo(x,y,i):
    screen.blit(ufoImg[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bulletImg , (x+16, y+10))

def isCollision(x1, y1, x2, y2):
    distance = math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2,2))
    if distance < 27:
        return True
    else:
        return False


# score
score_value =0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))


# game over
over_font = pygame.font.Font('freesansbold.ttf', 64)
def game_over():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))

    seguir_text = font.render("Press Y to continue / No to exit", True, (255,255,255))
    screen.blit(seguir_text, (200, 400))

    pygame.display.update()

    mixer.music.pause()
    pressed = 0
    while (not pressed):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    mixer.music.play(-1)
                    pressed = 1
                    inicializa_juego()
                elif event.key == pygame.K_n:
                    pygame.quit()
                    exit




def inicializa_juego():
    for i in range(num_of_enemies):
        ufoX[i] = random.randint(0,ufoX_offset)
        ufoY[i] = random.randint(5,150)
        ufo_step_X_change[i] = ufoX_jump
        ufo_step_Y_change[i] = ufoY_jump
        ufoX_change[i] = ufo_step_X_change[i]
        ufoY_change[i] = ufo_step_X_change[i]





#
# Loop
#

running = True
while running:

    # RGB
    screen.fill((10,10,10))
    # background
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -player_step_change
            if event.key == pygame.K_RIGHT:
                playerX_change = player_step_change
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY )
        if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_change=0

    # Checking for bounderies
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Checking for bounderies
    for i in range(num_of_enemies):

        # game over
        if ufoY[i] > 200:
            for j in range(num_of_enemies):
                ufoY[j] = 2000
            game_over()
            break

        ufoX[i] += ufoX_change[i]
        if ufoX[i] <= 0:
            ufoX_change[i] = ufo_step_X_change[i]
            ufoY[i] +=  ufo_step_Y_change[i]
        elif ufoX[i] >= ufoX_offset:
            ufoX_change[i ] = -ufo_step_X_change[i]

        # Check for the collision
        collision = isCollision(ufoX[i], ufoY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = bullet_offset
            bullet_state = "ready"
            ufoX[i] = random.randint(0,ufoX_offset)
            ufoY[i] = random.randint(5,150)
            score_value += 1

        ufo(ufoX[i],ufoY[i],  i)



    # Bullet movement
    if bulletY <= 0:
        bulletY = bullet_offset
        bullet_state = "ready"

    if bullet_state is "fired":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

    # Check isCollision


    player(playerX, playerY)

    show_score(textX, textY)

    pygame.display.update()
