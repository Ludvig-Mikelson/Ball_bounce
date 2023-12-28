import cv2
import glob, os
import matplotlib.pyplot as plt
from skimage import io
import numpy as np



# Video ielasīšana
script_dir = os.path.dirname(os.path.abspath(__file__))
video_file_path = os.path.join(script_dir, 'time_be_told.mp4')
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