#coding:utf-8
import urllib3
import json

def xiaohuangji(ask):
    ask = ask.encode('UTF-8')
    enask = urllib3.quote(ask)
    baseurl = r'http://www.simsimi.com/func/req?msg='
    url = baseurl+enask+'&lc=ch&ft=0.0'
    resp = urllib3.urlopen(url)
    reson = json.loads(resp.read())
    return resondef

if __name__ == "__main__":
	ret = xiaohuangji('你好')
	print('ret:',ret)
