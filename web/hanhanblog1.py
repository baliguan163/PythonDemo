#coding=utf-8
import  urllib

str = '<a title="" target="_blank" href="http://blog.sina.com.cn/s/blog_4701280b0102e63p.html">操，你想怎样——几部电影的影评</a>'
href= str.find(r'href=')
print(href)
html= str.find(r'.html')
print(html)

titleindex= str.find(r'</a>')
print(titleindex)

title= str[html+7:titleindex]
print(title)

ulr= str[href+6:html+5]
print(ulr)

content = urllib.urlopen(ulr).read();
#print content
filename = ulr[-26:]
print(filename)
open(filename,'w').write(content)