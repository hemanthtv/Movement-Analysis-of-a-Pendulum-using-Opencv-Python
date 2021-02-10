'''importing  Necessary Libraries'''

import numpy as np
import cv2
import math

cap=cv2.VideoCapture("hd1618.mov")
frame_counter=0

'''Saving audio clip'''
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('finaloutput.mp4', 0x7634706d, 20.0, (700,500))
hsv1 = cv2.VideoWriter('hsv.mp4', 0x7634706d, 20.0, (700,500))
sat = cv2.VideoWriter('sat.mp4', 0x7634706d, 20.0, (700,500))
med = cv2.VideoWriter('med.mp4', 0x7634706d, 20.0, (700,500))
'''Gradient Function'''
def gradient(pt1,pt2):
    return (pt2[1]-pt1[1])/(pt2[0]-pt1[0])

while True:
    _,rawImage=cap.read()
    rawImage = cv2.resize(rawImage, (700, 500))

    '''loop_back video when its end'''
    frame_counter += 1
    '''If the last frame is reached, reset the capture and the frame_counter'''
    if frame_counter == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        frame_counter = 0  # Or whatever as long as it is the same as next line
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


    '''Changiing Colour Space BGR2HSV'''
    hsv = cv2.cvtColor(rawImage, cv2.COLOR_BGR2HSV)
    hsv=cv2.resize(hsv,(700,500))
    hsv1.write(hsv)
    cv2.imshow('HSV Image',hsv)


    '''Extracting Only Saturation Channel Since it shows amount of white content from frame which indirectly points out Objects'''
    hue ,saturation ,value = cv2.split(hsv)
    saturation = cv2.resize(saturation, (700, 500))
    hue= cv2.resize(hue, (700, 500))
    value= cv2.resize(value, (700, 500))
    sat.write(saturation)
    # cv2.imshow('hue',hue)
    cv2.imshow('Saturation Image', saturation)
    # cv2.imshow('Value', value)


    '''Applying Threshold to the frame to convert into Binary format'''
    retval, thresholded = cv2.threshold(saturation, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    thresholded = cv2.resize(thresholded, (700, 500))
    cv2.imshow('Thresholded Image',thresholded)


    '''Applying MedianBlur to reduce Noice'''
    medianFiltered = cv2.medianBlur(thresholded,5)
    medianFiltered = cv2.resize(medianFiltered, (700, 500))
    med.write(medianFiltered)
    cv2.imshow('Median Filtered Image',medianFiltered)


    '''Finding Contours in MedianFiltered'''
    contours, hierarchy = cv2.findContours(medianFiltered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contour_list = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 200 :
            contour_list.append(contour)

    (x1, y1), rad = cv2.minEnclosingCircle(contours[1])
    cv2.line(rawImage,(350,0),(350,500),(255,255,255),1)

    '''Finding Angle and Distance made by the centre with Vertical Line'''
    pt1 = [350, 0]
    pt2 = [int(x1), int(y1)]
    m2 = gradient(pt1, pt2)
    angR = math.atan(m2)
    angD = round(math.degrees(angR))
    if angD>0:
        angD=90-angD
    else:
        angD=90+angD
    if (int(x1) < 350):
        distance = 350-int(x1)
    else:
        distance = int(x1) - 350
    j=0
    '''for i in range(350,700,10):
        cv2.putText(rawImage,str(j),(i,30),cv2.FONT_HERSHEY_SIMPLEX,0.2,(0,0,255),1)
        j+=10
        continue'''

    cv2.putText(rawImage, "Angle tilted : {} ".format(str(int(angD))), (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255, 0, 0), 2)
    cv2.putText(rawImage, "Distance from mean : {}".format(str(distance)), (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255, 0, 0), 2)



    cv2.circle(rawImage,(int(x1),int(y1)),int(rad),(0,0,255),3)
    print(rad)
    # cv2.drawContours(rawImage, contour_list,  -1, (255,0,0), 2)
    out.write(rawImage)
    cv2.imshow('Objects Detected',rawImage)
    key=cv2.waitKey(100)
    if key==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()