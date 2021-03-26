#3D Modeling - Working
#Created by TearlessCape914


#Import Modules
import numpy as np
import pyautogui
import pygame
import math
import cv2
import os


#Settings
window_size = (500,500)
background = (255,255,255)
lines = (0,0,0)


#Settings - Netting
img = os.path.join('\\'.join(__file__.split('\\')[:-1]),'SampleSkin.png')
img = cv2.imread(img,cv2.IMREAD_UNCHANGED)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
grid = img.shape[:-1]#Width x Height x RGBA
screen_size = (500,500)
show_points = False


#Create Window
screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
pygame.display.set_caption('3D Modeling')
screen.fill(background)
pygame.display.update()


#Screen Config
size_w, size_h = pyautogui.size()


#Define dist function
def dist(point1, point2):
    return [point2[0]-point1[0],point2[1]-point1[1]]

def points_to_angle(point1, point2):#Point1 to Point2
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    rads = math.atan2(-dy,dx)
    rads %= 2*math.pi
    return 360-(math.degrees(rads)+180+45)

def point_rotation(origin, rot_point, angle):
    angle = (int(angle)%360) * (math.pi/180)
    rotatedX = math.cos(angle) * (rot_point[0] - origin[0]) - math.sin(angle) * (rot_point[1] - origin[1]) + origin[0]
    rotatedY = math.sin(angle) * (rot_point[0] - origin[0]) + math.cos(angle) * (rot_point[1] - origin[1]) + origin[1]
    return [rotatedX,rotatedY]

def boxy(point_mid, point_other, size):
    ret = []
    ret.append(point_rotation(point_mid, (point_mid[0]+abs(size),point_mid[1]+abs(size)), points_to_angle(point_mid,point_other)+90+45))
    ret.append(point_rotation(point_mid, (point_mid[0]+abs(size),point_mid[1]+abs(size)), points_to_angle(point_mid,point_other)+45))
    ret.append(point_rotation(point_mid, (point_mid[0]+abs(size),point_mid[1]+abs(size)), points_to_angle(point_mid,point_other)-45))
    ret.append(point_rotation(point_mid, (point_mid[0]+abs(size),point_mid[1]+abs(size)), points_to_angle(point_mid,point_other)-90-45))
    return [ret[::-1][0]]+[ret[::-1][3]]+[ret[::-1][1]]+[ret[::-1][2]]#In specific order: tl, bl, tr, br

def draw_boxy(points,color=(0,0,0)):
    for point in points:
        pygame.draw.circle(screen, color, point, 3)

def move_boxy(points, offset = [0,0]):
    for i in points:
        i[0] += offset[0]
        i[1] += offset[1]
    return points


#Define Functions - Netting
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
        points.append(ratio_line(point1,point2,[i,slices-i]))
    points.append(point2)
    return points

def points_parser(points):
    return [points[:2],points[2:]]


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

class Head():
    def __init__(self, middle, size, front):
        self.middle = middle
        self.size = size
        self.back_plane = move_boxy(boxy(middle, [screen.get_width(),screen.get_height()//2], size), [-size//2,0])
        self.front_plane = move_boxy(boxy(middle, [screen.get_width(),screen.get_height()//2], size), [size,0])
        self.front = img_plane(front)
    def draw(self, show_planes=False):
        if show_planes:
            draw_boxy(self.back_plane,(255,0,0))
            draw_boxy(self.front_plane,(0,33,255))

#Main Loop
middle = (screen.get_width()//2,screen.get_height()//2)
plane = img_plane(img)
head = Head([screen.get_width()//2, screen.get_height()//2], 30, 'asdf')

while True:
    pygame.event.get()

    middle = size_w//2, size_h//2
    mouse_pos = list(pyautogui.position())

    virt_middle = [screen.get_width()//2, screen.get_height()//2]
    virt_mouse = [int(screen.get_width()*(mouse_pos[0]/size_w)),int(screen.get_height()*(mouse_pos[1]/size_h))]

    screen.fill(background)

    pygame.draw.circle(screen, lines,  virt_middle, 3)
    #pygame.draw.circle(screen, lines,  virt_mouse, 3)

    draw_boxy(move_boxy(boxy(virt_middle, virt_mouse, 30),[-15,-15]),(255,0,0))
    draw_boxy(move_boxy(boxy(virt_middle, virt_mouse, 30),[15,15]),(0,33,255))

    plane.line1, plane.line2 = points_parser(boxy(virt_middle, virt_mouse, 30))
    #plane.draw_grid(plane.img_grid())

    #head.draw(True)

    pygame.display.update()

'''
Additional Notes:
  1) Study math kids... That is how this was made possible
  2) You can use this program for free!
    a) Must give link to my channel and this project though...
'''