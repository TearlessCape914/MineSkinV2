#Netting - Phase Four - Works
#Created By: TearlessCape914

#Import Modules
import numpy as np
import keyboard
import pygame
import math
import cv2
import os


#Settings
speed = 3
img = os.path.join('\\'.join(__file__.split('\\')[:-1]),'SampleSkin.png')
img = cv2.imread(img,cv2.IMREAD_UNCHANGED)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
grid = img.shape[:-1]#Width x Height x RGBA
screen_size = (500,500)
points = [[200,200],[200,400],[400,400],[400,200]]
show_points = True
show_points_toggle = ' '


#Create Window Screen
screen = pygame.display.set_mode(screen_size,pygame.RESIZABLE)
pygame.display.set_caption('Netting - Phase Four')
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

def points_to_mb(point1,point2):
    if point2[0]-point1[0] != 0:
        return [(point2[1]-point1[1])/(point2[0]-point1[0]),(point1[1]-(point2[1]-point1[1])/(point2[0]-point1[0])*point1[0])]
    else:
        return [None, point1[0]]
def line_collide(line1,line2):
    m1, b1 = line1
    m2, b2 = line2
    if m2 == None:
        return [round(b2), round(m1*b2+b1)]
    elif m1 == None:
        return [round(b1), round(m2*b1+b2)]
    elif m1 - m2 == 0:
        return [round(b1), round(m2*b1+b2)]
    else:
        return [round((b2-b1)/(m1-m2)),round(m1*(b2-b1)/(m1-m2)+b1)]

def draw_all(points1, points2, points3, points4):
    for point1 in range(len(points1)-1):
        for point2 in range(len(points2)-1):
            pt1 = line_collide(points_to_mb(points1[point1],points3[-(point1+1)]),points_to_mb(points2[point2],points4[-(point2+1)]))
            pt2 = line_collide(points_to_mb(points1[point1+1],points3[-(point1+2)]),points_to_mb(points2[point2],points4[-(point2+1)]))
            pt3 = line_collide(points_to_mb(points1[point1+1],points3[-(point1+2)]),points_to_mb(points2[point2+1],points4[-(point2+2)]))
            pt4 = line_collide(points_to_mb(points1[point1],points3[-(point1+1)]),points_to_mb(points2[point2+1],points4[-(point2+2)]))
            pygame.draw.polygon(screen, img[point1][point2],[pt1,pt2,pt3,pt4])

import sys
#sys.exit()
#Main Loop
selection = False
show_lines = True
while True:
    pygame.event.get()

    screen.fill((255,255,255))
    
    if show_lines:
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
    
    draw_all(points1, points2, points3, points4)

    if show_lines:
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

    if keyboard.is_pressed('l') and show_lines:
        show_lines = False
        while keyboard.is_pressed('l'): pygame.event.get()
    elif keyboard.is_pressed('l') and not show_lines:
        show_lines = True
        while keyboard.is_pressed('l'): pygame.event.get()
    
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