#Netting - Phase Three - Works
#Created By: TearlessCape914

#Import Modules
import numpy as np
import keyboard
import pygame
import math


#Settings
speed = 3
grid = (8,8)#Width x Height
screen_size = (500,500)
points = [[100,100],[100,300],[300,300],[200,100]]
show_points = True
show_points_toggle = ' '


#Create Window Screen
screen = pygame.display.set_mode(screen_size,pygame.RESIZABLE)
pygame.display.set_caption('Netting - Phase Three')
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
        if show_points:
            pygame.draw.circle(screen,(0,255,33),ratio_line(point1,point2,[i,slices-i]),3)
        points.append(ratio_line(point1,point2,[i,slices-i]))
    points.append(point2)
    return points


#Main Loop
selection = False
while True:
    pygame.event.get()

    screen.fill((255,255,255))

    pygame.draw.line(screen, (0,0,0), points[0], points[1])
    pygame.draw.line(screen, (0,0,0), points[1], points[2])
    pygame.draw.line(screen, (0,0,0), points[2], points[3])
    pygame.draw.line(screen, (0,0,0), points[3], points[0])

    if show_points:
        pygame.draw.circle(screen, (0,33,255), points[0], 3)
        pygame.draw.circle(screen, (0,33,255), points[1], 3)
        pygame.draw.circle(screen, (0,33,255), points[2], 3)
        pygame.draw.circle(screen, (0,33,255), points[3], 3)

    points1 = parse(points[0],points[1],grid[1])
    points2 = parse(points[1],points[2],grid[0])
    points3 = parse(points[2],points[3],grid[1])
    points4 = parse(points[3],points[0],grid[0])

    for index in range(1,len(points1)-1):
        pygame.draw.line(screen, (125,125,125), points1[len(points1)-(1+index)], points3[index])
    for index in range(1,len(points1)-1):
        pygame.draw.line(screen, (125,125,125), points2[len(points1)-(1+index)], points4[index])

    if selection:
        pygame.draw.circle(screen, (255,0,0), selection, 3, 0)

    pygame.display.update()

    if keyboard.is_pressed(show_points_toggle) and show_points:
        show_points = False
        while keyboard.is_pressed(show_points_toggle): pygame.event.get()
    elif keyboard.is_pressed(show_points_toggle) and not show_points:
        show_points = True
        while keyboard.is_pressed(show_points_toggle): pygame.event.get()
    
    if pygame.mouse.get_pressed(3)[0]:
        dists = {}
        for point in points:
            dists[dist(list(pygame.mouse.get_pos()),point)] = point
        dists = list(dists.items())
        dists.sort()
        selection = dists[0][1]
        while pygame.mouse.get_pressed(3)[0]: pygame.event.get()
    if pygame.mouse.get_pressed(3)[2]:
        selection = False
        while pygame.mouse.get_pressed(3)[2]: pygame.event.get()
        
    if keyboard.is_pressed('up') and selection:
        points[points.index(selection)][1] -= speed
        selection[1] -= 1
        while keyboard.is_pressed('up'): pygame.event.get()    
    if keyboard.is_pressed('down') and selection:
        points[points.index(selection)][1] += speed
        selection[1] += 1
        while keyboard.is_pressed('down'): pygame.event.get()    
    if keyboard.is_pressed('left') and selection:
        points[points.index(selection)][0] -= speed
        selection[0] -= 1
        while keyboard.is_pressed('left'): pygame.event.get()    
    if keyboard.is_pressed('right') and selection:
        points[points.index(selection)][0] += speed
        selection[0] += 1
        while keyboard.is_pressed('right'): pygame.event.get()

'''
Additional Notes:
  1) Study math kids... That is how this was made possible
  2) You can use this program for free!
    a) Must give link to my channel and this project though...
'''