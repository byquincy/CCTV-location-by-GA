import numpy as np
import cv2
import math
from multiprocessing import Pool, freeze_support

import time

NUMBER_OF_CIRCLE=50
RADIUS_CIRCLE=75

def shotRay(img, rayImg, radian, length, coordinate):
    standardX = coordinate[0]
    standardY = coordinate[1]
    sin = math.sin(radian)
    cos = math.cos(radian)

    for i in range(length):
        x = standardX + round(cos*i)
        y = standardY + round(sin*i)
        if (x<0)or(y<0):
            continue
        
        try:
            if img.item(y, x)==0:
                break
            else:
                rayImg.itemset(y, x, 255)
        except Exception as e:
            break

def rayCircle(rayImg, coordinate):
    for i in range(1080):
        radian = math.radians(i/3)
        shotRay(img, rayImg, radian, RADIUS_CIRCLE, coordinate)
    
    return rayImg

def getFitness(gene):
    array = np.array(gene).astype(int).reshape(NUMBER_OF_CIRCLE, 2)
    rayImg = np.zeros((800, 800), np.uint8)

    start = time.time()

    for coordinate in array:
        rayImg = rayCircle(rayImg, coordinate)
    
    print(time.time() - start, "\t|", np.sum(rayImg)//255)
    return np.sum(rayImg)//255

def visualize(gene):
    array = np.array(gene).astype(int).reshape(NUMBER_OF_CIRCLE, 2)
    rayImg = np.zeros((800, 800), np.uint8)

    for coordinate in array:
        rayImg = rayCircle(rayImg, coordinate)
    
    cv2.imshow('bwImage', img)
    cv2.imshow('rayImage', rayImg)
    cv2.waitKey(0)


img = cv2.imread('imageSet/room_map.png', 0)

# cv2.imshow('bwImage', img)
# cv2.imshow('rayImage', rayImg)
# cv2.waitKey(0)