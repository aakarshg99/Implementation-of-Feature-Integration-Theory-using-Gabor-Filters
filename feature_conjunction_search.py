
# coding: utf-8

# In[3]:


import matplotlib.pyplot as plt
import sys
import time
import cv2
import numpy as np
from q1_final import generate_location_map
from q2_final import draw_image
import datetime

rt_feature = []
rt_conjunction = []

for num_obj in [5,10,15,20,25,30]:
    draw_image(num_obj, 1)    # feature search
    time1 = time.time()
    generate_location_map()
    
    with open('location_map.txt', 'r') as f:
        data = f.readlines()
    
    final_map = []
    image = cv2.imread('op.jpg', 1)

    for line in data:
        words = line.split(',')
        x = int(words[0])
        y = int(words[1])
        shape = int(words[2])
        rgb = image[y*100+50, x*100+50]
#             print (rgb)
        blue = rgb[0]
        red = rgb[2]

        if (red > 125):
            final_map.append((x,y,shape,2))   # 2 is for red

        elif (blue > 125):
            final_map.append((x,y,shape,1))   # 1 is for blue
            
    for i in final_map:
        if (i[2] == 2 and i[3] == 2):         # red square detected (odd stimulus)
            time2 = time.time()
            break

    rt_feature.append(time2-time1)

    draw_image(num_obj, 2)                    # conjunction search
    time1 = time.time()
    time.sleep(.25*num_obj)
    generate_location_map()
    
    with open('location_map.txt', 'r') as f:
        data = f.readlines()
#         final_map = []
        image = cv2.imread('op.jpg', 1)

    for line in data:
        words = line.split(',')
        x = int(words[0])
        y = int(words[1])
        shape = int(words[2])
        rgb = image[y*100+50, x*100+50]
#             print (rgb)
        blue = rgb[0]
        red = rgb[2]

        if (red > 125):
            final_map.append((x,y,shape,2))   # 2 is for red

        elif (blue > 125):
            final_map.append((x,y,shape,1))   # 1 is for blue
            
    for i in final_map:
        if (i[2] == 2 and i[3] == 2):
            time2 = time.time()
            break
            
    rt_conjunction.append(time2 - time1)
    
#         print(final_map)

plt.xlabel('Number of Objects')
plt.ylabel('Response Time')
plt.plot([5,10,15,20,25,30], rt_feature, '-bo')
plt.plot([5,10,15,20,25,30], rt_conjunction, '-rx')
plt.legend(['Feature Search', 'Conjunction Search'])
plt.show()
