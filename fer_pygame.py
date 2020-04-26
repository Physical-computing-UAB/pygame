import pygame
import random


pygame.init()

screen = pygame.display.set_mode((800,600))

# background
background = pygame.image.load("space2.png")

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
ufoImg = pygame.image.load('ufo.png')
ufoX = random.randint(0,800)
ufoY = random.randint(5,150)
ufoX_change = 0
ufoY_change = 0
ufo_step_X_change = 5
ufo_step_Y_change = 50

ufoX_change = ufo_step_X_change


#bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = random.randint(50,150)
bulletX_change = 0
bulletY_change = bullet_offset
#"ready" you can't see the bullet
#"fired" you see the bullet
bullet_state = "ready"
bullet_step_Y_change = 10




def player(x, y):
    screen.blit(playerImg, (x, y))

def ufo(x,y):
    screen.blit(ufoImg, (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fired"
    screen.blit(bulletImg , (x+16, y+10))

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
            print("K_DOWN")
            if event.key == pygame.K_LEFT:
                playerX_change = -player_step_change
            if event.key == pygame.K_RIGHT:
                playerX_change = player_step_change
            if event.key == pygame.K_SPACE:
                fire_bullet(playerX, bulletY )
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
    ufoX += ufoX_change

    if ufoX <= 0:
        ufoX_change = ufo_step_X_change
        ufoY +=  ufo_step_Y_change
    elif ufoX >= 736:
        ufoX_change = -ufo_step_X_change

    # Bullet movement
    if bullet_state is "fired":
        fire_bullet(playerX,bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    ufo(ufoX,ufoY)

    pygame.display.update()
