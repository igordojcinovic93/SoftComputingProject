from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2 as cv
print("Required packages are available")

stream = cv.VideoCapture('D:/Fakultet/SoftProject/SoftComputingProject/assets/videos/video1.mp4')
backgroundSubtractor = cv.createBackgroundSubtractorMOG2(detectShadows = True)
while(stream.isOpened()):
    ret, frame = stream.read()
    forGround = backgroundSubtractor.apply(frame)
    ret, binForGround = cv.threshold(forGround, 200, 255, cv.THRESH_BINARY)
    frameMask = cv.morphologyEx(binForGround, cv.MORPH_OPEN, np.ones((3, 3), np.uint8))
    frameMask = cv.morphologyEx(frameMask, cv.MORPH_CLOSE, np.ones((11, 11), np.uint8))

    contours0, hierarchy = cv.findContours(frameMask,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
    for potentialCont in contours0:
        if(frame is not None):
            contourArea = cv.contourArea(potentialCont)
            if(contourArea > 50 and contourArea < 300):
                moments = cv.moments(potentialCont)
                cx = int(moments['m10']/moments['m00'])
                cy = int(moments['m01']/moments['m00'])
                cv.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
            cv.imshow('frame', frame)
        else:
            break            
    if cv.waitKey(1) & 0xFF == ord('q'):
        break


stream.release()
cv.destroyAllWindows()