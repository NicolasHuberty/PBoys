import math
import random
import sys
import pygame
import os 
import subprocess
from matrixe import *
from pygame.locals import *
WHITE = (255,255,255)
BLACK = (0,0,0)
RED =(255,0,0)
GREEN =(0,255,0)
BLUE =(0,0,255)

class Game:
    def __init__(self, x, y, nbrBlocks):
        self.posBarreRed = x/2
        self.posBarreBlue = x/2
        self.x = x
        self.y = y
        self.nbrBlocks = nbrBlocks
        self.GameFinish = False
        self.matrix = [[0 for j in range(y)] for i in range(x)]
        self.nbrRedBalls = 1
        self.nbrBlueBalls = 1
        

        global pointBlue
        pointBlue = 0
        global pointRed
        pointRed = 0
        global bonusBlue
        bonusBlue = []
        global bonusRed
        bonusRed = []
        global start
        start = False
        global pause
        pause = False
        global ballRadius
        ballRadius = 10
        global ballVelocity
        ballVelocity = 0.1
        global sprites
        sprites = []
        global rect_vies 
        rect_vies = {}

    def choose(self,choose):
        if choose == 1:
            for i in range(0,(self.x),1):
                for j in range(0,(self.y),1):
                    if i == 0 or j == 0:
                        self.matrix[i][j] = Block([i,j],False)

            for i in range(1,(self.x-10),1):
                for j in range(1,(self.y-1),1):
                        self.matrix[i][j] = Block([i,j],True)
            

    def removeBlock(self, pos):
        self.matrix[pos[0],pos[1]] = None
        self.nbrBlocks -=1

        if self.nbrBlocks <= 0:
            self.GameFinish == True
    
    def GetFroPosition(self, pos):
        return self.matrix[pos[0]][pos[1]]
                

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        
        if random.randint(0,1) == 1:
            self.velocityX = ballVelocity 
        else:
            self.velocityX = -ballVelocity
         
        if random.randint(0,1) == 1:
            self.velocityY = ballVelocity
        else:
            self.velocityY = -ballVelocity
        '''
        self.velocityX =  random.randint(-15,15)
        self.velocityY =  random.randint(-15,15)
        '''
    def update(self):
        self.x += self.velocityX /2
        self.y += self.velocityY /2

        ball = self.draw()

         # Check for collision with bricks
        for brick in bricks:
            if ball.colliderect(brick):
                #rect_vies[brick] -=1
                #if rect_vies[brick]<= 0:
                bricks.remove(brick)
                if (ball.bottom > brick.top and ball.top < brick.top) or (ball.top < brick.bottom and ball.bottom > brick.bottom):   
                    self.velocityY = -self.velocityY
                if (ball.right > brick.left and ball.left < brick.left) or (ball.left < brick.right and ball.right > brick.right):
                    self.velocityX = -self.velocityX
                game.nbrBlocks -= 1        
       
            
        
        if self.x - self.radius < 0  or self.x + self.radius > screen_width:
            self.velocityX *= -1
        
        if self.color == RED:
            if ball.colliderect(paddleRed):
                self.velocityY *= -1
            elif self.y + self.radius > screen_height:
                    self.x = 2 * screen_width
                    self.y = screen_height//2
                    self.velocityX = 1
                    self.velocityY = 0
                    game.nbrRedBalls -=1
                    print(game.nbrRedBalls)
        else:
            if ball.colliderect(paddleBlue):
                self.velocityY *= -1
            elif self.y + self.radius > screen_height:
                self.x = 2 * screen_width
                self.y = screen_height//2   
                self.velocityX = 0
                self.velocityY = 0
                game.nbrBlueBalls -=1
                print(game.nbrBlueBalls)

        if  self.y - self.radius < 0 : 
            self.velocityY *= -1
           

        
    def draw(self):
        return pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

pygame.init()

info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
'''screen_width = 800
screen_height = 600'''
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("P-BOYZ")
clock = pygame.time.Clock()


#font_path = os.path.join("fonts", "Robus-BWqOd.otf")
def updateBackgroundImage():
    background_image = pygame.image.load("427159.jpg")
    background_rect = background_image.get_rect()
    background_x = screen_width // 2 - background_rect.width // 2
    background_y = screen_height // 2 - background_rect.height // 2
    screen.blit(background_image, (background_x, background_y))

updateBackgroundImage()
game = Game(100,100,20)

redBasePlace = []
redBasePlace = screen_width // 1.5 - 70, screen_height - 50
blueBasePlace = []
blueBasePlace = screen_width // 2.5 - 70, screen_height - 50

#gestion de la barre
paddleRed = pygame.Rect(redBasePlace[0], redBasePlace[1], 140, 20)
paddleBlue = pygame.Rect(blueBasePlace[0], blueBasePlace[1], 140, 20)

paddle_speedRed = 0
paddle_speedBlue = 0

#gestion des balles
redBalls = []
x = redBasePlace[0] + 70 # screen_width /2 - 10 #
y = redBasePlace[1]-20 # screen_height / 1.3 # 
color = RED
redBall = Ball(x, y, ballRadius, color)
redBalls.append(redBall)
sprites.append(redBall.draw())


blueBalls = []
x =   blueBasePlace[0] + 70 # screen_width /2 + 10 #
y =  blueBasePlace[1]-20 # screen_height / 1.3  #
color = BLUE
blueBall = Ball(x, y, ballRadius, color)
blueBalls.append(blueBall)
sprites.append(blueBall.draw())


#creation en fonction de la map
actualMatrixe = getMatrixes(5)
mapWidth = actualMatrixe[0] +5
print(mapWidth)
mapHeight = actualMatrixe[1] +4
print(mapHeight)
matrix_data = actualMatrixe[2] 


#creation des briques
brick_spacing = screen_width // 350
brick_width = screen_width // (mapHeight)
brick_height = screen_height // (mapWidth)
bricks = []

print(brick_spacing)
print(brick_width)
print(brick_height)

for i in range(mapHeight-4):
    brick_x = brick_spacing + i * (brick_width + brick_spacing)
    for j in range(mapWidth-10):
        if matrix_data[j][i] == 2:
            brick_y = brick_spacing + j * (brick_height + brick_spacing)
            brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
            bricks.append(brick_rect)
            #game.nbrBlocks +=1
            #rect_vies[brick_rect] = 1
        



while game.GameFinish != True:

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                paddle_speedRed = -10
            elif event.key == pygame.K_RIGHT:
                paddle_speedRed = 10
            if event.key == pygame.K_q:
                paddle_speedBlue = -10
            elif event.key == pygame.K_d:
                paddle_speedBlue = 10
            if event.key == pygame.K_r:
                print(event.key)
                newRedBalls = []
                for i in redBalls:
                     for y in range(3):
                        x = i.x
                        y = i.y
                        ball = Ball(x, y, ballRadius, RED)
                        newRedBalls.append(ball)
                        sprites.append(ball.draw())
                        game.nbrRedBalls +=1
                print(game.nbrRedBalls)

                for ball in newRedBalls:
                    redBalls.append(ball)

            if event.key == pygame.K_b:
                print(event.key)
                newBlueBalls = []
                for i in blueBalls:
                    for y in range(3):
                        x = i.x
                        y = i.y
                        ball = Ball(x, y, ballRadius, BLUE)
                        newBlueBalls.append(ball)
                        sprites.append(ball.draw())
                        game.nbrBlueBalls +=1
                print(game.nbrBlueBalls)
                for ball in newBlueBalls:
                    blueBalls.append(ball)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                paddle_speedRed = 0
            if event.key == pygame.K_q or event.key == pygame.K_d:
                paddle_speedBlue = 0
        




    #move the balls
    for ball in redBalls:
        ball.update()
      #  print("update Red Balls")
    for ball in blueBalls:
        ball.update()
    #  print("BlueBalls update")
      
    # Move the paddleRed
    paddleRed.x += paddle_speedRed
    if paddleRed.left < 0:
        paddleRed.left = 0
    elif paddleRed.right > screen_width:
        paddleRed.right = screen_width

      # Move the paddleBlue
    paddleBlue.x += paddle_speedBlue
    if paddleBlue.left < 0:
        paddleBlue.left = 0
    elif paddleBlue.right > screen_width:
        paddleBlue.right = screen_width

    


    pygame.draw.rect(screen, RED, paddleRed)
    pygame.draw.rect(screen, BLUE, paddleBlue)

    for brick in bricks:
        pygame.draw.rect(screen, WHITE, brick)
        
    
    pygame.display.flip()
    clock.tick(60)
    updateBackgroundImage()    

    if game.nbrBlueBalls <= 0:
        print("RedWins")
        game.GameFinish = True
    if game.nbrRedBalls <= 0:
        print("BlueWin")
        game.GameFinish = True
    

pygame.quit()