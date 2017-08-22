#!/usr/bin/python
# -*- coding: utf-8 -*-

from  urllib import request
import time

url=['']*350
page = 1

def htmlContentMark(conTent):
    conTent = conTent.replace("<!-- 正文结束 -->", "");
    conTent = conTent.replace("&nbsp;", "");
    conTent = conTent.replace("<br />", "");
    conTent = conTent.replace("<wbr>", "");
    conTent = conTent.replace("<wbr />", "");
    conTent = conTent.replace(";", "");
    conTent = conTent.replace("</div>", "");
    conTent = conTent.replace("</DIV>", "");
    conTent = conTent.replace("<div", "");
    conTent = conTent.replace('STYLE="min-height:22px">', "");
    conTent = conTent.replace("<p", "");
    conTent = conTent.replace("</P>", "");
    conTent = conTent.replace('STYLE="TexT-inDenT: 2em"><wbr>', "");
    conTent = conTent.replace('STYLE="TexT-inDenT: 2em">', "");
    conTent = conTent.replace('<span', "");
    conTent = conTent.replace('STYLE="font-weight: bold">', "");
    conTent = conTent.replace('/>', "");
    conTent = conTent.replace('</A>', "");
    conTent = conTent.replace('</SPAN>', "");

    conTent = conTent.replace('STYLE="TexT-ALiGn: justify Line-HeiGHT: 17.25pt MArGin-Top: 0pt MArGin-BoTToM: 0pt"> STYLE="FonT-FAMiLY: Arial FonT-siZe: 10.5pt">', "");
    conTent = conTent.replace('STYLE="FonT-FAMiLY: Arial FonT-siZe: 10.5pt"> STYLE="FonT-FAMiLY: Arial FonT-siZe: 10.5pt">', "");
    conTent = conTent.replace('STYLE="FonT-FAMiLY: Arial FonT-siZe: 10.5pt">', "");
    conTent = conTent.replace('<font FACE="Arial">Z</FONT><font FACE="宋'
                              '体">', "");
    conTent = conTent.replace('STYLE="FonT-FAMiLY: 宋体 FonT-siZe: 10.5pt">， STYLE="FonT-FAMiLY: Arial FonT-siZe: 10.5pt">', "");
    conTent = conTent.replace(' STYLE="FonT-FAMiLY: 宋体 FonT-siZe: 10.5pt">， ', "");
    conTent = conTent.replace(' STYLE="FonT-FAMiLY: 宋体 FonT-siZe: 10.5pt">', "");

    conTent = conTent.replace('STYLE="TexT-ALiGn: justify Line-HeiGHT: 17.25pt MArGin-Top: 0pt MArGin-BoTToM: 0pt">', "");
    conTent = conTent.replace('STYLE="TexT-ALiGn: justify Line-HeiGHT: 17.25pt MArGin-Top: 0pt MArGin-BoTToM: 0pt"> STYLE="FonT-FAMiLY: Arial FonT-siZe: 10.5pt FonT-WeiGHT: bold">', "");
    conTent = conTent.replace(' STYLE="FonT-FAMiLY: 宋体 FonT-siZe: 10.5pt">', "");
    conTent = conTent.replace(' STYLE="FonT-FAMiLY: 宋体 FonT-siZe: 10.5pt">', "");
    conTent = conTent.replace('STYLE="FonT-FAMiLY: Arial FonT-siZe: 10.5pt FonT-WeiGHT: bold">', "");
    conTent = conTent.replace(' STYLE="FonT-FAMiLY: Arial FonT-siZe: 10.5pt FonT-WeiGHT: bold">', "");
    return conTent


#<a title="" target="_blank" href="http://blog.sina.com.cn/s/blog_4701280b0102e63p.html">操，你想怎样——几部电影的影评</a>'
link = 1
while page <= 1:
    blogurl='http://blog.sina.com.cn/s/articlelist_1191258123_0_'+ str(page)+'.html'
    req = request.Request(blogurl)
    page = request.urlopen(req).read()
    content = page.decode('utf-8','ignore')

    title= content.find(r'<a title=')
    href= content.find(r'href=',title)
    html= content.find(r'.html',href)
    titleindex= content.find(r'</a>',html)

    i = 0
    while title != -1 and href != -1 and i < 50:
        title= content[html+7: titleindex]
        url[i]= content[href+6:html+5]
        print(link,i,title,url[i])

        req = request.Request(url[i])
        page = request.urlopen(req).read()
        article = page.decode('utf-8','ignore')

        #article =  urllib.urlopen(url[i]).read()
        print('download',i,url[i])
        f =open(r'hanhan_blog/' + url[i][-26:],'w+').write(article)

        #<h2 id="t_4701280b01000d2i" class="titName SG_txta">咨询&nbsp;2</h2>
        titleBegin = article.find(r'titName SG_txta">');
        titleEnd = article.find(r'</h2>');
        artTitle= article[titleBegin+17:titleEnd]
        print('arcTitle:',artTitle)

        #<div id="sina_keyword_ad_area2" class="articalContent   ">
        #<div id="share" class="shareUp">
        conTentBegin = article.find(r'class="articalContent   ">');
        conTentEnd = article.find(r'class="shareUp"',conTentBegin);
        conTent= article[conTentBegin+27:conTentEnd-16]

        conTent =  htmlContentMark(conTent)
        print('arcContent:',conTent)

        title= content.find(r'<a title=',html)
        href= content.find(r'href=',title)
        html= content.find(r'.html',href)
        titleindex= content.find(r'</a>',html)

        i = i + 1
        link = link + 1
    else:
        print(page,"find end!")
    page = page + 1
else:
    print('page find end!')

j = 0
while j < 350:
    #content =  urllib.urlopen(url[j]).read()
    #print 'download',j,url[j]
    #f =open(r'hanhanBlog/' + url[j][-26:],'w+')
    j = j + 1
    time.sleep(1)
else:
    print('download article finished!')



