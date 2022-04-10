from turtle import Screen
from pip import main
import pygame, random
from pygame.locals import *

pygame.init()

#Configuração de Tela

width = 600
height = 600
screen = pygame.display.set_mode((width, height))
fontTitle = pygame.font.SysFont("Ravie", 65)
fontOpitions = pygame.font.SysFont("Rockwell Extra Bold", 60)
title = fontTitle.render("Snake Game", True, ("white"))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

#Elementos
    
imageSizes = 30
snake = [((imageSizes*10), (imageSizes*10)), ((imageSizes*10 - imageSizes), (imageSizes*10)), ((imageSizes*10 - imageSizes*2), (imageSizes*10))]
head = pygame.image.load("./imagens/cobra_cabeca.png").convert()
head = pygame.transform.scale(head, (imageSizes,imageSizes))
body = pygame.image.load("./imagens/cobra_corpo.png").convert()
body = pygame.transform.scale(body, (imageSizes,imageSizes))
fruit = pygame.image.load("./imagens/fruta.png").convert()
fruit = pygame.transform.scale(fruit, (imageSizes,imageSizes))

#Randomizar Local da Fruta

def randomFruit():
    randomWidth = random.randint(0, (width - (imageSizes/2)))
    randomHeight = random.randint(0, (height - (imageSizes/2)))
    return(randomWidth//imageSizes * imageSizes, randomHeight//imageSizes * imageSizes)

fruitPosition = randomFruit()

#Função da Colisão

def collision(obj1, obj2):
    return (obj1[0] == obj2[0]) and (obj1[1] == obj2[1])

#Score

fontScore = pygame.font.SysFont("freesansbold.ttf", 50)
scoreValue = 0
textX = 0
textY = 0

def showScore (x,y):
    score = fontScore.render("Score: " + str(scoreValue), True, (255, 255, 255))
    screen.blit(score, (x,y))

#Teclas 

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
    
snakeDirection = RIGHT

#Menu

running = True

def mainMenu():
    menu = True
    while menu:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
            if event.type == KEYDOWN:
                if event.key == K_KP_ENTER:
                    running = True
                    menu = False

        screen.fill((144, 238, 144))
        screen.blit(title, (40, 130))
        screen.blit(fontOpitions.render("JOGAR", True, (65, 105, 225)), (230, 300))
        screen.blit(fontOpitions.render("SAIR", True, (65, 105, 225)), (250, 400))

        pygame.display.update()

#Loop de Execução

while running:
    clock.tick(10)
    showScore(textX, textY)

    #Configurações de Saída

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            
        #Inputs de Controle

        if event.type == KEYDOWN:
            if (event.key == K_UP or event.key == K_w) and snakeDirection != DOWN:
                snakeDirection = UP
                break
            if (event.key == K_DOWN or event.key == K_s) and snakeDirection != UP:
                snakeDirection = DOWN
                break
            if (event.key == K_LEFT or event.key == K_a) and snakeDirection != RIGHT:
                snakeDirection = LEFT
                break
            if (event.key == K_RIGHT or event.key == K_d) and snakeDirection != LEFT:
                snakeDirection = RIGHT    
                break
    
    #Colisão Com A Fruta

    if collision(snake[0], fruitPosition):
        fruitPosition = randomFruit()
            
        snake.append((0,0))
        scoreValue += 1
        showScore(textX, textY)

    #Comportamento do Corpo de "Fantasma"

    for i in range(len(snake) - 1, 0, -1):
        snake[i] = (snake[i-1][0], snake[i-1][1])
    
    #Movimentação da Cobra

    if snakeDirection == UP:
        snake[0] = (snake[0][0], snake[0][1] - imageSizes)
        head = pygame.transform.rotate(head, 270)
    if snakeDirection == DOWN:
        snake[0] = (snake[0][0], snake[0][1] + imageSizes)
        head = pygame.transform.rotate(head, 90)
    if snakeDirection == RIGHT:
        snake[0] = (snake[0][0] + imageSizes, snake[0][1])
        head = pygame.transform.rotate(head, 180)
    if snakeDirection == LEFT:
        snake[0] = (snake[0][0] - imageSizes, snake[0][1])
                
    screen.fill((144, 238, 144))
        
    #Desenho do Corpo da Cobra

    for pos in snake:
        if pos != snake[0]:
            screen.blit(body, pos)
                
    #Para Fazer Com Que A Fruta Spawne Em um Lugar Diferente do Corpo da Cobra

    for pos in range(1, len(snake) - 1):
        if fruitPosition == snake[pos]:
            fruitPosition = randomFruit()
            pos = 0
    
    #Desenhos

    screen.blit(fruit, fruitPosition)
    screen.blit(head, snake[0])
    head = pygame.image.load("./imagens/cobra_cabeca.png").convert()
    head = pygame.transform.scale(head, (imageSizes,imageSizes))
    showScore(textX, textY)
           
    #GAMEOVER

    if snake[0][0] >= width or snake[0][0] < 0 or snake[0][1] >= height or snake[0][1] < 0:
        pygame.time.delay(1000)
        running = False
    for i in range(1, len(snake) - 1):
        if snake[0] == snake[i]:
            pygame.time.delay(1000)
            running = False
        
    if running == True:   
        pygame.display.update()