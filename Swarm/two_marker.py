import numpy as numpy
import cv2
import cv2.aruco as aruco
import math
import datetime
import time
import glob
from socket import *

i = 0
cen1 = (0, 0)
cen2 = (0, 0)
cen0 = (0, 0)
theta1 = 0
theta2 = 0
j=0
g=0
phi = 0
def distance(pt1, pt2):
    x = pt1[0] - pt2[0]
    y = pt1[1] - pt2[1]
    distance = math.sqrt(x*x + y*y)
    #print("distance: ",distance)
    return distance

def angle_calculate(pt1, pt2):

    a = pt2[0]-pt1[0]
    b = pt2[1]-pt1[1]
    angle = math.degrees(math.atan2(b, a))
    if(angle<0):
          angle =angle+360
    return int(angle)

def allignment(theta, phi, id):
    global g
    clientSocket1 = socket(AF_INET, SOCK_DGRAM)
    clientSocket1.settimeout(1)
    clientSocket2 = socket(AF_INET, SOCK_DGRAM)
    clientSocket2.settimeout(1)
    print("angle difference: ",(theta - phi))
    addr1 = ("192.168.0.120", 5007)
    addr2 = ("192.168.0.   ", 5007)

    if id == 8:
        addr = addr1
    else:
        addr = addr2

    if -10<=theta-phi<=10:
        if(g<=3):       
            clientSocket1.sendto('4'.encode(), addr)
            g=g+1
            print(4)
        else:
            clientSocket1.sendto('0'.encode(), addr)
            print(0)
    else:
        clientSocket1.sendto('2'.encode(), addr)
        print(2)

def aruco_detect(frame, robot):
    global i,j
    i = 0
    global cen2
    cen2 = (0, 0)  #for aruco9
    global cen1
    cen1 = (0, 0)  #for aruco8
    global theta1
    theta1 = 0
    global theta2
    theta2 = 0
    global phi
    global cen0
    cen0 = (0, 0)  #for goal
    goal = 0
    follower = 0

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters = aruco.DetectorParameters_create()

    corners, ids, _ = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    aruco_frame = aruco.drawDetectedMarkers(gray, corners)
    #print("corners")
    #print(len(corners))
    # if len(corners)>0:
    #     for marker in range(len(ids)):
    #         if ids[marker] == 1:    #goal id
    #             x_center = int((corners[marker][0][0][0] + corners[marker][0][1][0] + corners[marker][0][2][0] + corners[marker][0][3][0])/4)
    #             y_center = int((corners[marker][0][0][1] + corners[marker][0][1][1] + corners[markers][0][2][1] + corners[marker][0][3][1])/4)
    if len(corners)>0:
        for marker in range(len(ids)):

            #print(len(corners))
            #print(ids)
            x_center= int((corners[marker][0][0][0] + corners[marker][0][1][0] + corners[marker][0][2][0] + corners[marker][0][3][0])/4)
            y_center= int((corners[marker][0][0][1] + corners[marker][0][1][1] + corners[marker][0][2][1] + corners[marker][0][3][1])/4)

            #print(x_center, y_center)
            

            cv2.circle(frame, (x_center, y_center),2,(0,0,255),2)
            x1 = int(corners[marker][0][0][0])
            x3 = int(corners[marker][0][3][0])
            y1 = int(corners[marker][0][0][1])
            y3 = int(corners[marker][0][3][1])
            pt1 = (x3, y3)
            pt2 = (x1, y1)
            if ids[marker] == 1:
                cen0 = (x_center, y_center)
            elif ids[marker] == 8:
                cen1 = (x_center, y_center)
                theta1 = 360 - angle_calculate(pt1, pt2)
                print("theta1 ",theta1)
            elif ids[marker] == 9:
                cen2 = (x_center, y_center)
                theta2 = 360 - angle_calculate(pt1, pt2)
                print("theta2 ",theta2)

            cv2.circle(frame, pt1, 2, (0,0,255), 2)
            cv2.circle(frame,pt2, 2, (0,0,255), 2)
            #cv2.imshow('aruco_frame', frame)            
            cv2.imshow('aruco_frame', frame)
            robot[int(ids[marker])]=(int(x_center), int(y_center), int(theta))
	
        dist1 = distance(cen0, cen1)
        dist2 = distance(cen0, cen2)
        if dist1 < dist2:
            phi = angle_calculate(cen0, cen1)
            allignment(theta1, phi, 8)
            goal = 8
            follower = 9

        else:
            phi = angle_calculate(cen0, cen2)
            allignment(theta2, phi, 9)
            goal = 9
            follower = 8

        if len(ids)>1:
            if(dist>150):
                allignment(theta, phi)
                j=2
            else:
                clientSocket1 = socket(AF_INET, SOCK_DGRAM)
                clientSocket1.settimeout(1)
                addr1 = ("192.168.0.120", 5007)
                clientSocket1.sendto('4'.encode(), addr1)
        #return direction
    start = 0
    start_time_update = time.time()

    cv2.imshow("aruco_frame", frame)
    return robot
robot={}
cap = cv2.VideoCapture(2)
while(1):
     _,img_rgb = cap.read()
     robot = aruco_detect(img_rgb,robot)

     k =  cv2.waitKey(1) & 0xFF
     if k == 27:
        cap.release()
        cv2.destroyAllWindow()
        break
