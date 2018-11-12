#-*-coding:utf-8-*-
__author__ = 'Administrator'

from imageai.Detection import ObjectDetection   #导入 ImageAI 目标检测类
import os


# resnet50_coco_best_v2.0.1.h5下载地址
# https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/resnet50_coco_best_v2.0.1.h5，准确度，比其他的都高

execution_path = os.getcwd()
print(execution_path)
print('--------------------000------------------------')
detector = ObjectDetection() #定义目标检测类
detector.setModelTypeAsRetinaNet() #将模型的类型设置为 RetinaNet
#将模型路径设置为 RetinaNet 模型的路径
detector.setModelPath(os.path.join(execution_path , "resnet50_coco_best_v2.0.1.h5"))
detector.loadModel()#将模型加载到的目标检测类

print('--------------------111------------------------')
# 调用目标检测函数，解析输入的和输出的图像路径
detections = detector.detectObjectsFromImage(
    input_image=os.path.join(execution_path , "1.jpg"),
    output_image_path=os.path.join(execution_path , "imagenew.jpg"))

print('--------------------222------------------------')
# 迭代执行 detector.detectObjectsFromImage 函数并返回所有的结果
print(detections)
for eachObject in detections:
    # 打印出所检测到的每个目标的名称及其概率值
    print(eachObject["name"] + ":" +
          str(eachObject["percentage_probability"]) + " " +
          str(eachObject["percentage_probability"]))

print('--------------------over------------------------')
