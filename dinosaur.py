import pygame,sys
from pygame import mixer

# initialize pygame
pygame.init()
mixer.init()

#FPS
FPS = 40
clock = pygame.time.Clock()

# screen
SCREENWIDTH = 600
SCREENHEIGHT = 300
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

# title and icon
title = pygame.display.set_caption("Dinosaur game")
icon = pygame.image.load("dinosaur.png")
pygame.display.set_icon(icon)

# load background
background = pygame.image.load("background.jpg")
backgroundx = 0
backgroundy = 0
backgroundx_change = 5
def display_background1(x,y):
    screen.blit(background,(x,y))

def display_background2(x,y):
    screen.blit(background,(x+600,y))

# move background
def move_background():
    global backgroundx
    backgroundx -= backgroundx_change
    if backgroundx + 600 < 0:
        backgroundx = 0

# dinosaur
class Dinosaur():
    def __init__(self,x,y):
        scale = 0.2
        self.x = x
        self.y = y
        self.x_change = 0
        self.y_change = 3
        self.index = 0
        self.jump = False
        self.update_time = pygame.time.get_ticks()
        self.dinosaur_list = []
        temp_list = []
        self.action = 0
        for i in range(6):
            img = pygame.image.load(f"img/walk/{i}.png")
            img = pygame.transform.scale(img,(img.get_width()*scale,img.get_height()*scale))
            temp_list.append(img)
        self.dinosaur_list.append(temp_list)
        temp_list = []

        for i in range(1):
            img = pygame.image.load(f"img/jump/{i}.png")
            img = pygame.transform.scale(img,(img.get_width()*scale,img.get_height()*scale))
            temp_list.append(img)
        self.dinosaur_list.append(temp_list)
        self.img = self.dinosaur_list[self.action][self.index]


    def move(self):
        if 230>= self.y>= 150:
            if self.jump == True:
                self.y -= self.y_change
        else:
            self.jump = False
        
        if self.y < 230:
            if self.jump == False:
                self.y += self.y_change
        

    def update_dinosaur(self):
        self.img = self.dinosaur_list[self.action][self.index] 

        if pygame.time.get_ticks() - self.update_time >= 100:
            self.update_time = pygame.time.get_ticks()
            self.index += 1

        if self.index >= len(self.dinosaur_list[self.action]):
            self.index = 0

    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.index = 0

    def get_rect(self):
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.x,self.y)

    def draw(self):
        self.get_rect()
        screen.blit(self.img,self.rect)

# Tree
class Tree():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.x_change = 5
        self.y_change = 0
        self.img = pygame.image.load("tree.png")

    def update_tree(self):
        self.x -= self.x_change
        if self.x < -10:
            self.x = 500

    def get_rect(self):
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.x,self.y)
    
    def draw(self):
        self.get_rect()
        screen.blit(self.img,self.rect)

tree = Tree(500,228)
dinosaur = Dinosaur(10,230)

# Score 
score_value = 0
font_score_value = pygame.font.SysFont("Arial",30)

# game over
overfont = pygame.font.SysFont("Arial",50)
over_game = overfont.render("GAME OVER",True,(0,0,0))

while True:
    # background
    display_background1(backgroundx,backgroundy)
    display_background2(backgroundx,backgroundy)
    move_background()

    # dinosaur 
    dinosaur.draw()
    dinosaur.update_dinosaur()
    dinosaur.move()

    # Tree
    tree.draw()
    tree.update_tree()

    # collision
    if dinosaur.rect.colliderect(tree.rect):
        
        pygame.draw.rect(screen,(255,0,0),dinosaur.rect,2)
        dinosaur.y_change = 0
        tree.x_change = 0
        backgroundx_change = 0
        dinosaur.index = 0
        screen.blit(over_game,(180,110))

    # score
    score_word = font_score_value.render("Score: "+ str(score_value),True,(0,0,0))
    if tree.x <= -10:
        score_value += 1
        jump_music = mixer.Sound("tick.wav")
        jump_music.play(0)
    screen.blit(score_word,(10,10))

    if 230 > dinosaur.y > 150:
        dinosaur.update_action(1)
    else:
        dinosaur.update_action(0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if dinosaur.y == 230:
                    dinosaur.jump = True

    clock.tick(FPS)
    pygame.display.update()