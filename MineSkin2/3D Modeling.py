#Import Modules
import _thread as thread
import numpy as np
import pyautogui
import keyboard
import pygame
import math
import json
import time
import cv2
import os


#Settings
cur_dir = '\\'.join(__file__.split('\\')[:-1])
file_data = json.load(open(os.path.join(cur_dir,'Config.json'),'r'))
plane_size = file_data['Configs']['PlaneSize']
window_size = file_data['Configs']['WindowSize']
offset = file_data['Configs']['Offset']
background = tuple(file_data['Configs']['Background'])
show_points = file_data['Configs']['ShowPoints'] != 0
lines = tuple(file_data['Configs']['Lines'])
reducer = file_data['Configs']['Reducer']
speed = file_data['Configs']['Speed']


#Define Image Functions
def open_img(filename):
    img = cv2.imread(filename,cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


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
        if show_points:
            pygame.draw.circle(screen,(0,255,33),ratio_line(point1,point2,[i,slices-i]),3)
        points.append(ratio_line(point1,point2,[i,slices-i]))
    points.append(point2)
    return points


#Define Additional Functions
def point_rotation(origin, rot_point, angle):
    angle = (angle%360) * (math.pi/180)
    rotatedX = math.cos(angle) * (rot_point[0] - origin[0]) - math.sin(angle) * (rot_point[1] - origin[1]) + origin[0]
    rotatedY = math.sin(angle) * (rot_point[0] - origin[0]) + math.cos(angle) * (rot_point[1] - origin[1]) + origin[1]
    return [rotatedX,rotatedY]
def x_to_angle(x):
    x1,y1 = 0,-90
    x2,y2 = window_size[0]-1,90
    m = (y2-y1)/(x2-x1)
    return m*x+(y1-m*x1)
def y_to_angle(y):
    x1,y1 = 0,-90
    x2,y2 = window_size[1]-1,90
    m = (y2-y1)/(x2-x1)
    return m*y+(y1-m*x1)
def get_lines(points, stuff):
    return [[points[stuff[1]][:2],points[stuff[0]][:2]],[points[stuff[3]][:2],points[stuff[2]][:2]]]


#Create Cube Class
class Cube():
    def __init__(self, size, middle=[window_size[0]//2,window_size[1]//2,0]):
        self.p1 = [middle[0]-size,middle[1]+size,middle[2]-size]
        self.p2 = [middle[0]-size,middle[1]-size,middle[2]-size]
        self.p3 = [middle[0]+size,middle[1]+size,middle[2]-size]
        self.p4 = [middle[0]+size,middle[1]-size,middle[2]-size]
        self.p5 = [middle[0]-size,middle[1]+size,middle[2]+size]
        self.p6 = [middle[0]-size,middle[1]-size,middle[2]+size]
        self.p7 = [middle[0]+size,middle[1]+size,middle[2]+size]
        self.p8 = [middle[0]+size,middle[1]-size,middle[2]+size]

    def rotate_bt(self, angle):#Rotate on Bottom-Top Axis
        new_points = []
        origins = [[(self.p1[0]+self.p4[0])/2,(self.p1[1]+self.p4[1])/2],[(self.p5[0]+self.p8[0])/2,(self.p5[1]+self.p8[1])/2]]#1st: 1234, 2nd 5678
        new_points.append(point_rotation(origins[0],[self.p1[0],self.p1[1]],angle)+[self.p1[2]])
        new_points.append(point_rotation(origins[0],[self.p2[0],self.p2[1]],angle)+[self.p2[2]])
        new_points.append(point_rotation(origins[0],[self.p3[0],self.p3[1]],angle)+[self.p3[2]])
        new_points.append(point_rotation(origins[0],[self.p4[0],self.p4[1]],angle)+[self.p4[2]])
        new_points.append(point_rotation(origins[1],[self.p5[0],self.p5[1]],angle)+[self.p5[2]])
        new_points.append(point_rotation(origins[1],[self.p6[0],self.p6[1]],angle)+[self.p6[2]])
        new_points.append(point_rotation(origins[1],[self.p7[0],self.p7[1]],angle)+[self.p7[2]])
        new_points.append(point_rotation(origins[1],[self.p8[0],self.p8[1]],angle)+[self.p8[2]])
        self.p1,self.p2,self.p3,self.p4,self.p5,self.p6,self.p7,self.p8 = new_points

    def rotate_lr(self, angle):#Rotate on Left-RIght Axis
        new_points = []
        origins = [[(self.p1[0]+self.p7[0])/2,(self.p1[2]+self.p7[2])/2],[(self.p2[0]+self.p8[0])/2,(self.p2[2]+self.p8[2])/2]]#1st 1357, 2nd 2468
        new_points.append(point_rotation(origins[0],[self.p1[0],self.p1[2]],angle))
        new_points[-1].insert(1,self.p1[1])
        new_points.append(point_rotation(origins[0],[self.p3[0],self.p3[2]],angle))
        new_points[-1].insert(1,self.p3[1])
        new_points.append(point_rotation(origins[0],[self.p5[0],self.p5[2]],angle))
        new_points[-1].insert(1,self.p5[1])
        new_points.append(point_rotation(origins[0],[self.p7[0],self.p7[2]],angle))
        new_points[-1].insert(1,self.p7[1])
        new_points.append(point_rotation(origins[1],[self.p2[0],self.p2[2]],angle))
        new_points[-1].insert(1,self.p2[1])
        new_points.append(point_rotation(origins[1],[self.p4[0],self.p4[2]],angle))
        new_points[-1].insert(1,self.p4[1])
        new_points.append(point_rotation(origins[1],[self.p6[0],self.p6[2]],angle))
        new_points[-1].insert(1,self.p6[1])
        new_points.append(point_rotation(origins[1],[self.p8[0],self.p8[2]],angle))
        new_points[-1].insert(1,self.p8[1])
        self.p1,self.p3,self.p5,self.p7,self.p2,self.p4,self.p6,self.p8 = new_points

    def rotate_bf(self, angle):#Rotate on Left-RIght Axis
        new_points = []
        origins = [[(self.p1[1]+self.p6[1])/2,(self.p1[2]+self.p6[2])/2],[(self.p3[1]+self.p8[1])/2,(self.p3[2]+self.p8[2])/2]]#1st: 1526, 2nd 3748
        new_points.append([self.p1[0]]+point_rotation(origins[0],[self.p1[1],self.p1[2]],angle))
        new_points.append([self.p5[0]]+point_rotation(origins[0],[self.p5[1],self.p5[2]],angle))
        new_points.append([self.p2[0]]+point_rotation(origins[0],[self.p2[1],self.p2[2]],angle))
        new_points.append([self.p6[0]]+point_rotation(origins[0],[self.p6[1],self.p6[2]],angle))
        new_points.append([self.p3[0]]+point_rotation(origins[1],[self.p3[1],self.p3[2]],angle))
        new_points.append([self.p7[0]]+point_rotation(origins[1],[self.p7[1],self.p7[2]],angle))
        new_points.append([self.p4[0]]+point_rotation(origins[1],[self.p4[1],self.p4[2]],angle))
        new_points.append([self.p8[0]]+point_rotation(origins[1],[self.p8[1],self.p8[2]],angle))
        self.p1,self.p5,self.p2,self.p6,self.p3,self.p7,self.p4,self.p8 = new_points

    def pygame_points(self):
        ret = []
        for point in [self.p1,self.p2,self.p3,self.p4,self.p5,self.p6,self.p7,self.p8]:
            ret.append([int(point[0]),int(point[1]),int(point[2])])
        return ret
    
    def reset(self, size, middle=[window_size[0]//2,window_size[1]//2,0]):
        self.p1 = [middle[0]-size,middle[1]+size,middle[2]-size]
        self.p2 = [middle[0]-size,middle[1]-size,middle[2]-size]
        self.p3 = [middle[0]+size,middle[1]+size,middle[2]-size]
        self.p4 = [middle[0]+size,middle[1]-size,middle[2]-size]
        self.p5 = [middle[0]-size,middle[1]+size,middle[2]+size]
        self.p6 = [middle[0]-size,middle[1]-size,middle[2]+size]
        self.p7 = [middle[0]+size,middle[1]+size,middle[2]+size]
        self.p8 = [middle[0]+size,middle[1]-size,middle[2]+size]


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
                    pygame.draw.polygon(screen, self.img[row][column], [grid[row][column],grid[row][column+1],grid[row+1][column+1],grid[row+1][column]])
    def enable(self): self.enabled = True
    def disable(self): self.enabled = False


#Create Window
pygame.init()
virt_middle = [window_size[0]//2-offset[0],window_size[1]//2-offset[1]]
screen = pygame.display.set_mode(window_size,pygame.RESIZABLE)
pygame.display.set_caption('3D Modeling')
pygame.mouse.set_visible(file_data['Configs']['ShowMouse']==1)


#Main Loop
cube = Cube(plane_size)
front = img_plane(open_img(os.path.join(cur_dir,'Generated',file_data['FileNames']['Front'])))
right = img_plane(open_img(os.path.join(cur_dir,'Generated',file_data['FileNames']['Right'])))
left = img_plane(open_img(os.path.join(cur_dir,'Generated',file_data['FileNames']['Left'])))
top = img_plane(open_img(os.path.join(cur_dir,'Generated',file_data['FileNames']['Top'])))
bottom = img_plane(open_img(os.path.join(cur_dir,'Generated',file_data['FileNames']['Bottom'])))


#Define Additional Rotation
#bt_rot = 0


#Define Update Function
def Update(plane_name, img_filename):#Update('left', 'Front.png') - Sample
    plane_name = plane_name.title()
    if plane_name == 'Top':
        top.img = cv2.cvtColor(cv2.imread(os.path.join(cur_dir, 'Custom', img_filename)),cv2.COLOR_BGR2RGB)
    elif plane_name == 'Left':
        left.img = cv2.cvtColor(cv2.imread(os.path.join(cur_dir, 'Custom', img_filename)),cv2.COLOR_BGR2RGB)
    elif plane_name == 'Front':
        front.img = cv2.cvtColor(cv2.imread(os.path.join(cur_dir, 'Custom', img_filename)),cv2.COLOR_BGR2RGB)
    elif plane_name == 'Right':
        right.img = cv2.cvtColor(cv2.imread(os.path.join(cur_dir, 'Custom', img_filename)),cv2.COLOR_BGR2RGB)
    elif plane_name == 'Bottom':
        bottom.img = cv2.cvtColor(cv2.imread(os.path.join(cur_dir, 'Custom', img_filename)),cv2.COLOR_BGR2RGB)
def Reset(plane_name):
    plane_name = plane_name.title()
    if plane_name == 'Top':
        top.img = open_img(os.path.join(cur_dir,'Generated',file_data['FileNames']['Top']))
    elif plane_name == 'Left':
        left.img = open_img(os.path.join(cur_dir,'Generated',file_data['FileNames']['Left']))
    elif plane_name == 'Front':
        front.img = open_img(os.path.join(cur_dir,'Generated',file_data['FileNames']['Front']))
    elif plane_name == 'Right':
        right.img = open_img(os.path.join(cur_dir,'Generated',file_data['FileNames']['Right']))
    elif plane_name == 'Bottom':
        bottom.img = open_img(os.path.join(cur_dir,'Generated',file_data['FileNames']['Bottom']))


#Create Callbacks List
def Main(affected, filename, duration):
    Update(affected, filename)
    time.sleep(duration)
    Reset(affected)
def sep_thread(affected, filename, duration):
    thread.start_new_thread(Main, (affected, filename, duration))
for Key in file_data['Custom'].keys():
    args = (file_data['Custom'][Key]['AffectedPlane'], file_data['Custom'][Key]['Filename'], file_data['Custom'][Key]['Duration'])
    keyboard.add_hotkey(file_data['Custom'][Key]['Hotkey'],sep_thread,args=args)


#Main Loop
while True:
    #Get Screen Events
    pygame.event.get()

    #Fill Background
    screen.fill(background)

    #Get Virt Mouse
    virt_mouse = [(screen.get_width()*pyautogui.position().x)/pyautogui.size().width,(screen.get_height()*pyautogui.position().y)/pyautogui.size().height]

    #Get Points of Cube
    points = cube.pygame_points()
    if show_points:
        for point in points:
            pygame.draw.circle(screen, (0,0,0), point[:2], 3)

    #Draw Left Plane
    if virt_mouse[0] > screen.get_width()//2:
        left.line1, left.line2 = get_lines(points, [4,5,0,1])
        left.draw_grid(left.img_grid())

    #Draw Top Plane
    if virt_mouse[1] > screen.get_height()//2:
        top.line1, top.line2 = get_lines(points, [5,1,7,3])
        top.draw_grid(top.img_grid())

    #Draw Right Plane
    if virt_mouse[0] < screen.get_width()//2:
        right.line1, right.line2 = get_lines(points, [2,3,6,7])
        right.draw_grid(right.img_grid())

    #Draw Bottom Plane
    if virt_mouse[1] < screen.get_height()//2:
        bottom.line1, bottom.line2 = get_lines(points, [0,4,2,6])
        bottom.draw_grid(bottom.img_grid())
    
    #Draw Body
    body_surf = pygame.image.load(os.path.join(cur_dir,'Generated','Body_Main.png'))
    body_surf = pygame.transform.scale(body_surf, [screen.get_width()//3,screen.get_height()//2-plane_size+15*10])
    screen.blit(body_surf, [screen.get_width()//2-body_surf.get_width()//2,screen.get_height()//2+plane_size-10])#The 10 is extra
    right_surf = pygame.image.load(os.path.join(cur_dir,'Generated','Arm_Left.png'))
    right_surf = pygame.transform.scale(right_surf, [screen.get_width()//7,screen.get_height()//2-plane_size+15*10+5])
    screen.blit(right_surf, [screen.get_width()//2-body_surf.get_width()//2-right_surf.get_width(), screen.get_height()//2+plane_size-10])#The 10 is extra
    left_surf = pygame.image.load(os.path.join(cur_dir,'Generated','Arm_Right.png'))
    left_surf = pygame.transform.scale(left_surf, [screen.get_width()//7,screen.get_height()//2-plane_size+15*10+5])
    screen.blit(left_surf, [screen.get_width()//2+body_surf.get_width()//2, screen.get_height()//2+plane_size-10])#The 10 is extra

    #Draw Front Plane
    front.line1, front.line2 = get_lines(points, [0,1,2,3])
    front.draw_grid(front.img_grid())

    #Cube Rotations
    cube.reset(plane_size)
    cube.rotate_lr(x_to_angle(virt_mouse[0])//reducer)
    cube.rotate_bf(y_to_angle(virt_mouse[1])//reducer)
    #cube.rotate_bt(int(bt_rot))

    #Rotations w/ Keyboard
    #if keyboard.is_pressed('right'): bt_rot += speed
    #if keyboard.is_pressed('left'): bt_rot -= speed

    #Update Screen
    pygame.display.update()

'''
Additional Notes:
  1) Study math kids... That is how this was made possible
  2) You can use this program for free!
    a) Must give link to my channel and this project though...
'''