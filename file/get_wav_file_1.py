#coding=utf-8

import sys
import struct
import os
import pyaudio

__author__ = 'bob_hu, hewitt924@gmail.com'
__date__ = 'Dec 19,2011'
__update__ = 'Dec 19,2011'

# python——pcm音频添加头转成Wav格式文件
def geneHeadInfo(sampleRate,bits,sampleNum):
      '''''
      生成头信息，需要采样率，每个采样的位数，和整个wav的采样的字节数
      '''
      rHeadInfo = '\x52\x49\x46\x46'
      fileLength = struct.pack('i',sampleNum + 36)
      rHeadInfo += fileLength
      rHeadInfo += '\x57\x41\x56\x45\x66\x6D\x74\x20\x10\x00\x00\x00\x01\x00\x01\x00'
      rHeadInfo += struct.pack('i',sampleRate)
      rHeadInfo += struct.pack('i',sampleRate * bits / 8)
      rHeadInfo += '\x02\x00'
      rHeadInfo += struct.pack('H',bits)
      rHeadInfo += '\x64\x61\x74\x61'
      rHeadInfo += struct.pack('i',sampleNum)
      return rHeadInfo


if __name__ == '__main__':
      if len(sys.argv) != 5:
        print "usage: python %s inFile sampleRate bits outFile" % sys.argv[0]
        sys.exit(1)

      fout = open(sys.argv[4],'wb') #用二进制的写入模式
      #fout.write(struct.pack('4s','\x66\x6D\x74\x20'))
      #写入一个长度为4的串，这个串的二进制内容为 66 6D 74 20
      #Riff_flag,afd,fad,afdd, = struct.unpack('4c',fin.read(4))
      #读入四个字节，每一个都解析成一个字母
      #open(sys.argv[4],'wb').write(struct.pack('4s','fmt '))
      #将字符串解析成二进制后再写入
      #open(sys.argv[4],'wb').write('\x3C\x9C\x00\x00\x57')
      #直接写入二进制内容：3C 9C 00 00 57
      #fout.write(struct.pack('i',6000)) #写入6000的二进制形式
      #check whether inFile has head-Info
      fin = open(sys.argv[1],'rb')
      Riff_flag, = struct.unpack('4s',fin.read(4))
      if Riff_flag == 'RIFF':
        print "%s 有头信息" % sys.argv[1]
        fin.close()
        sys.exit(0)
      else:
        print "%s 没有头信息" % sys.argv[1]
        fin.close()
        #采样率
        sampleRate = int(sys.argv[2])
        #bit位
        bits = int(sys.argv[3])
        fin = open(sys.argv[1],'rb')
        startPos = fin.tell()
        fin.seek(0,os.SEEK_END)
        endPos = fin.tell()
        sampleNum = (endPos - startPos)
        print sampleNum
        headInfo = geneHeadInfo(sampleRate,bits,sampleNum)
        fout.write(headInfo)
        fin.seek(os.SEEK_SET)
        fout.write(fin.read())
        fin.close()
        fout.close()