import os
import numpy as np
import cv2
matrix = np.array([])


for filename in os.listdir('Training/passport'):
    if filename.endswith(".jpg"): 
    	print str(filename)
        img = cv2.imread(filename,0)
        surf = cv2.SURF(500)
        surf.upright = True
        surf.extended = True
        kp, des = surf.detectAndCompute(img,None)
        vector = des.flatten()
        np.vstack((matrix, vector))
        continue
    else:
        continue

# img = cv2.imread('Training/passport/7169136.jpg',0)

# surf = cv2.SURF(500)
# surf.upright = True
# surf.extended = True
# kp, des = surf.detectAndCompute(img,None)
#print des.shape