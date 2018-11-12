#-*-coding:utf-8-*-
from imp import reload

__author__ = 'Administrator'

import sys
reload(sys)
# sys.setdefaultencoding('utf-8')

import time
time1 = time.time()
from PIL import Image
import pytesseract


image = Image.open(r'yw.jpg')
code = pytesseract.image_to_string(image)
print(code)
