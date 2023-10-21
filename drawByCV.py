import numpy as np
import cv2
import math

import ray
import os

ray.shutdown()
# ray.init(num_cpus=12)
ray.init(num_cpus=10, num_gpus=16)
NUMBER_OF_CIRCLE=50
RADIUS_CIRCLE=75
NUMBER_OF_CIRCLE_RAY=250
BASE_DIR=os.path.dirname(os.path.abspath(__file__))

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

def makeRayimage(gene):
    array = np.array(gene).reshape(NUMBER_OF_CIRCLE, 2)

    queue = []
    for coordinate in array:
        queue.append( rayCircle.remote(coordinate) )
    
    results = ray.get(queue)
    sumRayImg = np.zeros((800, 800), np.uint8)
    for rayImg in results:
        sumRayImg = np.maximum(rayImg, sumRayImg)
    
    return sumRayImg

def getFitness(gene):
    return np.sum(makeRayimage(gene))//255

def visualize(gene):
    rayImage = makeRayimage(gene)
    
    print(np.sum(rayImage)//255)
    cv2.imshow('bwImage', img)
    cv2.imshow('rayImage', rayImage)
    cv2.waitKey(0)

def saveRay(gene, fileName=BASE_DIR+"/savedImage.png"):
    rayImage = makeRayimage(gene)

    cv2.imwrite(fileName, rayImage)


img = None
def setFilePath(filePath):
    global img

    os.chdir(filePath)
    img = cv2.imread('room_map.png', 0)


if __name__ == "__main__":
    data = [716,29,198,571,298,487,568,245,442,609,493,190,163,286,667,135,571,20,599,389,267,721,58,774,39,545,657,571,691,613,121,683,203,482,640,90,493,310,348,154,97,574,48,246,61,685,596,745,503,305,394,59,684,506,334,332,138,799,385,495,789,694,61,122,768,160,530,641,514,488,61,258,682,310,20,133,576,398,367,300,186,605,728,69,77,385,561,154,642,586,117,585,223,409,630,726,558,318,524,354]
    setFilePath(BASE_DIR +"/imageSet" )
    visualize(data)