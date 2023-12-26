# -*- coding: utf-8 -*-
"""
Created on Thu Dec 21 17:31:40 2023

@author: User
"""
# Pakešu imports
import cv2
import glob, os

# Video ielasīšana
vidcap = cv2.VideoCapture('SampleVideo_1280x720_1mb.mp4')
count = 0
success, image = vidcap.read()

# Jaunas mapes izveide
try:
    if not os.path.exists('kadri'):
        os.makedirs('kadri')
except OSError:
    print('Kļūda saglabājot failu')
    
# Kadru ielasīšana un saglabāšana
while success:
    cv2.imwrite("kadri//frame%d.jpg" % count, image)     # save frame as JPEG file
    success, image = vidcap.read()      
    print('Reading a new frame:', success, '; Count:', count)
    count += 1


#%%

# Failu dzēšana (ja nepieciešams)
for i in glob.glob('C://Users//Juris//Python Scripts//kadri//frame*.jpg'):
    os.remove(i)



