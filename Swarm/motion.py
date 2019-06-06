import numpy as numpy
import cv2
import cv2.aruco as aruco
import math
import datetime
import time
import glob

i = 0
x = (0, 0)
y = (0, 0)
theta = 0
phi = 0

def distance(pt1, pt2):
    x = pt1[0] - pt2[0]
    y = pt1[1] - pt2[1]
    distance = math.sqrt(x*x + y*y)
    print(distance)

def angle_calculate(pt1, pt2):

    a = pt2[0]-pt1[0]
    b = pt2[1]-pt1[1]
    angle = math.degrees(math.atan2(b, a))

    return int(angle)

def allignment(theta, phi):
    if 0<=theta-phi<=2:
        print("forward")
    elif 0<=phi-theta<=2:
        print("forward")
    else:
        print("right")

def aruco_detect(frame, robot):
    global i
    i = 0
    global x 
    x = (0, 0)
    global y 
    y = (0, 0)
    global theta
    theta = 0
    global phi
    phi = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()

    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    aruco_frame = aruco.drawDetectedMarkers(gray, corners)
    print("corners")
    print(len(corners))
    if len(corners)>0:
        for marker in range(len(ids)):

            print(len(corners))
            print(ids)
            x_center= int((corners[marker][0][0][0] + corners[marker][0][1][0] + corners[marker][0][2][0] + corners[marker][0][3][0])/4)
            y_center= int((corners[marker][0][0][1] + corners[marker][0][1][1] + corners[marker][0][2][1] + corners[marker][0][3][1])/4)

            print(x_center, y_center)
            

            cv2.circle(frame, (x_center, y_center),2,(0,0,255),2)
            x1 = int(corners[marker][0][0][0])
            x3 = int(corners[marker][0][3][0])
            y1 = int(corners[marker][0][0][1])
            y3 = int(corners[marker][0][3][1])
            if i == 0:
                x = (x_center, y_center)
                print("YES")
                i+=1
                y = (x_center, y_center)
            else:
                y = (x_center, y_center)


            pt1 = (x3,y3)
            pt2 = (x1,y1)
            cv2.circle(frame, pt1, 2, (0,0,255), 2)
            cv2.circle(frame,pt2, 2, (0,0,255), 2)
            cv2.imshow('aruco_frame', frame)
            if ids[marker] == 8:
                theta = angle_calculate(pt1, pt2)
                print('theta', theta)

            cv2.imshow('aruco_frame', frame)
            robot[int(ids[marker])]=(int(x_center), int(y_center), int(theta))
    
        phi = angle_calculate(x, y)
        allignment(theta, phi)
        #return direction
    start = 0
    start_time_update = time.time()

    cv2.imshow("aruco_frame", frame)
    return robot
robot={}
cap = cv2.VideoCapture(0)
while(1):
     _,img_rgb = cap.read()
     robot = aruco_detect(img_rgb,robot)

     k =  cv2.waitKey(1) & 0xFF
     if k == 27:
        cap.release()
        cv2.destroyAllWindow()
        break
