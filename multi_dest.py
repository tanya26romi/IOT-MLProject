import numpy as np
import cv2
import time
import serial
from xbee import ZigBee
from xbee.helpers.dispatch import Dispatch
import math

def sendData(address, datatosend):
  	zb.send('tx', dest_addr_long = address, dest_addr = UNKNOWN, data = datatosend)
dest=[]
dest.append(([419,414],[436,439]))#,[198,351],[526,341],[518,97],[219,114]))
#cap = cv2.VideoCapture("/dev/video0")
cap = cv2.VideoCapture(1)
fourcc = cv2.cv.CV_FOURCC(*'XVID')
out0 = cv2.VideoWriter('robot_path_planning.avi', fourcc, 20.0, (640,480))
i=0
while(i<len(dest[0])):
    ret, frame = cap.read()
    frame = cv2.blur(frame,(3,3))
    img_hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # yellow color masking
    cx=0
    cy=0
    cx1=0
    cy1=0
    bool1=False
    bool2=False
    cxavg=0
    cyavg=0
    dataString="b";

    lower = np.array([18,113,115])
    upper = np.array([38,133,195])
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
            bool1=True
            cv2.circle(frame,(cx,cy),5, (0,0,255), -1)
        except Exception as e:
            bool1=False
            print("ex")


    else:
        print("sorry please put yellow color object before camera")
    #find range of Green color

    lower_g = np.array([66,80,91])
    upper_g = np.array([86,100,171])
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
            bool2=True
            cv2.circle(frame,(cx1,cy1),5, (0,255,255), -1)

            cxavg = (cx1+cx)/2
            cyavg = (cy1+cy)/2
            cv2.circle(frame,(cxavg,cyavg),5, (0,255,255), -1)
            cv2.circle(frame,(dest[0][0][0],dest[0][0][1]),5, (0,255,255), -1)
            k=1
            while(k<len(dest[0])):
                cv2.circle(frame,(dest[0][k][0],dest[0][k][1]),1, (0,255,255), -1)
                k+=1
            cv2.line(frame,(cx,cy),(dest[0][i][0],dest[0][i][1]),(255,0,255),5)
            d = math.sqrt(math.pow(cxavg-dest[0][i][0],2)+math.pow(cyavg-dest[0][i][1],2))
            temp1=math.sqrt(math.pow(dest[0][i][0]-cx1,2)+math.pow(dest[0][i][1]-cy1,2));
            temp2=math.sqrt(math.pow(cx-cx1,2)+math.pow(cy-cy1,2));
            if(d>15):
                cx2cx1diff=dest[0][i][0]-cx1
                cy2cy1diff=dest[0][i][1]-cy1
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
                i+=1;
                dataString=dataString+'5'

            PORT = '/dev/ttyUSB0'
            BAUD_RATE = 9600

            UNKNOWN = '\xff\xfe'
            WHERE = '\x00\x13\xA2\x00\x41\x5D\x87\xB3'
            #WHERE = '\x00\x13\xA2\x00\x41\x6C\x44\xE9'
            #WHERE = '\x00\x13\xA2\x00\x40\xF7\x0A\x50'

            # Open serial port
            ser = serial.Serial(PORT,BAUD_RATE)

            zb = ZigBee(ser)

            #test data sending method
            try:
                print("sending data : ",dataString)
                sendData(WHERE, dataString)
            except KeyboardInterrupt:
                break

        except Exception as e:
            bool2=False
            print("ex")


    else:

        print("sorry please put green color object before camera")

    if(bool1&bool2):
        print(cxavg,cyavg)

    out0.write(frame)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('a'):
        i=len(dest[0])
        break



cap.release()
cv2.destroyAllWindows()
