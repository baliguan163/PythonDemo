from urllib import request
#http://qinghuabeida.cn/
try:
    data=request.urlopen("http://qinghuabeida.cn/admin").read()
    print(data)
    print("页面存在")
except:
    print("页面不存在")