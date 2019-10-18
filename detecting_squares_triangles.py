
# coding: utf-8

# In[3]:


import numpy as np
import cv2
import time

def img_thres(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def generate_location_map():
    image = cv2.imread('op.jpg', 0)
    image = img_thres(image)

    kernel = cv2.getGaborKernel((8, 8), sigma=3, theta=0, lambd=5.0, gamma=0, psi=0)
    temp_image_vert = cv2.filter2D(image, 0, kernel)
    temp_image_vert = img_thres(temp_image_vert)
    cv2.imwrite('op_gabor_vert.jpg', temp_image_vert)

    kernel = cv2.getGaborKernel((8, 8), sigma=3, theta=np.pi/2, lambd=5.0, gamma=0, psi=0)
    temp_image_horiz = cv2.filter2D(image, 0, kernel)
    temp_image_horiz = img_thres(temp_image_horiz)
    cv2.imwrite('op_gabor_horiz.jpg', temp_image_horiz)

    kernel = cv2.getGaborKernel((8, 8), sigma=3, theta=np.pi/6, lambd=2.9, gamma=0, psi=0)
    temp_image_slant30 = cv2.filter2D(image, 0, kernel)
    temp_image_slant30 = img_thres(temp_image_slant30)
    cv2.imwrite('op_gabor_slant30.jpg', temp_image_slant30)

    kernel = cv2.getGaborKernel((8, 8), sigma=3, theta=5*np.pi/6, lambd=2.9, gamma=0, psi=0)
    temp_image_slant150 = cv2.filter2D(image, 0, kernel)
    temp_image_slant150 = img_thres(temp_image_slant150)
    cv2.imwrite('op_gabor_slant150.jpg', temp_image_slant150)

    alpha = 0.5
    temp_image = temp_image_vert + temp_image_horiz + temp_image_slant30 + temp_image_slant150
    temp_image = img_thres(temp_image)

    cv2.imwrite('op_gabor.jpg', temp_image)

    location_map = []

    with open('location_list.txt', 'r') as f:
        data = f.readlines()

        for line in data:
            words = line.split(',')
            x = int(words[0])
            y = int(words[1])
            img = temp_image[y*100:(y+1)*100, x*100:(x+1)*100]

            image_cont, contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

            if (len(contours) > 5):
                location_map.append((x,y,2))       # 2 is for square

            else:
                location_map.append((x,y,1))       # 1 is for triangle

    with open('location_map.txt', 'w') as f:
        for item in location_map:
            f.write("%s, " % str(item[0]))
            f.write("%s, " % str(item[1]))
            f.write("%s\n" % str(item[2]))
            
if __name__ == "__main__":
    generate_location_map()

