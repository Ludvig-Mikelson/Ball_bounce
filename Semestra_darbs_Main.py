# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 16:50:38 2023

@author: Juris
"""

#Sadalit un saglabat video bildes
#Atrast bumbinu caur krasas profilu
#Atrast apmeram bumbinas masas centru caur x liniju un y liniju 
#ielikt visu programu zem viena cikla
#arpus cikla apstradat pilnu atelu
#zem cikla apstradat tikai atelu kas ir robezas ap bumbu
#salikt framus atpakal video
#uz video uzzimet gan masas centra trajektoriju gan visus bumbinas punktus (iztiks bez punktiem)
#salikt kodu pec iespejas kompaktat iskatas ka visu var izdarit caur video while ciklu
#atrast laiku per frame
#atrast atalumu per pixel
#atvasinat atrumu un patrinajumu
#saglabat pdf failos
#sagriezt video lai bumba tiek uzreiz atlaista
#

#Sadalit un saglabat video bildes
#Atrast bumbinu caur krasas profilu
#Atrast apmeram bumbinas masas centru caur x liniju un y liniju 
#ielikt visu programu zem viena cikla
#arpus cikla apstradat pilnu atelu
#zem cikla apstradat tikai atelu kas ir robezas ap bumbu
#salikt framus atpakal video
#uz video uzzimet gan masas centra trajektoriju gan visus bumbinas punktus (iztiks bez punktiem)
#salikt kodu pec iespejas kompaktat iskatas ka visu var izdarit caur video while ciklu
#atrast laiku per frame
#atrast atalumu per pixel
#atvasinat atrumu un patrinajumu
#saglabat pdf failos
#sagriezt video lai bumba tiek uzreiz atlaista
#salabot augstuma noteiksanu
#sarakstit grafikos fps,izmesanas augstumu.

import cv2
import glob, os
import matplotlib.pyplot as plt
from skimage import io
import numpy as np
from scipy.signal import argrelextrema


# Video ielasīšana
script_dir = os.path.dirname(os.path.abspath(__file__))
video_file_path = os.path.join(script_dir, 'daudz_gaismas.mp4')

vidcap = cv2.VideoCapture(video_file_path)
count = 0
success, frame = vidcap.read()

#Finds position of the ball in the first frame by going trough the whole image    
def ball_finder(image, rgb_low, rgb_high):
    pixels = []
    height, width, _ = image.shape
    for y in range(height):
        for x in range(width):
            pixel = image[y, x]
            if np.all(rgb_low <= pixel) and np.all(pixel <= rgb_high):
                pixels.append((x, y))
    return pixels
#Using info about previous position of the ball looks for the ball in a limited area
def ball_finder_loop(left, right, top, bot, image, rgb_low, rgb_high):
    pixels = []
    
    #makes sure that ball is looked for within dimensions of image
    end_y = min(bot + 80, image.shape[0])
    end_x = min(right + 10, image.shape[1])
    
    for y in range(top -50, end_y):
        for x in range(left - 10, end_x):
            pixel = image[y, x]
            if np.all(rgb_low <= pixel) and np.all(pixel <= rgb_high):
                pixels.append((x, y))
    return pixels
#Finds the center coordinates given 4 points
def center_finder(top, bot, left, right):
    center_x = left + (right - left) / 2
    center_y = top + (bot - top) / 2
    
    return center_x,center_y

#RGB range for ball finder fucntions 
lower_rgb = np.array([167, 10, 10])
upper_rgb = np.array([255, 150, 80])

ball_movement_y = []
ball_movement_x =[]
time = 0

#defining variables for while loop to use
output_video_path = os.path.join(script_dir, 'testo.mp4')
fps = vidcap.get(cv2.CAP_PROP_FPS)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (int(vidcap.get(3)), int(vidcap.get(4))))

count = 0
success, frame = vidcap.read()

image_test = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
points_ball = ball_finder(image_test, lower_rgb, upper_rgb)
x, y = zip(*points_ball)
x = np.array(x)
y = np.array(y)
left_ball = np.min(x)
right_ball = np.max(x)
top_ball = np.min(y)
bot_ball = np.max(y)

trajectory_points = []

while success:
    #Changes the color from BGR to RGB, because old cameras
    image_test = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    points_ball = ball_finder_loop(left_ball, right_ball, top_ball, bot_ball, image_test, lower_rgb, upper_rgb)
    
    #Finds the top,bot,left,right most points from all the points for center finder.
    x, y = zip(*points_ball)
    x = np.array(x)
    y = np.array(y)

    left_ball = np.min(x)
    right_ball = np.max(x)
    top_ball = np.min(y)
    bot_ball = np.max(y)

    center_x, center_y = center_finder(top_ball, bot_ball, left_ball, right_ball)
    
    ball_movement_y.append(center_y)
    ball_movement_x.append(center_x)
    time += 1
    
    #Draws the found mass center on the frame 
    cv2.circle(frame, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)
    
    #Either this or ball_movement_y/x is not needed, but both are being used at this point
    trajectory_points.append((int(center_x), int(center_y)))
    
    #draws all of the points associated with the ball
    for point in points_ball:
        cv2.circle(frame, point, 5, (0, 0, 255), -1)
        
    #Draws line connecting all of the previous positions of mass center 
    for i in range(1, len(trajectory_points)):
        cv2.line(frame, trajectory_points[i - 1], trajectory_points[i], (255, 0, 0), 2)

    out.write(frame)

    success, frame = vidcap.read()
    
    count += 1

out.release()
cv2.destroyAllWindows()

fig, ax = plt.subplots()
ax.plot(np.linspace(0, time-1, time), ball_movement_y)
plt.show()

#Finds time per frame given recording fps (playback fps doesn't matter)
fps = 200
tpf = 1/fps


real_time_full = time *tpf
real_time_set = np.linspace(0,real_time_full,time)
time_bounce = 0

peak_index = argrelextrema(np.array(ball_movement_y), np.greater)

max_index = peak_index[0][0] if peak_index[0].size > 0 else None
time_bounce = real_time_set[max_index]
#Finds height from which the ball was released given idealized conditions
Augstums = (9.81*np.square(time_bounce))/2

trajectory_points_y = [point[1] for point in trajectory_points]
trajectory_point_first = trajectory_points_y[0]
trajectory_points_x = [point[0] for point in trajectory_points]

#Finds how many meters are per pixel
ptm = Augstums/(ball_movement_y[max_index]-trajectory_point_first)

print(max_index)
print(real_time_full)
print(time_bounce)
print(Augstums)
print(ptm)
print(ball_movement_y[max_index]-trajectory_point_first)

#Derives velocity and acceleration from y and x position sets and time set.
velocity_array = np.gradient(trajectory_points_y, real_time_set)
acceleration_array = np.gradient(velocity_array, real_time_set)

velocity_array_x = np.gradient(trajectory_points_x, real_time_set)
acceleration_array_x = np.gradient(velocity_array_x, real_time_set)

#%%

#%%

#Plots and converts from pixels to meters
fig, ax = plt.subplots()
ax.plot(real_time_set, np.array(trajectory_points_y) * ptm)
plt.savefig("positon.png", format="png")
plt.title('Atrašanās vieta $y(t)$')
plt.xlabel('$t, s$')
plt.ylabel('$y, m$')
plt.show()

fig, ax = plt.subplots()
ax.plot(real_time_set, np.array(velocity_array) * ptm)
plt.savefig("velocity.png", format="png")
plt.title('Ātrums $v_y(t)$')
plt.xlabel('$t, s$')
plt.ylabel('$v_y, m/s$')
plt.show()

fig, ax = plt.subplots()
ax.plot(real_time_set, np.array(acceleration_array) * ptm)
plt.savefig("acceleration.png", format="png")
plt.title('Paātrinājums $a_y(t)$')
plt.xlabel('$t, s$')
plt.ylabel('$a_y, m/s^2$')
plt.show()

fig, ax = plt.subplots()
ax.plot(real_time_set, np.array(trajectory_points_x) * ptm)
plt.savefig("positon_x.png", format="png")
plt.title('Atrašanās vieta $x(t)$')
plt.xlabel('$t, s$')
plt.ylabel('$x, m$')
plt.show()

fig, ax = plt.subplots()
ax.plot(real_time_set, np.array(velocity_array_x) * ptm)
plt.savefig("velocity_x.png", format="png")
plt.title('Ātrums x virzienā $v_x(t)$')
plt.xlabel('$t, s$')
plt.ylabel('$v_x, m/s$')
plt.show()

fig, ax = plt.subplots()
ax.plot(real_time_set, np.array(acceleration_array_x) * ptm)
plt.savefig("acceleration_x.png", format="png")
plt.title('Paātrinājums x virzienā $a_x(t)$')
plt.xlabel('$t, s$')
plt.ylabel('$a_x, m/s^2$')
plt.show()

