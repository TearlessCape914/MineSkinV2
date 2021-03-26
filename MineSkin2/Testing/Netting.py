#Netting - Works
#Created By: TearlessCape914

#Import Modules
import pygame
import math


#Settings
screen_size = (300,300)


#Create Window Screen
screen = pygame.display.set_mode(screen_size,pygame.RESIZABLE)
pygame.display.set_caption('Netting')
screen.fill((255,255,255))
pygame.display.update()


#Define Functions
def dist(point1,point2):
    return math.sqrt((point2[0]-point1[0])**2+(point2[1]-point1[1])**2)

def orderize(point1,point2):
    points = [list(point1),list(point2)]
    points.sort()
    return points

def ratio_line(point1,point2,ratio):
    frac = [ratio[0],sum(ratio)]
    rise = point2[1]-point1[1]
    run = point2[0]-point1[0]
    x = point1[0] + (frac[0]*run)/frac[1]
    y = point1[1] + (frac[0]*rise)/frac[1]
    return [int(x),int(y)]

def parse(point1,point2,slices):
    #point1, point2 = orderize(point1, point2)
    points = [point1]
    for i in range(1,slices):
        pygame.draw.circle(screen,(0,255,33),ratio_line(point1,point2,[i,slices-i]),3)
        points.append(ratio_line(point1,point2,[i,slices-i]))
    points.append(point2)
    return points


#Main Loop
while True:
    pygame.event.get()

    middle = [screen.get_width()//2,screen.get_height()//2]
    mouse = pygame.mouse.get_pos()

    screen.fill((255,255,255))
    pygame.draw.line(screen, (0,0,0), middle, mouse)
    pygame.draw.circle(screen, (255,0,0), middle, 3)
    pygame.draw.circle(screen, (0,33,255), mouse, 3)

    parse(middle,mouse,3)

    pygame.display.update()

'''
Additional Notes:
  1) Study math kids... That is how this was made possible
  2) You can use this program for free!
    a) Must give link to my channel and this project though...
'''