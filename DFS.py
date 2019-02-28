import numpy as np
import cv2
import time
import serial
from xbee import ZigBee
from xbee.helpers.dispatch import Dispatch
import math
import sys

cap = cv2.VideoCapture(1)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out0 = cv2.VideoWriter('DFS.avi', fourcc, 20.0, (640,480))
def sendData(address, datatosend,a,zb):
  	zb.send('tx', dest_addr_long = address, dest_addr =a, data = datatosend)
def travelBotTo(dest):
    print("called travel Bot to")
    print(dest)
    # k=0
    # t_end = time.time() + 60 *0.1
    # while time.time() < t_end:
    #     k+=1

    rchdest=False
    while(True):
        ret, frame = cap.read()
        frame = cv2.blur(frame,(3,3))
        img_hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # yellow color masking
        cx=0
        cy=0
        cx1=0
        cy1=0
        cxavg=0
        cyavg=0
        dataString="b";
        lower = np.array([20,88,162])
        upper = np.array([40,108,242])

        mask_test=cv2.inRange(img_hsv,lower,upper)
        contours, hierarchy = cv2.findContours(mask_test, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        idx = 0
        max_area=0
        best_cnt=0
        if(len(contours)>0):
            for cnt in contours:
              area = cv2.contourArea(cnt)
              if(area>max_area):
                  max_area=area
                  best_cnt=cnt
            M = cv2.moments(best_cnt)

            try:
                cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
                cv2.circle(frame,(cx,cy),5, (0,0,255), -1)
            except Exception as e:
                print("ex")


        else:
            print("sorry please put yellow color object before camera")
        #find range of Green color
        lower_g = np.array([70,76,93])
        upper_g = np.array([90,96,173])
        mask_test=cv2.inRange(img_hsv,lower_g,upper_g)
        contours, hierarchy = cv2.findContours(mask_test, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        idx = 0
        max_area=0
        best_cnt=0
        if(len(contours)>0):
            for cnt in contours:
              area = cv2.contourArea(cnt)
              if(area>max_area):
                  max_area=area
                  best_cnt=cnt
            M = cv2.moments(best_cnt)

            try:
                cx1,cy1 = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
                cv2.circle(frame,(cx1,cy1),5, (0,255,255), -1)

                cxavg = (cx1+cx)/2
                cyavg = (cy1+cy)/2
                cv2.circle(frame,(cxavg,cyavg),5, (0,255,255), -1)
                cv2.circle(frame,(dest[0],dest[1]),5, (0,255,255), -1)
                cv2.line(frame,(cx,cy),(dest[0],dest[1]),(255,0,255),5)
                d = math.sqrt(math.pow(cxavg-dest[0],2)+math.pow(cyavg-dest[1],2))
                temp1=math.sqrt(math.pow(dest[0]-cx1,2)+math.pow(dest[1]-cy1,2));
                temp2=math.sqrt(math.pow(cx-cx1,2)+math.pow(cy-cy1,2));
                if(d>15):
                    cx2cx1diff=dest[0]-cx1
                    cy2cy1diff=dest[1]-cy1
                    cycy1diff=cy-cy1
                    cxcx1diff=cx-cx1
                    diff1=cx2cx1diff*cycy1diff
                    diff2=cy2cy1diff*cxcx1diff
                    z=diff1-diff2
                    tmp=temp1*temp2
                    result=z/tmp #sin thita
                    print(result)
                    print(z)
                    if all([result<0.183,result>-0.113]):
                        dataString=dataString+'2'
                    elif(z<0):
                        dataString=dataString+'4'
                    elif(z>0):
                        dataString=dataString+'1'
                    else:
                        dataString=dataString+'5'
                else:
                    rchdest=True
                    dataString=dataString+'5'

                PORT = '/dev/ttyUSB0'
                BAUD_RATE = 9600

                UNKNOWN = '\xff\xfe'
                #WHERE = '\x00\x13\xA2\x00\x41\x6C\x44\xE9'
                WHERE = '\x00\x13\xA2\x00\x41\x5D\x87\xB3'
                #WHERE = '\x00\x13\xA2\x00\x40\xF7\x0A\x50'

                # Open serial port
                ser = serial.Serial(PORT,BAUD_RATE)

                zb = ZigBee(ser)

                #test data sending method
                try:
                    print("sending data : ",dataString)
                    sendData(WHERE, dataString,UNKNOWN,zb)
                except KeyboardInterrupt:
                    break

            except Exception as e:
                print("ex")


        else:

            print("sorry please put green color object before camera")
        if(rchdest==True):
            break;
        out0.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('a'):
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()
            break

def travelBotBackTo(dest):
    print("called travel Bot to")
    print(dest)
    # k=0
    # t_end = time.time() + 60 *0.1
    # while time.time() < t_end:
    #     k+=1

    rchdest=False
    while(True):
        ret, frame = cap.read()
        frame = cv2.blur(frame,(3,3))
        img_hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # yellow color masking
        cx=0
        cy=0
        cx1=0
        cy1=0
        cxavg=0
        cyavg=0
        dataString="b";

        lower = np.array([20,88,162])
        upper = np.array([40,108,242])
        mask_test=cv2.inRange(img_hsv,lower,upper)
        contours, hierarchy = cv2.findContours(mask_test, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        idx = 0
        max_area=0
        best_cnt=0
        if(len(contours)>0):
            for cnt in contours:
              area = cv2.contourArea(cnt)
              if(area>max_area):
                  max_area=area
                  best_cnt=cnt
            M = cv2.moments(best_cnt)

            try:
                cx,cy = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
                cv2.circle(frame,(cx,cy),5, (0,0,255), -1)
            except Exception as e:
                print("ex")


        else:
            print("sorry please put yellow color object before camera")


        #find range of Green color

        lower_g = np.array([70,76,93])
        upper_g = np.array([90,96,173])
        mask_test=cv2.inRange(img_hsv,lower_g,upper_g)
        contours, hierarchy = cv2.findContours(mask_test, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        idx = 0
        max_area=0
        best_cnt=0
        if(len(contours)>0):
            for cnt in contours:
              area = cv2.contourArea(cnt)
              if(area>max_area):
                  max_area=area
                  best_cnt=cnt
            M = cv2.moments(best_cnt)


            try:
                cx1,cy1 = int(M['m10']/M['m00']), int(M['m01']/M['m00'])
                cv2.circle(frame,(cx1,cy1),5, (0,255,255), -1)

                cxavg = (cx1+cx)/2
                cyavg = (cy1+cy)/2
                cv2.circle(frame,(cxavg,cyavg),5, (0,255,255), -1)
                cv2.circle(frame,(dest[0],dest[1]),5, (0,255,255), -1)
                cv2.line(frame,(cx1,cy1),(dest[0],dest[1]),(255,0,255),5)
                d = math.sqrt(math.pow(cxavg-dest[0],2)+math.pow(cyavg-dest[1],2))
                temp1=math.sqrt(math.pow(dest[0]-cx1,2)+math.pow(dest[1]-cy1,2));
                temp2=math.sqrt(math.pow(cx-cx1,2)+math.pow(cy-cy1,2));
                if(d>15):
                    cx2cx1diff=dest[0]-cx
                    cy2cy1diff=dest[1]-cy
                    cycy1diff=cy1-cy
                    cxcx1diff=cx1-cx
                    diff1=cx2cx1diff*cycy1diff
                    diff2=cy2cy1diff*cxcx1diff
                    z=diff1-diff2
                    tmp=temp1*temp2
                    result=z/tmp #sin thita
                    print(result)
                    print(z)
                    if all([result<0.183,result>-0.113]):
                        dataString=dataString+'3'
                    elif(z<0):
                        dataString=dataString+'4'
                    elif(z>0):
                        dataString=dataString+'1'
                    else:
                        dataString=dataString+'5'
                else:
                    rchdest=True
                    dataString=dataString+'5'

                PORT = '/dev/ttyUSB0'
                BAUD_RATE = 9600

                UNKNOWN = '\xff\xfe'
                #WHERE = '\x00\x13\xA2\x00\x41\x6C\x44\xE9'
                WHERE = '\x00\x13\xA2\x00\x41\x5D\x87\xB3'
                #WHERE = '\x00\x13\xA2\x00\x40\xF7\x0A\x50'

                # Open serial port
                ser = serial.Serial(PORT,BAUD_RATE)

                zb = ZigBee(ser)

                #test data sending method
                try:
                    print("sending data : ",dataString)
                    sendData(WHERE, dataString,UNKNOWN,zb)
                except KeyboardInterrupt:
                    break

            except Exception as e:
                print("ex")


        else:

            print("sorry please put green color object before camera")
        if(rchdest==True):
            break;
        out0.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('a'):
            cap.release()
            cv2.destroyAllWindows()
            sys.exit()
            break

def moveMyBotInNetwork(dest_points,net,source,destination,stk,visited):
    if(source==destination):
        print("destination reached dude")
        cap.release()
        cv2.destroyAllWindows()
        sys.exit()

    search=0
    indx_source=0
    indx_destination=0
    while(search<len(dest_points[0])):
        if(dest_points[0][search]==source[0]):
            indx_source=search
        search+=1
    visited[indx_source]=True
    stk.append(([source[0][0],source[0][1]]))
    print(visited)
    i=0
    while(i<len(net[0])):
        if(net[indx_source][i]==1 and visited[i]==False):
            travelBotTo(dest_points[0][i])
            l=[]
            l.append((dest_points[0][i]))
            moveMyBotInNetwork(dest_points,net,l,destination,stk,visited)
        i+=1

    stk.pop(len(stk)-1)
    travelBotBackTo(stk[len(stk)-1])

def moveMyBot(dest_points,net,source,destination,stk):
    i=0
    visited=[]
    while(i<len(dest_points[0])):
        visited.append(False)
        i+=1
    moveMyBotInNetwork(dest_points,net,source,destination,stk,visited)

dest_points=[]
dest_points.append(([219,114],[136,239],[198,351],[526,341],[518,97]))
#dest_points.append(([519,114]))#,[526,341],[518,697]))
net=[]
net=np.genfromtxt("net.txt",delimiter=",")
# Ax = input("enter x coordinate of the starting point")
# Ay = input("enter y coordinate of the starting point")
# Dx = input("enter x coordinate of the destination point")
# Dy = input("enter y coordinate of the destination point")
source=[]
source.append((dest_points[0][0]))
destination=[]
destination.append((dest_points[0][len(dest_points[0])-2]))
stk = []
moveMyBot(dest_points,net,source,destination,stk)
