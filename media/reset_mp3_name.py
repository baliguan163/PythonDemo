#coding=utf-8
import mp3play
import time

#!修改下载的Mp3文件名称为正确的Mp3文件
def ModifyMp3FileInfo(filename):
"tag":{"valuepos":(0,3),"value":""},
         "SongName":{"valuepos":(3,33),"value":""},
         "SongPeople":{"valuepos":(33,63),"value":""},
         "Zj":{"valuepos":(63,93),"value":""},
         "Year":{"valuepos":(93,97),"value":""},
         "Bak":{"valuepos":(97,125),"value":""}
         }
	try:
	f = open(filename,'rb')
         f.seek(-128,2)
         sdata = f.read(3)
         if sdata == 'TAG':
             f.seek(-128,2)
             sdata = f.read(128)
             for tag,subitem in mp3Id3V1.items():
                 subitem["value"] = sdata[subitem["valuepos"][0]:subitem["valuepos"][1]].replace('\00','').strip()
                 print '%s='%tag,'%s'%subitem["value"],'\n'
             f.close()
             import os
             if mp3Id3V1["SongName"]["value"]!='':
                 test = [os.path.dirname(filename),'\\']
                 test.append(mp3Id3V1["SongName"]["value"])
                 test.append('.mp3')
                 newfilename = ''.join(test)
                 print newfilename
                 if os.path.exists(newfilename):
                     test = ['Filename ',newfilename,' Has Existed']
                     print ''.join(test)
                 else:
                     try:
                         os.rename(filename,newfilename)
                     except WindowsError,e:
                         if e.winerror:
                             print 'Modify filename failed ,maybe the file is inuse'
                         else:
                             print 'UnKnown error'
         else:
             print 'Is not a MP3 file'
     except IOError:
         print 'Open file failed'