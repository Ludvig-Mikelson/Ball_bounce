#Sadalit un saglabat video bildes
#Atrast bumbinu caur krasas profilu
#Atrast apmeram bumbinas masas centru caur x liniju un y liniju 
#ielikt visu programu zem viena cikla
#arpus cikla apstradat pilnu atelu
#zem cikla apstradat tikai atelu kas ir robezas ap bumbu
#

import cv2
import glob, os
import matplotlib.pyplot as plt
from skimage import io
import numpy as np

# Video ielasīšana
script_dir = os.path.dirname(os.path.abspath(__file__))
video_file_path = os.path.join(script_dir, 'daudz_gaismas_10s.mp4')
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
    
    
#while success:
   # cv2.imwrite(os.path.join(kadri_folder, "frame%d.jpg" % count), frame)
    #success, frame = vidcap.read() 
  #  count += 1
    
def ball_finder(image, rgb_low, rgb_high):
    pixels = []
    height, width, _ = image.shape
    for y in range(height):
        for x in range(width):
            pixel = image[y, x]
            if np.all(rgb_low <= pixel) and np.all(pixel <= rgb_high):
                pixels.append((x, y))
    return pixels

def ball_finder_loop(left,right,top,bot, image, rgb_low, rgb_high):
    pixels = []
    for y in range(top-40,bot+40):
        for x in range(left-20,right+20):
            pixel = image[y, x]
            if np.all(rgb_low <= pixel) and np.all(pixel <= rgb_high):
                pixels.append((x, y))
    return pixels

def center_finder(top, bot, left, right):
    center_x = left + (right - left) / 2
    center_y = top + (bot - top) / 2
    
    
    return center_x,center_y


image_path = r'C:\Users\Deloading\Desktop\semestra\Ball_bounce\kadri\frame0.jpg'
image = cv2.imread(image_path)
image_test = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
lower_rgb = np.array([90, 105, 10])
upper_rgb = np.array([255, 195, 70])

points_ball = ball_finder(image_test,lower_rgb,upper_rgb)


x, y = zip(*points_ball)
x = np.array(x)
y = np.array(y)

left_ball = np.min(x)
right_ball = np.max(x)
top_ball = np.min(y)
bot_ball = np.max(y)

center_x,center_y = center_finder(top_ball,bot_ball,left_ball,right_ball)

print("Top:", top_ball)
print("Bottom:", bot_ball)
print("Left:", left_ball)
print("Right:", right_ball)


image_cut = image[top_ball:bot_ball,left_ball:right_ball]
fig, ax = plt.subplots()
ax.imshow(cv2.cvtColor(image_cut, cv2.COLOR_BGR2RGB))
ax.scatter(x,y, color='red', marker='o', s=5)
ax.scatter(center_x,center_y, color='blue', marker='o', s=5)
plt.show()

ball_movement_y = []
ball_movement_x =[]
time = 0

for frame_number in range(263):
    image_path = f'C:\\Users\\Deloading\\Desktop\\semestra\\Ball_bounce\\kadri\\frame{frame_number}.jpg'
    
    image = cv2.imread(image_path)
    image_test = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    points_ball = ball_finder_loop(left_ball,right_ball,top_ball,bot_ball,image_test,lower_rgb, upper_rgb)
    
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
    
    #fig, ax = plt.subplots()
    #image_cut = image[top_ball:bot_ball,left_ball:right_ball]
    #ax.imshow(cv2.cvtColor(image_cut, cv2.COLOR_BGR2RGB))
    #ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    #ax.scatter(x,y, color='red', marker='o', s=5)
    #ax.scatter(center_x,center_y, color='blue', marker='o', s=5)
    #plt.show()

fig, ax = plt.subplots()
ax.plot(np.linspace(0, time-1, time), ball_movement_y)
plt.show()








        
    