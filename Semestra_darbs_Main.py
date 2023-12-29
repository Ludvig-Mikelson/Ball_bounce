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

import cv2
import glob, os
import matplotlib.pyplot as plt
from skimage import io
import numpy as np


# Video ielasīšana
script_dir = os.path.dirname(os.path.abspath(__file__))
video_file_path = os.path.join(script_dir, 'Untitled real.mp4')

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
    
    
def ball_finder(image, rgb_low, rgb_high):
    pixels = []
    height, width, _ = image.shape
    for y in range(height):
        for x in range(width):
            pixel = image[y, x]
            if np.all(rgb_low <= pixel) and np.all(pixel <= rgb_high):
                pixels.append((x, y))
    return pixels

def ball_finder_loop(left, right, top, bot, image, rgb_low, rgb_high):
    pixels = []
    
    start_y = max(top - 150, 0)
    end_y = min(bot + 150, image.shape[0] - 1)
    
    for y in range(start_y, end_y + 1):
        for x in range(left - 10, right + 20):
            pixel = image[y, x]
            if np.all(rgb_low <= pixel) and np.all(pixel <= rgb_high):
                pixels.append((x, y))
    return pixels

def center_finder(top, bot, left, right):
    center_x = left + (right - left) / 2
    center_y = top + (bot - top) / 2
    
    
    return center_x,center_y


lower_rgb = np.array([78, 106, 20])
upper_rgb = np.array([255, 142, 62])

ball_movement_y = []
ball_movement_x =[]
time = 0


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
   
    image_test = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    points_ball = ball_finder_loop(left_ball, right_ball, top_ball, bot_ball, image_test, lower_rgb, upper_rgb)
    
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

    cv2.circle(frame, (int(center_x), int(center_y)), 5, (0, 0, 255), -1)
    trajectory_points.append((int(center_x), int(center_y)))
    
    for point in points_ball:
        cv2.circle(frame, point, 5, (0, 0, 255), -1)
        

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

fps = 200
tpf = 1/fps

real_time_full = time *tpf
real_time_set = np.linspace(0,real_time_full,time)
time_bounce = 0

max_index = np.argmax(ball_movement_y)
time_bounce = real_time_set[max_index]
Augstums = (9.81*np.square(time_bounce))/2

trajectory_points_y = [point[1] for point in trajectory_points]
trajectory_point_first = trajectory_points_y[0]

trajectory_points_x = [point[0] for point in trajectory_points]


ptm = Augstums/(ball_movement_y[max_index]-trajectory_point_first)

print(max_index)
print(real_time_full)
print(time_bounce)
print(Augstums)
print(ptm)
print(ball_movement_y[max_index]-trajectory_point_first)

velocity_array = np.gradient(trajectory_points_y, real_time_set)
acceleration_array = np.gradient(velocity_array, real_time_set)

velocity_array_x = np.gradient(trajectory_points_x, real_time_set)
acceleration_array_x = np.gradient(velocity_array_x, real_time_set)



fig, ax = plt.subplots()
ax.plot(real_time_set, np.array(trajectory_points_y) * ptm)
plt.savefig("positon.png", format="png")
plt.show()

fig, ax = plt.subplots()
ax.plot(real_time_set, np.array(velocity_array) * ptm)
plt.savefig("velocity.png", format="png")
plt.show()

fig, ax = plt.subplots()
ax.plot(real_time_set, np.array(acceleration_array) * ptm)
plt.savefig("acceleration.png", format="png")
plt.show()

fig, ax = plt.subplots()
ax.plot(real_time_set, np.array(trajectory_points_x) * ptm)
plt.savefig("positon_x.png", format="png")
plt.show()

fig, ax = plt.subplots()
ax.plot(real_time_set, np.array(velocity_array_x) * ptm)
plt.savefig("velocity_x.png", format="png")
plt.show()

fig, ax = plt.subplots()
ax.plot(real_time_set, np.array(acceleration_array_x) * ptm)
plt.savefig("acceleration_x.png", format="png")
plt.show()





        
    