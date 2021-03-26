#Import Modules
import numpy as np
import cv2
import os


#Get Skin Path
cur_dir = '\\'.join(__file__.split('\\')[:-1])
skin_dir = os.path.join(cur_dir,'Skin')
skin = os.path.join(skin_dir,os.listdir(skin_dir)[0])


#Load Skin
skin_img = cv2.imread(skin, cv2.IMREAD_UNCHANGED)
size = list(skin_img.shape)[:2]
unit = size[0]//8#Minecraft Skin


#Define Extract Function
def extract(img, start, end):#Includes start, not includes end
    new_img = []
    for row in img[start[1]:end[1]]:
        new_img.append(row[start[0]:end[0]])
    return np.array(new_img)

#Segment
stuff = [
    'Nothing.png','Top.png','Bottom.png','Nothing.png','Nothing.png','Top-Asc.png','Nothing.png','Nothing.png',
    'Left.png','Front.png','Right.png','Back.png','Left-Asc.png','Front-Asc.png','Right-Asc.png','Nothing.png'
]
folder = os.path.join(cur_dir,'Generated')
for x in list(range(size[0]//8)):
    for y in list(range(size[1]//8))[:2]:
        index = x + y*8
        cv2.imwrite(os.path.join(folder,stuff[index]), extract(skin_img, [x*8,y*8], [(x+1)*8,(y+1)*8]))
cv2.imwrite(os.path.join(folder,'Body_Main.png'), extract(skin_img, [20,20], [28,32]))
cv2.imwrite(os.path.join(folder,'Arm_Left.png'), extract(skin_img, [44,20], [48,32]))
cv2.imwrite(os.path.join(folder,'Arm_Right.png'), extract(skin_img, [36,52], [40,64]))


#Clean Up
if os.path.isfile(os.path.join(folder,'Nothing.png')):
    os.remove(os.path.join(folder,'Nothing.png'))

'''
Additional Notes:
  1) Study math kids... That is how this was made possible
  2) You can use this program for free!
    a) Must give link to my channel and this project though...
'''