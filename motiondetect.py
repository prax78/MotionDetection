### Below code is courtsey of Intel [https://software.intel.com/en-us/node/754940], Please visit the site to learn more
##I have just added subprocess which will call powershell.exe whenever the motion is detected. 

import numpy as np
import cv2
import datetime
import subprocess
import threading



subprocess.run(['powershell.exe','Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Force'])

# This function will open powershell.exe whenever motion is detected, so this will open multiple instances of powershell.exe.
def logpowershell():
 t=subprocess.run(['powershell.exe','.\log_event.ps1']) 
 
 


sdThresh = 10
font = cv2.FONT_HERSHEY_SIMPLEX
#TODO: Face Detection 1

def distMap(frame1, frame2):
    """outputs pythagorean distance between two frames"""
    frame1_32 = np.float32(frame1)
    frame2_32 = np.float32(frame2)
    diff32 = frame1_32 - frame2_32
    norm32 = np.sqrt(diff32[:,:,0]**2 + diff32[:,:,1]**2 + diff32[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
    dist = np.uint8(norm32*255)
    return dist

cv2.namedWindow('frame')
cv2.namedWindow('dist')

#capture video stream from camera source. 0 refers to first camera, 1 referes to 2nd and so on.
cap = cv2.VideoCapture(0)

_, frame1 = cap.read()
_, frame2 = cap.read()

facecount = 0
while(True):
    _, frame3 = cap.read()
    rows, cols, _ = np.shape(frame3)
    cv2.imshow('dist', frame3)
    dist = distMap(frame1, frame3)

    frame1 = frame2
    frame2 = frame3

    # apply Gaussian smoothing
    mod = cv2.GaussianBlur(dist, (9,9), 0)

    # apply thresholding
    _, thresh = cv2.threshold(mod, 100, 255, 0)

    # calculate st dev test
    _, stDev = cv2.meanStdDev(mod)

    cv2.imshow('dist', mod)
    cv2.putText(frame2, "Standard Deviation - {}".format(round(stDev[0][0],0)), (70, 70), font, 1, (255, 0, 255), 1, cv2.LINE_AA)
    if stDev > sdThresh:
            print(f"Motion detected.....{datetime.datetime.now()}")
            #Since subprocess.run is blocking , so I created a thread to call logging function. you can put whatever action that you would like to see when motion is detected
            t1=threading.Thread(target=logpowershell)
            t1.start()
            
            

    cv2.imshow('frame', frame2)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()


 