import pygame
import math
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

import cv2
import numpy as np

def read_texture(opencv_image):

    pil_image=Image.fromarray(cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB))

    img_data = np.array(list(pil_image.getdata()), np.int8)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 pil_image.size[0], pil_image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID


pygame.init()
display = (400, 400)

screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
pygame.display.set_caption('Live Camera')

gluPerspective(40, (display[0]/display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)    # sets initial zoom so we can see globe

#counter = 0

while True:

    
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()

    if ret:

        #join the camera image side by side
        img = cv2.hconcat([frame, frame])
        texture = read_texture(img)

        #Keep turning right and down
        glRotate(30,0,5,0)
        glRotate(10,1,0,0)

        # Creates Sphere and wraps texture
        glEnable(GL_DEPTH_TEST)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        qobj = gluNewQuadric()
        gluQuadricTexture(qobj, GL_TRUE)
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, texture)
        gluSphere(qobj, 1, 50, 50)
        gluDeleteQuadric(qobj)
        glDisable(GL_TEXTURE_2D)

        
        for event in pygame.event.get(): 
            # Exit cleanly if user quits window
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Displays pygame window
        pygame.display.flip()
        pygame.time.wait(0)


