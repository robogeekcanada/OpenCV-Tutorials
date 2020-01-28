#Example using homography for Star Wars intro
#Robo-Geek - www.robo-geek.ca

#Source and Destination images are the same initially
#but we will write the text in source and paste in
#the selected region using homography

import cv2
import numpy as np


font = cv2.FONT_HERSHEY_SIMPLEX
GOLD = (0,215,255)
font_size = 2
thickness = 4

#Source image and capture dimensions
frame = cv2.imread('starry_sky.jpg')
size = frame.shape
frame_width = size[1] -1 
frame_height = size[0] -1


#Star Wars intro text
intro_msg =[
"       Episode VIII",
"       THE LAST JEDI",
" ",
"The FIRST ORDER reigns.", 
"Having decimated the peaceful",
"Republic, Supreme Leader Snoke",
"now deploys his merciless legions",
"to seize military control of the galaxy.",
"Only General Leia Organa's band of",
"RESISTANCE fighters stand against",
"the rising tyranny, certain that",
"Jedi Master Luke Skywalker will",
"return and restore a spark of hope",
"to the fight. But the Resistance",
"has been exposed. As the First",
"Order speeds toward the rebel",
"base, the brave heroes mount a",
"desperate escape...."

]

#spacing starts 80% towards the bottom of the screen
#and increases gradually. SPEED is inversely proportional
frame_counter = 0
spacing = 0.8
SPEED = 15

while True and frame_counter < 800:

    frame = cv2.imread('starry_sky.jpg')


    if frame_counter % SPEED == 0:

        #Move up every cycle
        spacing = 0.8 - (frame_counter/SPEED)*0.05

        for line in intro_msg:

            cv2.putText(frame,line,(0,int(frame_height*spacing)),
                    font, font_size, GOLD,thickness)
            
            spacing +=0.15 #Space between lines


        #Source points
        pts_src = np.array([[0,0], [frame_width, 0], [frame_width, frame_height],
                            [0, frame_height]],dtype=float)


        # Read destination image
        img_dst = cv2.imread('starry_sky.jpg')
        img_dst_width = img_dst.shape[1]
        img_dst_height = img_dst.shape[0]

        pts_dst = np.float32([[374, 233], [802,233],
                    [1200, 768], [100, 768]]).reshape(-1,2)

        # Calculate Homography
        h, status = cv2.findHomography(pts_src, pts_dst)

        # Warp source image. 
        img_with_text = cv2.warpPerspective(frame, h,
                                            (img_dst_width,img_dst_height))

        # Black out original polygon
        cv2.fillConvexPoly(img_dst, pts_dst.astype(int), 0, 16)

        #cv2.imshow("img_with_text", img_with_text)


        # Add warped source image to destination image.
        img_dst = img_dst + img_with_text

        # Display image.
        cv2.imshow("Star Wars Intro", img_dst)

    frame_counter += 1


    if cv2.waitKey(1) == 27:
            break

cv2.destroyAllWindows()


