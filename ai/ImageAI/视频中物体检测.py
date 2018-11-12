#-*-coding:utf-8-*- 
__author__ = 'Administrator' 

from imageai.Detection import ObjectDetection
import os
# https://blog.csdn.net/zkt286468541/article/details/81238708


from imageai.Detection import VideoObjectDetection
import os
import time
#计时
start = time.time()

 #当前文件目录
execution_path = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsTinyYOLOv3() #设置需要使用的模型
detector.setModelPath( os.path.join(execution_path, "yolo-tiny.h5")) #加载已经训练好的模型数据
detector.loadModel()

 #设置输入视频地址 输出地址 每秒帧数等
video_path = detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, "traffic.mp4"), output_file_path=os.path.join(execution_path, "traffic_detected"), frames_per_second=20, log_progress=True)
print(video_path)
#结束计时
end = time.time()
print ("\ncost time:",end-start)
