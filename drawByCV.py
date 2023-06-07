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


@ray.remote
def rayCircle(coordinate):
    rayImg = np.zeros((800, 800), np.uint8)

    for i in range(NUMBER_OF_CIRCLE_RAY):
        radian = 2*math.pi * (i/NUMBER_OF_CIRCLE_RAY)

        # Shot ray
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
    array = np.array(gene).reshape(NUMBER_OF_CIRCLE, 2)

    queue = []
    for coordinate in array:
        queue.append( rayCircle.remote(coordinate) )
    
    results = ray.get(queue)
    sumRayImg = np.zeros((800, 800), np.uint8)
    for rayImg in results:
        sumRayImg = np.maximum(rayImg, sumRayImg)
    
    cv2.imshow('bwImage', img)
    cv2.imshow('rayImage', sumRayImg)
    cv2.waitKey(0)


img = cv2.imread('imageSet/room_map.png', 0)

if __name__ == "__main__":
    rayImg = np.zeros((800, 800), np.uint8)
    queue = [
        rayCircle.remote((200, 400))
    ]
    rayImg = ray.get(queue)[0]

    print(np.sum(rayImg)//255)

    cv2.imshow('bwImage', img)
    cv2.imshow('rayImage', rayImg)
    cv2.waitKey(0)