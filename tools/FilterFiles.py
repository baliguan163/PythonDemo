
import os

def anyTrue(predicate, sequence):
    return  True in map(predicate, sequence);

def filterFiles(folder, exts):
    for fileName in os.listdir(folder):
        path = folder + '/' + fileName
        fl = unicode(path,'gbk')
        if os.path.isdir(fl):
             filterFiles(path, exts)
        elif anyTrue(fileName.endswith, exts):
            print unicode(fileName,'gbk')

exts = ['.rmvb', '.avi', '.mkv','.mp4']
filterFiles('H:/', exts)
