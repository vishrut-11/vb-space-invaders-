import pygame
import random
import math
from pygame import mixer
#intialize the pyagame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800, 600)) #tuple is at inside

#background
background = pygame.image.load("game/background.png")

# background music
mixer.music.load("game/background.wav")        #to  load the soound
mixer.music.play(-1)                               # to play sound (-1) play the sound in loop

#title and icon
pygame.display.set_caption("Vb space Game")
icon = pygame.image.load("game/ufo.png")
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load("game/player.png")
#co-ordinate
playerX = 376    #between x-axis
playerY = 480     #between y-axis
playerX_change = 0



#Enemy empyty of  list
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []               
enemyY_change = []
num_of_enmies = 6


#Enemy
for i in range(6):
    enemyImg.append(pygame.image.load("game/enemy.png"))
    enemyX.append(random.randint(0, 735))   #between x-axis
    enemyY.append(random.randint(50, 150))  #between y-axis
    enemyX_change.append(10)                # speed of enemy  
    enemyY_change.append(30)

#Bullet
#ready - you can't see the bullet on the screen
#fire - the bullet is currently moving
bulletImg = pygame.image.load("game/bullet.png")
bulletX = 0 
bulletY = 480                           # to keep bullet on top on spaceship
bulletX_change= 0
bulletY_change = 40                     #speed of bullet
bullet_state = "ready"                  # state of bullet

#score 
score_val = 0
font = pygame.font.Font("freesansbold.ttf", 32)

textX = 10  # where do you want to show
textY = 10  # where do you want to show

#game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)

def show_score(x , y):
    score = font.render("Score : " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text =  over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit( over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))      #blit means show the image ((x, y and what position)
    # logic to move image

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))       #blit means show the image 

def fire_bullet(x,y):
    global bullet_state                 #accesing global keyword in func
    bullet_state = "fire"               #setting new state of bullet so that it can fire
    screen.blit(bulletImg, (x+16, y+10))

def iscollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY ,2)))         #d=√((x_2-x_1)²+(y_2-y_1)²)
    if distance < 27:
        return True
    else:
        return False



#Game loop
running = True
while running:

    #RGB red green and blue
    screen.fill((0, 0, 0))
    #playerX += 0.3              #playerX = playerX+0.3

    # enemyX += 0.3

    #background
    screen.blit(background, (0, 0))

    #events from keyboard 
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            running = False

    #if keystroke is presssed check whether its is right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -20                     #print("left key is pressed")
            if event.key == pygame.K_RIGHT:
                playerX_change =  20                     #print("right key is pressed")
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":             #when you press the pressbar it check the bullet is on the screen or not whyen it get x -coordinate of sapceship
                    # bullet sound 
                    bullet_sound =  mixer.Sound("game/laser.wav")
                    bullet_sound.play()
                    bulletX = playerX                   # wheneve the spacebar is press we have the playerX co-ordinate value in bulletX and bulletX pass pass every where  
                    fire_bullet(bulletX, bulletY)       #calling fire_bullet here
                            
        if event.type == pygame.KEYUP:
            if (event.key == pygame.K_LEFT) or ( event.key == pygame.K_RIGHT):
               playerX_change = 0                      #print("keystorke has been relased")




    #370 = 370 + -0.1 -> 370 = 370 - 0.1 
    # 370= 370 + 0.1  -> 370 = 370 + 0.1
    # checking for boundery of spaceship so its doesn't go out
    playerX += playerX_change           #changeing existing to new player 
    if playerX<=0:
        playerX = 0
    elif playerX>=736:
        playerX = 736


    #Enemy movemnet 
    # (0,800) = 750 + 0.3 ->    750 = 750 + 0.3, 0.4, 0.5, 0.6
    # (0,800) = 750 + -0.3  ->  750 = 750 - 0.3,  0.2, 0.1, 0.0

    for i in range(num_of_enmies):

        #game over
        if enemyY[i] >440:
            for j in range(num_of_enmies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]             #changeing existing to new enemy after hitting boundery( basiically movemennt of enemy)
        if enemyX[i]<=0:
            enemyX_change[i]  = 10              #when it hit  x-axis at 0 it must go towards right hand side(whenever a boundry is hit it should go some place)
            enemyY[i] +=  enemyY_change[i]        #when it hit  x-axis so it will come down by 30px
        elif enemyX[i] >=736:
            enemyX_change[i]  = -10             #when it hit  x-axis at 736 it must go towards left hand side
            enemyY[i] +=  enemyY_change[i]  

        #collsioin 
        collision = iscollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # collision sound 
            explosionSound =  mixer.Sound("game/explosion.wav")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_val += 1
            # print(score_val) 
            enemyX[i] = random.randint(0, 736)   # if the collision occer send enemy back to his original position
            enemyY[i] = random.randint(50, 150) 
        
        enemy(enemyX[i], enemyY[i] , i)


     #bullet movemnet 
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)   #to see the bullet in continew appering on the screen after ittartion of while loop
        bulletY -= bulletY_change       #decrase the value of bullet in y-axis (up direction)

    # checking for boundery of bulletY(above the screen)
    if bulletY<=0:
        bulletY=480
        bullet_state = "ready"

#function calls

    player(playerX, playerY)
    show_score(textX, textY)
# anthing added nedd to be updated
    pygame.display.update()



















