'''
========================================
Load packages
========================================
'''

import pydicom as dicom 
import os
import cv2
import shutil, os       
from time import sleep
import glob            
import imageio

'''
========================================
Transform files type
========================================
'''

#Dicom tranform to jpg.
def emptydir(dirname):          
    if os.path.isdir(dirname):  
        shutil.rmtree(dirname) 
        sleep(2)               
    os.mkdir(dirname)     

folder_path = "Raw"
jpg_folder_path = "convert"
emptydir(jpg_folder_path)
images_folder_path = os.listdir(folder_path)
print("images_folder_path = ",images_folder_path)


for i in images_folder_path:
    full_images_path =folder_path + "\\" + i
    print("full_images_path = ",full_images_path)
    
    images_path = os.listdir(full_images_path)
    print("images_path = ",images_path)
    
    emptydir(jpg_folder_path +"\\" + i)
    
    for image in images_path:
        ds = dicom.dcmread(os.path.join(full_images_path, image)) 
        pixel_array_numpy = ds.pixel_array
        image = image. replace('.dcm', '.jpg') 
        pixel_array_numpy = cv2.cvtColor(pixel_array_numpy, cv2.COLOR_RGB2BGR) #RGB transform to BGR
        cv2.imwrite(os.path.join(jpg_folder_path +"\\" + i, image), pixel_array_numpy) #save files

'''
========================================
Crop
========================================
'''

# Have finished transforming files road.
path = (glob.glob("convert/ESO-051(O)/*.jpg"))
path

pic = path[0]
pic

im = cv2.imread(pic)
# Select ROI
r = cv2.selectROI(im)
#coordinate
(x, y, w, h) = r

imCrop = im[y: y + h, x:x + w]
print(r)

cv2.imshow("Image", imCrop) 
cv2.waitKey(10000)
cv2.destroyAllWindows()
checked = int(input('Please enter 1 to continue 1：'))
if checked == 1:
    output_folder = 'ROI/'+path[0][8:19]
    if not os.path.exists(output_folder): os.makedirs(output_folder)
    
    for i in path:
        image_read = cv2.imread(i)
        roiImg = image_read[y: y + h, x:x + w]
        cv2.imwrite(output_folder+i[19:], roiImg)
else:
    print("program shutdown")

'''
========================================
Bright spot
========================================
'''

path = (glob.glob("ROI/ESO-051(O)/*.jpg")) 
print(path)
output_folder = 'bright spot/'+path[0][4:15] 
if not os.path.exists(output_folder): os.makedirs(output_folder) 

for i in path:
    img = cv2.imread(i) 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(gray, (41,41), 0) 
   
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(blur)    

    if maxVal >= 174:  #set brightlight higher than 174,then make a spot.
        cv2.circle(img, maxLoc, 41, (255, 0, 0), 2) 
        cv2.putText(img, str(i), (400,300), cv2.FONT_HERSHEY_SIMPLEX, 1,
		(50, 168, 82), 2, cv2.LINE_AA) 
        cv2.imwrite(output_folder + i[15:], img) 
        cv2.imshow("results", img) 
        cv2.waitKey(1000) 
        cv2.destroyAllWindows()
    else:
        cv2.imwrite(output_folder + i[15:], img)

'''
========================================
GIF
========================================
'''
#Trying to make a GIF because I want to look it moving.

path='./bright spot/ESO-051(O)/'

def create_gif(gif_name, path, duration = 0.3):
    frames = []
    image_list = []
    for i in range(1,84):
        image_list.append(path+"I%d0.jpg" % i)
        
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return

create_gif('test.gif',path,duration = 0.3)


