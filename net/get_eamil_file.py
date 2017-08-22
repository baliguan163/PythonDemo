#coding=utf-8
import sys
import os
import re
import requests
import urllib
import threading


def analysis_file(path):
    print("analysis file: %s." % path)
    fi = open(path, "r")
    try:
        all_text = fi.read()
    finally:
        fi.close()

    #print("content:")
    #print(all_text)
    mails = set()
    re_mail = re.compile(r"([a-zA-Z-]+(?:\.[\w-]+)*@[\w-]+(?:\.[a-zA-Z-]+)+)")
    ms = re_mail.findall(all_text)
    for m in ms:
        #print(m)
        mails.add(m)
    print("results: %d" % len(mails))
    if len(mails) > 0:
        fo = open(path + ".mail.txt", "wt")
        for mail in mails:
            fo.write(mail)
            fo.write(",")
        fo.close()



def analysis_dir(path):
    files = os.listdir(path)
    for file in files:
        if (not os.path.isfile(file)) or file.endswith(".mail.txt"):
            continue
        analysis_file(path + "\\" + file)

def main():
    print("analysis is working... ...")
    print("current direcotry: %s." % os.getcwd())
    url = "http://bbs.tianya.cn/post-16-995691-1.shtml"

    if len(sys.argv) < 2:
        print("set the directory to serach")
        return

    path = sys.argv[1]
    is_file = os.path.isfile(path)

    if is_file:
        print("searching file: %s." % path)
        analysis_file(path)
    else:
        if not os.path.exists(path):
            print("there isn't exist direcoty: %s" % path)
            return
        print("searching alll files in directory: %s." % path)
        analysis_dir(path)

if __name__ == '__main__':
    main()
