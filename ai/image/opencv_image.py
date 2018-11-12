
#!/usr/bin/env python
#coding=utf-8

from __future__ import print_function
import sys
from PIL import Image

def  getAttr(path):
    for infile in path:
        try:
            with Image.open(infile) as im:
                print(infile, im.format, "%dx%d" % im.size, im.mode)
                img = Image.open(infile)
                #Image._show(img)
                new_img = img.convert('L')
                #Image._show(new_img)
        except IOError:
            print('IOError')
            pass

path=[r'D:\图片\001.jpg']
if __name__ == "__main__":
    getAttr(path)