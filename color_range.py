import cv2
import numpy as np

image_hsv = None
#pixel = (10,20,)
#declare variables for windows
vc = cv2.VideoCapture(1)

while(1):
    #take each frame
    ret, frame = vc.read()
    #image_hsv = None
    #pixel = (20,60,80)  #random default
    #pixel = (20,60,80) #some random default

    #mouse callback function
    def pick_color(event,x,y,flags,param):
        #if event == cv2.EVENT_LBUTTONDBLCLK:
        if(event == cv2.EVENT_LBUTTONDOWN):
            pixel = image_hsv[y,x]

            #image adjustment
            upper = np.array([pixel[0] + 10, pixel[1] + 10, pixel[2] + 40])
            lower = np.array([pixel[0] - 10, pixel[1] - 10, pixel[2] - 40])
            print(lower, upper)
            #print(pixel, lower, upper)

            image_mask = cv2.inRange(image_hsv, lower,upper)
            cv2.imshow("mask",image_mask)
            #cv2.imshow('frame',frame)


    #global image_hsv, pixel
    cv2.namedWindow('hsv')
    cv2.setMouseCallback('hsv',pick_color)
    #now click into the hsv img,and look at values:
    image_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow("hsv",image_hsv)
    #cv2.imshow('frame',frame)
    #cv2.imshow('mask',image_mask)
    if cv2.waitKey(5) & 0xFF == 27:
        break
vc.release()
cv2.destroyAllWindows()
#sys.exit(0)
