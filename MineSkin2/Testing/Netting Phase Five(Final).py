#Netting - Phase Five(Final) - Working
#Created By: TearlessCape914

#Import Modules
import numpy as np
import pygame
import math
import cv2
import os


#Settings
img = os.path.join('\\'.join(__file__.split('\\')[:-1]),'SampleSkin.png')
img = cv2.imread(img,cv2.IMREAD_UNCHANGED)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
grid = img.shape[:-1]#Width x Height x RGBA
screen_size = (500,500)
show_points = False


#Create Window Screen
screen = pygame.display.set_mode(screen_size,pygame.RESIZABLE)
pygame.display.set_caption('Netting - Phase Five(Final)')
screen.fill((255,255,255))
pygame.display.update()


#Define Functions
def ratio_line(point1,point2,ratio):
    frac = [ratio[0],sum(ratio)]
    rise = point2[1]-point1[1]
    run = point2[0]-point1[0]
    x = point1[0] + (frac[0]*run)/frac[1]
    y = point1[1] + (frac[0]*rise)/frac[1]
    return [int(x),int(y)]
def parse(point1,point2,slices):
    points = [point1]
    for i in range(1,slices):
        '''
        if show_points:
            pygame.draw.circle(screen,(0,255,33),ratio_line(point1,point2,[i,slices-i]),3)
        '''
        points.append(ratio_line(point1,point2,[i,slices-i]))
    points.append(point2)
    return points


#Create img_plane class
class img_plane():
    def __init__(self, img, line1=[[100,100],[100,200]], line2=[[200,100],[200,200]], enabled=True):
        self.img = img
        self.line1 = line1
        self.line2 = line2
        self.enabled = enabled
    def img_grid(self):
        grid = []
        slices1 = parse(self.line1[0],self.line1[1],self.img.shape[1])
        slices2 = parse(self.line2[0],self.line2[1],self.img.shape[1])
        for point_index in range(len(slices1)):
            grid.append(parse(slices1[point_index],slices2[point_index],self.img.shape[0]))
        return grid
    def draw_grid(self, grid):
        if self.enabled:
            for row in range(self.img.shape[1]):
                for column in range(self.img.shape[0]):
                    pygame.draw.polygon(screen, img[row][column], [grid[row][column],grid[row][column+1],grid[row+1][column+1],grid[row+1][column]])
    def enable(self): self.enabled = True
    def disable(self): self.enabled = False


#Main Loop
plane = img_plane(img)#, [[0,0],[0,100]],[[300,0],[300,300]])
plane.draw_grid(plane.img_grid())
pygame.display.update()
while True: pygame.event.get()#Hash this out to use tests...


'''
#Spinny Test
direction = 1
while True:
    pygame.event.get()

    screen.fill((255,255,255))
    plane.line1 = [[plane.line1[0][0]+direction,plane.line1[0][1]],[plane.line1[1][0]+direction,plane.line1[1][1]]]

    if plane.line1[0][0] > 600 or plane.line1[0][0] < 0:
        direction = -direction

    plane.draw_grid(plane.img_grid())
    pygame.display.update()
'''

'''
#Twisty Test
plane = img_plane(img)
starting1 = plane.line2[0][1]
starting2 = plane.line2[1][1]
direction = .1
while True:
    pygame.event.get()

    screen.fill((255,255,255))
    plane.line2[0][1] += direction
    plane.line2[1][1] -= direction

    if plane.line2[0][1] > starting2 or plane.line2[1][1] > starting2:
        direction *= -1

    plane.draw_grid(plane.img_grid())
    pygame.display.update()
'''



'''
Additional Notes:
  1) Study math kids... That is how this was made possible
  2) You can use this program for free!
    a) Must give link to my channel and this project though...
'''