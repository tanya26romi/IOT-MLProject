import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils


cap = cv2.VideoCapture(1)

while(1):


    #take each frame
    ret, frame = cap.read()

    def pick(event,x,y,flag,param):

        if(event == cv2.EVENT_LBUTTONDOWN):

            img1 = imutils.resize(frame)

            img2 = img1[197:373,181:300]  #roi of the image
            ans = []
            for y in range(0, img2.shape[0]):  #looping through each rows
                for x in range(0, img2.shape[1]): #looping through each column
                    if all(img2[y, x] != 0):
                        ans = ans + [[x, y]]
            ans = np.array(ans)
            print ans

    cv2.namedWindow('coord')
    cv2.setMouseCallback('coord',pick)

    #cv2.imshow('frame',frame)

    if cv2.waitKey(5) & 0xFF == ord('a'):
        print(cv2.waitKey(5))
        break

cap.release()
cv2.destroyAllWindows()
