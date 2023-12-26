# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 10:57:28 2023

@author: Juris
"""

import cv2
import os
import matplotlib.pyplot as plt
from skimage import io
import numpy as np

vidcap = cv2.VideoCapture('vecteezy_animated-bouncing-ball-2d-motion-on-green-screen_6299150.mov')

success, frame = vidcap.read()

cv2.imwrite('Kadrs_nr0.jpg', frame)

#%%
image = io.imread('Kadrs_nr0.jpg')
io.imshow(image)

#%%


y_coord = 0
x_coord = 0
b_ball = 43
g_ball = 43
r_ball = 162

b = frame[:, :, 0]
g = frame[:, :, 1]
r = frame[:, :, 2]

ball_widths = []
previous_width = 0
equal_width_count = 0
equal_height_count = 0
ball_found = False
upper_found = False
mc_y_found = False
mc_x_found = False
mc_x_left_found = False

# Bumbiņas atrašanās vietas noteikšana
while not ball_found:
    
    # Augšējā robeža
    if r_ball in r[y_coord] and not upper_found:
        upper_bound = y_coord - 1
        upper_found = True
        
    # Centra x un y koordinātu intervāls
    elif r_ball in r[y_coord] and not mc_y_found:
        width = (r[y_coord] == r_ball).sum()
        ball_widths.append(width)
        
        if not mc_x_found:
            while not mc_x_found:
                if r[y_coord][x_coord] == r_ball and not mc_x_left_found:
                    mc_x_left = x_coord
                    mc_x_left_found = True
                if r[y_coord][x_coord] != r_ball and mc_x_left_found:
                    mc_x_right = x_coord
                    # Bumbiņas masas centra x koordināta:
                    mc_x_coord = mc_x_left + int((mc_x_right - mc_x_left)/2)
                    mc_x_found = True
                x_coord += 1
                
        if width == previous_width:
            equal_width_count += 1
            if equal_width_count == 1:
                mc_y_upper = y_coord - 1
                
        if width > previous_width:
            equal_width_count = 0
            
        if width < previous_width:
            mc_y_lower = y_coord - 1
            mc_y_found = True
            max_width = max(ball_widths)
        previous_width = width
        
    # Apakšējā robeža
    elif r_ball not in r[y_coord] and upper_found:
        lower_bound = y_coord
        ball_found = True
        
    y_coord += 1

# Bumbiņas masas centra y koordinātas aprēķināšana
mc_y_coord = mc_y_upper + int((mc_y_lower - mc_y_upper)/2)

# Zīmēšanai uz video kadra
bound_line_x = np.arange(0, len(r[y_coord]), 1)
upper_bound_line = np.full((len(r[y_coord]), 1), upper_bound)
lower_bound_line = np.full((len(r[y_coord]), 1), lower_bound)
plt.plot(bound_line_x, upper_bound_line)
plt.plot(bound_line_x, lower_bound_line)
plt.plot(mc_x_coord, mc_y_coord, '.', c='r')
plt.show()

#%%

# RGB grafiki
plt.plot(b[y_coord], c='b')
plt.plot(g[y_coord], c='g')
plt.plot(r[y_coord], c='r')
plt.show()


