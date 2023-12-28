# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 23:14:42 2023

@author: Juris
"""

import cv2
import glob, os
import matplotlib.pyplot as plt
from skimage import io, measure
import numpy as np


ball = io.imread('ball_for_color.png')
io.imshow(ball)
plt.show()
#%%
r = []
g = []
b = []

for i in range(61):
    y_coord = measure.profile_line(ball, (0, i), (56, i))
    r = np.append(r, y_coord[:, 0])
    r = np.delete(r, np.where(r == 0))
    
    g = np.append(g, y_coord[:, 1])
    g = np.delete(g, np.where(g == 0))
    
    b = np.append(b, y_coord[:, 2])
    b = np.delete(b, np.where(b == 0))

#%%
r_max = np.max(r)
r_min = np.min(r)

g_max = np.max(g)
g_min = np.min(g)

b_max = np.max(b)
b_min = np.min(b)

print(f'r_max: {r_max}')
print(f'r_min: {r_min}')
print(f'g_max: {g_max}')
print(f'g_min: {g_min}')
print(f'b_max: {b_max}')
print(f'b_min: {b_min}')

plt.plot(y_coord)
plt.show()


