from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2 as cv
import model
print("Required packages are available")

def getDimensions(frame):
    height = frame.get(4)
    width = frame.get(3)
    bottomBorder = int(height*0.25)
    topBorder = int(height*0.9)
    leftBorder = int(5*(width/16))
    rightBorder = int(11*(width/16))
    return height, width, bottomBorder, topBorder, leftBorder, rightBorder

def calculateCentroid(contour):
    moments = cv.moments(contour)
    x = int(moments['m10']/moments['m00']) #xCoord center calculation by contour moments by mathematical formula shown on openCv Docs
    y = int(moments['m01']/moments['m00']) #yCoord center calculation by contour moments by mathematical formula shown on openCv Docs 
    return x, y

def removeNoiseFromFrame(frame):
    oKernel = np.ones((3, 3), np.uint8)
    cKernel = np.ones((11, 11), np.uint8)
    frameMask = cv.morphologyEx(frame, cv.MORPH_OPEN, oKernel) #Noise reduction
    frameMask = cv.morphologyEx(frameMask, cv.MORPH_CLOSE, cKernel) #Object blobing
    return frameMask

i = 1
while(i < 11):    
    detectedObjects = []
    pedestriansCrossed = []

    stream = cv.VideoCapture('D:/Fakultet/SoftProject/SoftComputingProject/assets/videos/video' + str( i ) + '.mp4')    

    platoeHeight, platoeWidth, platoeBottomSide, platoeTopSide, _, _ = getDimensions(stream)

    backgroundSubtractor = cv.createBackgroundSubtractorMOG2(detectShadows = True) #static background subtraction with shadow detection
    
    while(stream.isOpened()):
        _, frame = stream.read()
        if(frame is not None):
            forGround = backgroundSubtractor.apply(frame)   #Extracting moving objects in frames
            _, binForGround = cv.threshold(forGround, 200, 255, cv.THRESH_BINARY) #Thresholding function to ease noise reduction
            frameMask = removeNoiseFromFrame(binForGround)
            foundContours, _ = cv.findContours(frameMask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE) #Find outer most contures of objects and compress them to 4 point rectangles
            for potentialCont in foundContours:            
                    contourArea = cv.contourArea(potentialCont)
                    if(contourArea > 25 and contourArea < 300):
                        cx, cy = calculateCentroid(potentialCont)  
                        x, y, w, h = cv.boundingRect(potentialCont) #Bounding rectangle, smallest square area around the detected contour
                        cv.rectangle(frame, (x, y), (x + w, y + w), (0, 255, 0), 1)
                        newPedestrian = True                        
                        for o in detectedObjects:
                            if abs(x - o.getXCoord()) <= 25 and abs(y - o.getYCoord()) <= 35: #Check if current object distance is close enough to coords of any previously detected objects
                                o.setAge()  #Increment object age so that we can distinguish flash noise from constant moving objects
                                newPedestrian = False
                                o.updatePosition(cx, cy)                       
                                break                     
                        if newPedestrian == True:
                            pedestrian = model.Pedestrian(cx, cy, 0)
                            detectedObjects.append(pedestrian)
                    cv.imshow('frame', frame)
            for detectedObj in detectedObjects:            
                if detectedObj.getAge() > 15:
                    if detectedObj not in pedestriansCrossed:
                        if detectedObj.getYCoord()  >= platoeBottomSide and detectedObj.getYCoord() <= platoeTopSide: #Check if moving object was at any time inside the boundries of the wanted area
                            pedestriansCrossed.append(detectedObj)
        else:
            break            
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    print("Number of pedestrians in video-" + str(i) + " is: " + str(len(pedestriansCrossed)))
    stream.release()
    cv.destroyAllWindows()
    i += 1