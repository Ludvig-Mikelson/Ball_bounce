# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 17:31:40 2023

@author: User
"""
# Pakešu imports
import cv2
import glob, os
import matplotlib.pyplot as plt
from skimage import io
import numpy as np

# Bumbiņas RGB vērtības
b_ball = 255
g_ball = 127
r_ball = 80

range_b = range(b_ball - 1, b_ball + 1) 
range_g = range(g_ball - 1, g_ball + 1)
range_r = range(r_ball - 1, r_ball + 1)


# Funkciju definēšana

# Visa kadra RGB vērtību masīvi
def frame_rgb(frame):
    b = frame[:, :, 0]
    g = frame[:, :, 1]
    r = frame[:, :, 2]
    return r, g, b

# Bumbiņas RGB vērtību pārbaude uz dotās y līnijas
def rgb_in_line(y):
    conditions = (
        any(value in range_r for value in r[y]),
        any(value in range_g for value in g[y]),
        any(value in range_b for value in b[y]),
    )
    return all(conditions) 

# Masas centra x koordināta
def xcoord(x, y, mc_x_found, mc_x_left_found):
    if not mc_x_found:
        while not mc_x_found:
            if r[y][x] == r_ball and not mc_x_left_found:
                mc_x_left = x
                mc_x_left_found = True
            if r[y][x] != r_ball and mc_x_left_found:
                mc_x_right = x
                # Bumbiņas masas centra x koordināta:
                mc_x_coord = mc_x_left + int((mc_x_right - mc_x_left)/2)
                mc_x_found = True
                return mc_x_coord, mc_x_found
            x += 1

# Bumbiņas masas centra atrašanās vietas kadrā noteikšana
def mc_coord(x_coord, y_coord):
    
    # Sākuma parametri
    ball_widths = []
    previous_width = 0
    equal_width_count = 0
    ball_found = False
    upper_found = False
    mc_y_found = False
    mc_x_found = False
    mc_x_left_found = False
    
            
    while not ball_found:
        
        # Augšējā robeža
        if rgb_in_line(y_coord) and not upper_found:
            upper_bound = y_coord - 1
            upper_found = True
            
        # Centra x un y koordinātu intervāls
        elif rgb_in_line(y_coord) and not mc_y_found:
            width = (r[y_coord] == r_ball).sum()
            ball_widths.append(width)
                    
            if width == previous_width:
                equal_width_count += 1
                if equal_width_count == 1:
                    mc_y_upper = y_coord - 1
                    
            if width > previous_width:
                equal_width_count = 0
                
            if width < previous_width:
                mc_x_coord, mc_x_found = xcoord(x_coord, 
                                                y_coord, 
                                                mc_x_found, 
                                                mc_x_left_found)
                mc_y_lower = y_coord - 1
                mc_y_found = True
            previous_width = width
            
        # Apakšējā robeža
        elif not rgb_in_line(y_coord) and upper_found:
            lower_bound = y_coord
            ball_found = True
            
        y_coord += 1
    
    # Bumbiņas masas centra y koordināta:
    mc_y_coord = mc_y_upper + int((mc_y_lower - mc_y_upper)/2)

    return mc_x_coord, mc_y_coord, lower_bound, upper_bound

# Katra kadra parādīšana ar matplotlib
def show_frame(mc_x_coord, mc_y_coord, upper_bound, lower_bound):
    
    # Video kadra parādīšana
    image = io.imread("kadri//frame%d.jpg" % count)
    io.imshow(image)
    
    # Zīmēšanai uz video kadra
    bound_line_x = np.arange(0, len(r[y_coord]), 1)
    upper_bound_line = np.full((len(r[y_coord]), 1), upper_bound)
    lower_bound_line = np.full((len(r[y_coord]), 1), lower_bound)
    plt.plot(bound_line_x, upper_bound_line)
    plt.plot(bound_line_x, lower_bound_line)
    plt.plot(mc_x_coord, mc_y_coord, '.', c='r')
    plt.show()

# Video ielasīšana
script_dir = os.path.dirname(os.path.abspath(__file__))
video_file_path = os.path.join(script_dir, 'ar_limenradi_3.mp4')
vidcap = cv2.VideoCapture(video_file_path)
count = 0
success, frame = vidcap.read()

# Jaunas mapes izveide
kadri_folder = os.path.join(script_dir, 'kadri')
try:
    if not os.path.exists(kadri_folder):
        os.makedirs(kadri_folder)
except OSError:
    print('Kļūda saglabājot failu')
    
# Trajektorijas x un y masīvu definēšana
x_trajectory = []
y_trajectory = []

# Bumbiņas masas centra x un y koordinātu noteikšana katrā kadrā
while success:
    cv2.imwrite(os.path.join(kadri_folder, "frame%d.jpg" % count), frame)
    
    y_coord = 0
    x_coord = 0
    r, g, b = frame_rgb(frame)
    
    mc_x_coord, mc_y_coord, lower_bound, upper_bound = mc_coord(x_coord, y_coord)
    show_frame(mc_x_coord, mc_y_coord, upper_bound, lower_bound)
    
    x_trajectory = np.append(x_trajectory, mc_x_coord)
    y_trajectory = np.append(y_trajectory, mc_y_coord)
    
    success, frame = vidcap.read()      
    print('Reading a new frame:', success, '; Count:', count)
    
    if count == 25:
        success = False
    count += 1


#%%

# Failu dzēšana (ja nepieciešams)
for i in glob.glob('C://Users//Juris//Python Scripts//kadri//frame*.jpg'):
    os.remove(i)



