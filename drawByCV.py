import numpy as np
import cv2
import math

import ray

ray.shutdown()
ray.init(num_cpus=12)
# ray.init(num_cpus=10, num_gpus=16)
NUMBER_OF_CIRCLE=50
RADIUS_CIRCLE=75
NUMBER_OF_CIRCLE_RAY=250

# def shotRay(img, rayImg, radian, length, coordinate):
#     standardX = coordinate[0]
#     standardY = coordinate[1]
#     sin = math.sin(radian)
#     cos = math.cos(radian)

#     for i in range(length):
#         x = standardX + round(cos*i)
#         y = standardY + round(sin*i)
#         if (x<0)or(y<0):
#             continue
        
#         try:
#             if img.item(y, x)==0:
#                 break
#             else:
#                 rayImg.itemset(y, x, 255)
#         except Exception as e:
#             break

@ray.remote
def rayCircle(coordinate):
    rayImg = np.zeros((800, 800), np.uint8)

    for i in range(NUMBER_OF_CIRCLE_RAY):
        radian = 2*math.pi * (i/NUMBER_OF_CIRCLE_RAY)

        # shot Ray
        # shotRay(img, rayImg, radian, RADIUS_CIRCLE, coordinate)
        standardX = coordinate[0]
        standardY = coordinate[1]
        sin = math.sin(radian)
        cos = math.cos(radian)

        for i in range(RADIUS_CIRCLE):
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
    
    return rayImg

def getFitness(gene):
    array = np.array(gene).reshape(NUMBER_OF_CIRCLE, 2)

    queue = []
    for coordinate in array:
        queue.append( rayCircle.remote(coordinate) )
    
    results = ray.get(queue)
    sumRayImg = np.zeros((800, 800), np.uint8)
    for rayImg in results:
        sumRayImg = np.maximum(rayImg, sumRayImg)

    return np.sum(sumRayImg)//255

def visualize(gene):
    array = np.array(gene).astype(int).reshape(NUMBER_OF_CIRCLE, 2)
    rayImg = np.zeros((800, 800), np.uint8)

    for coordinate in array:
        rayImg = rayCircle(rayImg, coordinate)
    
    cv2.imshow('bwImage', img)
    cv2.imshow('rayImage', rayImg)
    cv2.waitKey(0)


img = cv2.imread('imageSet/room_map.png', 0)

if __name__ == "__main__":
    rayImg = np.zeros((800, 800), np.uint8)
    rayCircle(rayImg, (200, 400))

    cv2.imshow('bwImage', img)
    cv2.imshow('rayImage', rayImg)
    cv2.waitKey(0)