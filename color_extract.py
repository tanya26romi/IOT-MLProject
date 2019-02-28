import cv2
import numpy as np

cap = cv2.VideoCapture(1)

while(1):

    #take each frame
    ret, frame = cap.read()

    #convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #define range of blue color to get any Colors
    lower = np.array([167, 152, 113])
    upper = np.array([187, 172, 193])

    #threshold the HSV image to get only any Colors
    mask = cv2.inRange(hsv, lower, upper)

    #bitwise_and mask and original image
    res = cv2.bitwise_and(frame,frame, mask=mask)

    cv2.imshow('frame',frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
