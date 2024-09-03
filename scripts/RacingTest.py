#!/usr/bin/env python
# coding: utf-8

# In[2]:

import pygame
import time
from pygame.math import Vector2
import math
import os
import neat
import graphviz
clock = pygame.time.Clock()
from pygame.locals import *
import pickle


class Player(pygame.sprite.Sprite):
    def __init__(self, picture,x=855,y=135):
        super(Player, self).__init__()
        self.tSpeed = 1.8
        self.heading   = 0
        self.speed     = 0
        self.velocity  = pygame.math.Vector2( 0, 0 )
        self.position  = pygame.math.Vector2( x, y )
        self.min_angle = 1
        self.rot_img   = []
        self.point = False
        self.check = 0
        #self.score = 0
        for i in range( 360 ):
            rotated_image = pygame.transform.rotozoom( picture, 360-90-( i*self.min_angle ), 1 )
            self.rot_img.append( rotated_image )
        self.min_angle = math.radians( self.min_angle )
        self.image = self.rot_img[0]
        self.rect = self.image.get_rect()
        self.rect.center = ( x, y )

    def update(self, probs):
        if (math.degrees(self.heading)>360):
            self.heading = math.radians(math.degrees(self.heading)%360)

        if  probs[0]>0.25:
            self.accelerate(0.5)
        elif  probs[0]<-0.25:
            self.brake()
        turning = False
        if  probs[1]>0.25:
            self.turn(-self.tSpeed)
            if self.tSpeed < 3.5:
                self.tSpeed+=0.1
            turning = True
        elif  probs[1]<-0.25: #if to elif
            self.turn(self.tSpeed)
            if self.tSpeed < 3.5:
                self.tSpeed+=0.1
            turning = True
        if(turning==False):
            self.tSpeed=1.8

        self.velocity.from_polar( ( self.speed, math.degrees( self.heading ) ) )
        self.position += self.velocity
        self.rect.center = ( round(self.position[0]), round(self.position[1] ) )

    def turn(self, angle_degrees):
        if(self.speed>0):
            self.heading += math.radians(angle_degrees)
            image_index = int( self.heading / self.min_angle ) % len( self.rot_img )
            if ( self.image != self.rot_img[ image_index ] ):
                x,y = self.rect.center
                self.image = self.rot_img[ image_index ]
                self.rect  = self.image.get_rect()
                self.rect.center = (x,y)
    def accelerate(self, amount):
        if (self.speed < 15):
            self.speed += amount

    def brake(self):
        self.speed = (self.speed/3)*2
        if ( abs( self.speed ) < 0.33 ):
            self.speed = 0
    def dRight(self):
        dist = 0
        tempX = self.position.x
        tempY = self.position.y
        d = math.degrees(self.heading)
        if(d < 45 and d > -45):
            while (screen.get_at((int(tempX), int(tempY)))[:3]!=(0,0,0)):
                    dist+=1
                    tempY+=1
        elif((d < 135 and d > 45) or (d > -315 and d < -225)):
            while (screen.get_at((int(tempX), int(tempY)))[:3]!=(0,0,0)):
                dist+=1
                tempX-=1
        elif(d > -135 and d < -45 or (d < 315 and d > 225)):
            while (screen.get_at((int(tempX), int(tempY)))[:3]!=(0,0,0)):
                dist+=1
                tempX+=1
        elif(abs(d) > 135 and abs(d) < 225):
            while (screen.get_at((int(tempX), int(tempY)))[:3]!=(0,0,0)):
                dist+=1
                tempY-=1
        return dist
    def dLeft(self):
        dist = 0
        tempX = self.position.x
        tempY = self.position.y
        d = math.degrees(self.heading)
        if(d < 45 and d > -45):
            while (screen.get_at((int(tempX), int(tempY)))[:3]!=(0,0,0)):
                    dist+=1
                    tempY-=1
        elif((d < 135 and d > 45) or (d > -315 and d < -225)):
            while (screen.get_at((int(tempX), int(tempY)))[:3]!=(0,0,0)):
                dist+=1
                tempX+=1
        elif(d > -135 and d < -45 or (d < 315 and d > 225)):
            while (screen.get_at((int(tempX), int(tempY)))[:3]!=(0,0,0)):
                dist+=1
                tempX-=1
        elif(abs(d) > 135 and abs(d) < 225):
            while (screen.get_at((int(tempX), int(tempY)))[:3]!=(0,0,0)):
                dist+=1
                tempY+=1
        return dist
    def dForward(self):
        dist = 0
        tempX = self.position.x
        tempY = self.position.y
        d = math.degrees(self.heading)
        if(d < 45 and d > -45):
            while (screen.get_at((int(tempX), int(tempY)))[:3]!=(0,0,0)):
                    dist+=1
                    tempX+=1
        elif((d < 135 and d > 45) or (d > -315 and d < -225)):
            while (screen.get_at((int(tempX), int(tempY)))[:3]!=(0,0,0)):
                dist+=1
                tempY+=1
        elif(d > -135 and d < -45 or (d < 315 and d > 225)):
            while (screen.get_at((int(tempX), int(tempY)))[:3]!=(0,0,0)):
                dist+=1
                tempY-=1
        elif(abs(d) > 135 and abs(d) < 225):
            while (screen.get_at((int(tempX), int(tempY)))[:3]!=(0,0,0)):
                dist+=1
                tempX-=1
        return dist

class Wall(pygame.sprite.Sprite):
    def __init__(self, posX, posY, box):
        super(Wall, self).__init__()
        self.x = posX
        self.y = posY
        self.image = box
        self.rect = self.image.get_rect()
        self.rect.center = ( self.x, self.y )
class Start(pygame.sprite.Sprite):
    def __init__(self, posX, posY, start):
        super(Start, self).__init__()
        self.x = posX
        self.y = posY
        self.image = start
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
class Check(pygame.sprite.Sprite):
    def __init__(self, posX, posY, check):
        super(Check, self).__init__()
        self.x = posX
        self.y = posY
        self.image = check
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
class Dist(pygame.sprite.Sprite):
    def __init__(self, posX, posY, d):
        super(Dist, self).__init__()
        self.x = posX
        self.y = posY
        self.image = d
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

def update_fps():
	fps = str(int(clock.get_fps()))
	fps_text = font.render(fps, 1, pygame.Color("coral"))
	return fps_text

pygame.init()
font = pygame.font.SysFont("Arial", 18)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000
flags = DOUBLEBUF
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], flags)
picture = pygame.image.load( 'car.png' ).convert_alpha()
wallP = pygame.image.load( 'wall.png' ).convert_alpha()
finishP = pygame.image.load("finishRed.png").convert_alpha()
checkP = pygame.image.load("line.png").convert_alpha()
distP = pygame.image.load("wall2GreyWide.png").convert_alpha()
distP2 = pygame.image.load("wall3GreyWide.png").convert_alpha()
sens = pygame.image.load("sens.png").convert_alpha()
wall = Wall(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, wallP)
finish = Start(830, 145, finishP)
check = Check(830, 485,checkP)
dist = Dist(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, distP)
dist2 = Dist(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, distP2)
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])


# font = pygame.font.Font('freesansbold.ttf', 32)
# text = font.render(' ', True, (255,255,255))
# textRect = text.get_rect()
# textRect.center = (150, 25)
maxFit = -1000
def main(genomes, config):
    global maxFit
    t = time.time()
    pList = []
    nets = []
    ge = []
    players = pygame.sprite.Group()
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        player = Player(picture)
        players.add(player)
        pList.append(player)
        g.fitness =0
        ge.append(g)
    running=True
    while running:
        if(len(pList)==0):
            # for g in ge:
            #     g.fitness-=5
            running = False
            break
        #print(t-time.time())
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    pygame.quit()
                    quit()
            elif event.type == QUIT:
                running = False
                pygame.quit()
                quit()

        #pressed_keys = pygame.key.get_pressed()
        #players.update(pressed_keys)

        for x, p in enumerate(pList):
            #output = nets[x].activate((p.dLeft(), p.dForward(), p.dRight(), p.speed, p.heading, p.tSpeed))
            output = nets[x].activate((p.dLeft(), p.dForward(), p.dRight(), p.speed, p.heading, p.tSpeed, p.heading, p.velocity.x, p.velocity.y, p.position.x, p.position.y))
            p.update(output)
        screen.fill((255,255,255))
        screen.blit(dist.image, dist.rect)
        screen.blit(dist2.image, dist.rect)
        screen.blit(finish.image, finish.rect)
        screen.blit(check.image, check.rect)
        players.draw(screen)
        screen.blit(wall.image, wall.rect)
        screen.blit(update_fps(), (10,0))
#         text = font.render(str(player.dRight()), True, (255,255,255))
#         textRect = text.get_rect()
#         textRect.center = (150, 25)
#         screen.blit(text, textRect)
        max = ge[0]
        x =0
        while x < len(pList):
            if(ge[x].fitness>max.fitness):
                max = ge[x]
            xRight, yRight = pList[x].rect.topright
            xLeft, yLeft = pList[x].rect.topleft
#             BxRight, ByRight = p.rect.bottomright
#             BxLeft, ByLeft = p.rect.bottomleft
            if (x<len(pList) and screen.get_at((int(xRight), int(yRight)))[:3]==(0,0,0)):
                ge[x].fitness-=1
                players.remove(pList[x])
                nets.pop(x)
                ge.pop(x)
                pList.pop(x)
                continue

            elif (x<len(pList) and screen.get_at((int(xLeft), int(yLeft)))[:3]==(0,0,0)):
                ge[x].fitness-=1
                players.remove(pList[x])
                nets.pop(x)
                ge.pop(x)
                pList.pop(x)
                continue
            if (x<len(pList) and screen.get_at((int(xRight), int(yRight)))[:3]==(252,252,252) and pList[x].check==1):
                pList[x].check = 2
                #p.score+=1
                ge[x].fitness+=5
            if (x<len(pList) and screen.get_at((int(xRight), int(yRight)))[:3]==(255,255,255) and (pList[x].check == 2 or pList[x].check ==0)):
                pList[x].check = 1
                #p.score+=1
                ge[x].fitness+=5

            if (x<len(pList) and screen.get_at((int(xRight), int(yRight)))[:3]==(255,215,5)):
                pList[x].point = True
            if (x<len(pList) and screen.get_at((int(xLeft), int(yLeft)))[:3]==(255,215,5)):
                pList[x].point = True

            if (x<len(pList) and math.degrees(pList[x].heading)%360>-45 and math.degrees(pList[x].heading)%360<45 and pList[x].position.y>500):
                ge[x].fitness-=1
            elif(x<len(pList) and abs(math.degrees(pList[x].heading))%360 > 135 and abs(math.degrees(pList[x].heading))%360 < 225 and pList[x].position.y<500):
                ge[x].fitness-=1


            # if (x<len(pList) and screen.get_at((int(xRight), int(yRight)))[:3]==(255,0,0)  and pList[x].point==True and math.degrees(pList[x].heading)%360>-45 and math.degrees(pList[x].heading)%360<45):
            #     ge[x].fitness+=50
            #     players.remove(pList[x])
            #     nets.pop(x)
            #     ge.pop(x)
            #     pList.pop(x)
            #     continue
            # elif (x<len(pList) and screen.get_at((int(xLeft), int(yLeft)))[:3]==(255,0,0)  and pList[x].point==True and math.degrees(pList[x].heading)%360>-45 and math.degrees(pList[x].heading)%360<45):
            #     ge[x].fitness+=50
            #     players.remove(pList[x])
            #     nets.pop(x)
            #     ge.pop(x)
            #     pList.pop(x)
            #     continue
            x+=1

        pygame.display.flip()
        tick = clock.tick(60)
#main()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                               neat.DefaultSpeciesSet, neat.DefaultStagnation,
                               config_path)
    p = neat.Population(config)
    #p = neat.Checkpointer.restore_checkpoint("neat-checkpoint-4099")
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    #checkpoint = neat.Checkpointer(generation_interval=100, time_interval_seconds=None)
    p.add_reporter(stats)
    #p.add_reporter(checkpoint)
    file = open("winner97.pkl",'rb')
    w = pickle.load(file)
    file.close()
    main([(0, w)], config) #50 = number of generations
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)

#print(p.score)


# In[ ]:
