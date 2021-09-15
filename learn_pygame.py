import pygame
import os
import random

pygame.init()
pygame.mixer.init()


WIDTH=660
HEIGHT=660
FPS=15
WHITE=(255,255,255)
BLACK=(0,0,0)
SPEED = 20 
HEADSIZE=20
BODYSIZE=18
FRUITSIZE=10

head_img =pygame.image.load(os.path.join('img','circle.png'))
body_img =pygame.image.load(os.path.join('img','circle.png'))
fruit_img =pygame.image.load(os.path.join('img','circle.png'))

eat_sound =pygame.mixer.Sound(os.path.join('sound','eat_sound.mp3'))

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('The game')



grid=[[0 for _ in range (int(WIDTH/20))] for _ in range (int(HEIGHT/20))]


class head(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(head_img,(HEADSIZE,HEADSIZE))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center=(WIDTH/2,HEIGHT/2)
        self.dir='r'
        self.v=(1,0)
    def update(self):
        grid[int(self.rect.x/20)][int(self.rect.y/20)]=0
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT] and self.dir !='l' :
            self.dir='r'
            self.v=(1,0)
        elif pressed[pygame.K_LEFT] and self.dir !='r' :
            self.dir='l'
            self.v=(-1,0)
        elif pressed[pygame.K_UP] and self.dir !='d' :
            self.dir='u'
            self.v=(0,-1)
        elif pressed[pygame.K_DOWN] and self.dir !='u' :
            self.dir='d'
            self.v=(0,1)
        self.rect.x += self.v[0]*SPEED
        self.rect.y += self.v[1]*SPEED
        self.rect.x %= WIDTH
        self.rect.y %= HEIGHT
        grid[int(self.rect.x/HEADSIZE)][int(self.rect.y/HEADSIZE)]=1

class body(pygame.sprite.Sprite):
    def __init__(self,pos,dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(body_img,(BODYSIZE,BODYSIZE))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        x,y = pos
        space = (BODYSIZE+HEADSIZE)/2
        if(dir=='u'):
            y += space
        elif(dir=='d'):
            y-=space
        elif(dir=='l'):
            x+=space
        elif(dir=='r'):
            x-=space
        
        self.rect.center=(x,y)
        grid[int((x-BODYSIZE/2)/HEADSIZE)][int((y-BODYSIZE/2)/HEADSIZE)]=1
    def update(self,pos):
        grid[int(self.rect.x/HEADSIZE)][int(self.rect.y/HEADSIZE)]=0
        x,y = pos
        self.rect.center = pos
        grid[int((x-BODYSIZE/2)/HEADSIZE)][int((y-BODYSIZE/2)/HEADSIZE)]=1    
class fruit(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(fruit_img,(FRUITSIZE,FRUITSIZE))
        self.image.set_colorkey(WHITE)
        self.exist= True
        self.rect = self.image.get_rect()
        x=random.randrange(0,WIDTH/HEADSIZE,1)
        y=random.randrange(0,HEIGHT/HEADSIZE,1)
        while grid[x][y] == 1 :
            x=random.randrange(0,WIDTH/HEADSIZE)
            y=random.randrange(0,HEIGTH/HEADSIZE)
        self.rect.center=(x*HEADSIZE + HEADSIZE/2 , y*HEADSIZE + HEADSIZE/2)

    def update(self):
        if (self.exist == False):
            x=random.randrange(0,WIDTH/HEADSIZE,1)
            y=random.randrange(0,HEIGHT/HEADSIZE,1)
            while grid[x][y] == 1 :
                x=random.randrange(0,WIDTH/HEADSIZE)
                y=random.randrange(0,HEIGHT/HEADSIZE)
            self.rect.center=(x*HEADSIZE + HEADSIZE/2 , y*HEADSIZE + HEADSIZE/2)
            self.exist=True
    def ate(self):
        fruit.exist=False
        eat_sound.play()
        


all_sprit = pygame.sprite.Group()
head_g = pygame.sprite.Group()
body_g = pygame.sprite.Group()
head = head()
fruit = fruit()
all_sprit.add(head)
all_sprit.add(fruit)
head_g.add(head)

clock = pygame.time.Clock()
running=True

body_list = list()

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False
    pos = head.rect.center
    head.update()

    eat = pygame.sprite.spritecollide(fruit,head_g,False)
    if(eat):
        fruit.ate()
        Nbody = body(head.rect.center,head.dir)
        all_sprit.add(Nbody)
        body_g.add(Nbody)
        body_list.insert(0,Nbody)
    
    collide_self = pygame.sprite.spritecollide(head,body_g,False)
    if(collide_self):
        running=False
    if(body_list and not eat):
        body_list[-1].update(pos)
        copy = body_list[-1]
        body_list.pop()
        body_list.insert(0,copy)
    fruit.update()
    
    screen.fill(WHITE)
    all_sprit.draw(screen)
    pygame.display.update()

pygame.quit()