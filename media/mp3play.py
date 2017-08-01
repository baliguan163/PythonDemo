#coding=utf-8
import mp3play
import time

filename = "ymyrgsn.mp3"
clip = mp3play.load(filename)
while 1:
  if time.localtime().tm_min % 30 == 0:
    clip.play()
    print "\nStart to play"
    time.sleep(clip.seconds())
    clip.stop()
    print "Stop"
  print '>',
  time.sleep(30) #暂停30秒（不是30分钟）
