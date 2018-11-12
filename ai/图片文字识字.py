#-*-coding:utf-8-*- 
from PIL import Image
import pytesseract
# 这里我们需要用到两个库：pytesseract和PIL

# 同时我们还需要安装识别引擎tesseract-ocr
# 图片文字的OCR识别有一款开源原件tesseract-ocr,最初是在linux上，当然现在也有windows版本，现在发展到4.0版本。
# https://github.com/tesseract-ocr/tesseract/wiki/4.0-with-LSTM#400-alpha-for-windows
# https://github.com/UB-Mannheim/tesseract/wiki

# tesseract OCR语言包的下载地址
# https://github.com/tesseract-ocr/tessdata

def image_to_string(path):
    # 上面都是导包，只需要下面这一行就能实现图片文字识别
    text = pytesseract.image_to_string(Image.open(path), lang='chi_sim')
    return text

print(image_to_string('2.jpg'))
