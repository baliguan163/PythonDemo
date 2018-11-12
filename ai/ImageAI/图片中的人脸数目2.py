#-*-coding:utf-8-*- 
__author__ = 'Administrator' 


#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import numpy as np

# https://blog.csdn.net/xiao__run/article/details/76513275

face_cascade=cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")
eye_cascade=cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_eye.xml")
cap=cv2.VideoCapture('test.avi')
while True:
    ret,frame=cap.read()
    i=frame
       # print i.shape
    gray=cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.3,5)
    l=len(faces)
    print l
    for (x,y,w,h) in faces:
    	cv2.rectangle(i,(x,y),(x+w,y+h),(255,0,0),2)
	    cv2.putText(i,'face',(w/2+x,y-h/5),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = i[y:y+h, x:x+w]
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
	        cv2.putText(i,"face count",(20,20),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
	        cv2.putText(i,str(l),(230,20),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
	cv2.imshow("rstp",i)
	if cv2.waitKey(1) & 0xFF == ord('q'):
	    exit(0)
