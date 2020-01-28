import cv2
import numpy as np

# Read image and determine width and height
img = cv2.imread('RG-logo.jpg')

width, height = img.shape[:2]

#Rotation with pivot from the center of image
#Set center as center of image

center = (int(width/2), int(height/2))
rotation_scale = 0.75
output_scale = (int(width*1.25),int(height*1.25))

for angle in range(0,361,5):
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, rotation_scale)
    #print(rotation_matrix)
    
    img_rotated = cv2.warpAffine(img, rotation_matrix, output_scale)
    cv2.waitKey(50)
    cv2.imshow('Rotation Demo', img_rotated)

#Translation right and down in increments of 2

y = 0
increment = 2
output_scale = (int(width*1.25),int(height*1.25))

for x in range(0, int(width/2), increment):
    
    translation_matrix = np.float32([[1,0,x], [0,1,y]])
    if y < int(height/2):
        y +=increment

    img_translated = cv2.warpAffine(img, translation_matrix, output_scale)
    cv2.waitKey(50)
    cv2.imshow("Translation Demo", img_translated)

