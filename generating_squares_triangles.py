
# coding: utf-8

# In[1]:


import numpy as np
import cv2
import time
import random
import sys
import math

def gen_rand_cell(check_cell_repeat):
#     print("Hi2")
    x = random.randint(0,7)
    y = random.randint(0,7)    

    while (check_cell_repeat[x,y] == 1):
        x = random.randint(0,7)
        y = random.randint(0,7)

    check_cell_repeat[x,y] = 1
#     print("Hi3")
#     print (x,y)
    return x,y

def draw_shape(img, check_cell_repeat, color, shape):           # color: 1 for blue, 2 for red
#     print ("Hi1")
    x,y = gen_rand_cell(check_cell_repeat)               # shape: 1 for triange, 2 for square
    red = 0
    green = 0
    blue = 0

    if (color == 1):
        red = 255

    else:
        blue = 255

    if (shape == 2):
        cv2.rectangle(img, (100*x  + 25, 100*y + 25), (100*x + 75, 100*y + 75), (red, green, blue), -1)    

    else:
        pts = np.array([[100*x + 25, 100*y + 75],[100*x + 75, 100*y + 75],[100*x + 50, 100*y + 75 - 25*math.sqrt(3)]], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.fillConvexPoly(img, pts, (red, green, blue))

def draw_image(num_obj, experiment_type):
    
#     print ("Hi 0")
    check_cell_repeat = np.zeros((8,8))
    img = np.ones((800, 800, 3), np.uint8)*255
    
    draw_shape(img, check_cell_repeat, 2, 2)            # 2,2 red square (odd stimulus)

    if (experiment_type == 1):
        even_stimulus = random.randint(1,2) # randomly deciding between red triangle and blue square
        for i in range (num_obj-1):
            if(even_stimulus==2):
                draw_shape(img, check_cell_repeat, 1, 2)          # blue square
            else:
                draw_shape(img, check_cell_repeat, 2, 1)          # red triangle

    else:
        for i in range (num_obj-1):
            draw_shape(img, check_cell_repeat, ((i+1)%2 + 1), (i%2 + 1) )  # alternating between red triangles and blue squares

    cv2.imwrite('op.jpg', img)

    location_list = []

    for x in range(8):
        for y in range(8):
            if (check_cell_repeat[x,y] == 1):
                location_list.append((x,y))

    with open('location_list.txt', 'w') as f:
        for item in location_list:
            f.write("%s, " % str(item[0]))
            f.write("%s\n" % str(item[1]))
    
#     print (check_cell_repeat)

            
if __name__ == "__main__":
    
    num_obj = int(input("Number of objects: "))
    experiment_type = int(input("Experiment Type (1 for Feature Search, 2 for Conjunction Search): "))
    
    if (num_obj > 64):
        print("Too many objects! Number of objects should not be greater than 64")
        sys.exit(1)

    if ((experiment_type != 1) and (experiment_type != 2)):
        print("Incorrect experiment type. Please try again with value 1 or 2")
        sys.exit(1)
        
#     print ("Hi-1")
    draw_image(num_obj, experiment_type)
    


