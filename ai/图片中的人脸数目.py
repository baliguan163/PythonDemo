#-*-coding:utf-8-*- 
__author__ = 'Administrator' 

#!/usr/bin/python
# -*- coding: utf-8 -*-
import cv2
import numpy as np

# 小编有个群193369905，里面分享的均是机器视觉的资料。基于图像的人数统计属于模式识别问题，可应用于安防领域。传统的方法包括：1）视频捕获；2）目标提取（背景建模、前景分析）——常见方法有高斯背景建模、帧差法、三帧差法等；3）目标识别（模式识别、特征点分析），如人脸识别，头肩部识别等，OpenCV里可以使用Hear特征、级联分类器来进行特征检测；4）目标跟踪——基本方法有直方图特征匹配和运动目标连续性匹配，opencv里可以使用CamShift算法直接对彩色图像进行分析；5）轨迹分析——根据目标的运动轨迹计算目标目标运动方向和位移，判断目标是进入还是离开指定区域，从而对目标进行数目统计。
# 前段时间我接到一个项目，需要统计公交车的人数，于是我就利用python-opencv对人头统计了一下，然后利用轨迹分析计算目标运动的方向和位移，来判断目标是上公交还是下公交。
# 下面我先贴出如何利用python-opencv来统计一下图片中的人脸数目吧，人脸检测注释请参考我的上一篇博客：

                         ''
face_cascade=cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")
eye_cascade=cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_eye.xml")
i = cv2.imread('1.jpg')
print i.shape
gray=cv2.cvtColor(i,cv2.COLOR_BGR2GRAY)
faces=face_cascade.detectMultiScale(gray,1.3,5)
l=len(faces)
print l
for (x,y,w,h) in faces:
    cv2.rectangle(i,(x,y),(x+w,y+h),(255,0,0),2)
    cv2.putText(i,'face',(w/2+x,y-h/5),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = i[y:y+h, x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
cv2.putText(i,"face count",(20,20),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
cv2.putText(i,str(l),(230,20),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
#cv2.putText(i,"eyes count",(20,60),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
print i.shape	#cv2.putText(i,str(r),(230,60),cv2.FONT_HERSHEY_PLAIN,2.0,(255,255,255),2,1)
cv2.imshow("img",i)
cv2.waitKey(0)
