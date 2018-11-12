##coding=utf-8
import shutil

__author__ = 'Administrator'

#根据肤色数量判断
from PIL import Image
import os

# 思路：
# 一、打开图片，转换为YCbCr 格式，
# 二、根据 cb 、 cr 值判断当前像素是否为皮肤
# 三、计算图片中皮肤所占的像素数量。如果该数量超过图片总像素的30%，则判断为色情图片

# 结论：
# 1、算法比较简单，容易实现。
# 2、如果是纯色情图片，这个算法识别率较高
# 3、如果穿有一定数量的衣服干扰，或者人物在图片中占比较小，误判率较高
# 4、大头照容易误判
# 5、没有判断图片是否是人还是动物
# 6、图片像素大于10万时速度较慢，最好先缩放一下

def image_porn(filelist):
    pic_porn_is = 0
    pic_porn_no = 0
    for filename in filelist:
        full_filename=os.path.join(basedir,filename)
        img = Image.open(full_filename).convert('YCbCr')
        w, h = img.size
        data = img.getdata()
        cnt = 0

        for i, ycbcr in enumerate(data):
            y, cb, cr = ycbcr
            # print(filename,y,cb,cr)
            if 86 <= cb <= 117 and 140 <= cr <= 168:
                cnt += 1
        pic_cnt = w * h * 0.3
        if cnt > pic_cnt:
            pic_porn_is = pic_porn_is+1
            print('%s[%s>%s]%s->%s %s is a porn image?:%s' % (pic_porn_is,cnt,pic_cnt,w,h,basedir+'\\'+filename,'Yes'))
            # 拷贝
            mycopyfile(basedir +'\\' + filename,dstfile +'/' + filename);
        else:
            # pass
            pic_porn_no = pic_porn_no+1
            # print('        %s[%s>%s]%s->%s %s is a porn image?:%s.' % (pic_porn_no,cnt,pic_cnt,w,h,basedir+'\\' + filename,'No'))

# if 86 <= cb <= 117 and 140 <= cr <= 168:，这一句最为重要，是本文的精髓所在。根据 YCbCr 肤色模型，
# 许多论文推荐用 86 <= cb <= 127，130 <= cr < 168，但经实验，这个数值并不好，
# 所以我把 cb 的上限改为 117，cr 的下限改为 140，过滤掉太白和太黑的部分。



def mymovefile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.move(srcfile,dstfile)          #移动文件
        # print("move %s -> %s"%( srcfile,dstfile))

def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        # print("copy %s -> %s"%( srcfile,dstfile))


basedir=r'C:\chat_temp'

# srcfile='/Users/xxx/git/project1/test.sh'
dstfile=r'C:/chat_temp/porn'

filelist = os.listdir(basedir)
image_porn(filelist)
