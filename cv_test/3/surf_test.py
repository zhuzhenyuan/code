# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 22:41:39 2014
@author: duan
"""
import numpy as np
import cv2
from matplotlib import pyplot as plt
# img = cv2.imread('t.jpg', 0)
img = cv2.imread('t_t2.jpg', 0)
# Initiate STAR detector
surf = cv2.SURF()
# find the keypoints with ORB
kp = surf.detect(img, None)
# compute the descriptors with ORB
# kp, des = surf.compute(img, kp)
# draw only keypoints location,not size and orientation
img2 = cv2.drawKeypoints(img, kp, 0, color=(0,255,0), flags=0)
plt.imshow(img2),plt.show()