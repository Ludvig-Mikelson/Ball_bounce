#Sadalit un saglabat video bildes
#Atrast bumbinu caur krasas profilu
#Atrast apmeram bumbinas masas centru caur x liniju un y liniju 
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
    
    
while success:
    cv2.imwrite(os.path.join(kadri_folder, "frame%d.jpg" % count), frame)
    success, frame = vidcap.read() 
    count += 1
    
def ball_finder(image, rgb_low, rgb_high):
    pixels = []
    height, width, _ = image.shape
    for y in range(height):
        for x in range(width):
            pixel = image[y, x]
            if np.all(rgb_low <= pixel) and np.all(pixel <= rgb_high):
                pixels.append((x, y))
    return pixels

image_path = r'C:\Users\Deloading\Desktop\semestra\Ball_bounce\kadri\frame0.jpg'
image = cv2.imread(image_path)
lower_rgb = np.array([10, 30, 30])
upper_rgb = np.array([200, 115, 150])

points_ball = ball_finder(image,lower_rgb,upper_rgb)


x, y = zip(*points_ball)
x = np.array(x)
y = np.array(y)

fig, ax = plt.subplots()
ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
ax.scatter(x, y, color='red', marker='o', s=5)
plt.show()







        
    