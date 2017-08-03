#decoding=utf-8
import  urllib
import  hashlib
import  pymysql
import requests

import  time


global cur
global conne
def connnect_db():
    global conne
    global cur
    conne=pymysql.connect(host='localhost',user='root',passwd='123456',db='test',charset='utf8')
    cur=conne.cursor()


def get_md5(src):
    myMd5 = hashlib.md5()
    myMd5.update(src)
    myMd5_Digest = myMd5.hexdigest()
    return myMd5_Digest


#保存link信息
def save_link(title,url):
    link_md5=get_md5(url)
    print(link_md5)
    sql="SELECT * FROM url WHERE title = '"+title+"'"
    print(sql)
    cur.execute(sql)
    result=cur.fetchone()
    print(result)
    '''
    if result == None:
    domain=url.replace('http://','')
    domain=domain.replace('https://','')

    #类似于PHP的trim()
    domain=domain.strip('/');
    domain=domain+'/';
    endpos=domain.find('/')

    #这个字符截取方式看起来也是与众不同，因为都没用到函数
    domain=domain[0:endpos]

    #这里注意一下 对于utf8 截取3个字节是一个汉字，这和编码有关
    title=title.decode('utf8')[0:3*48].encode('utf8')
    '''
    print(title)
    print(url)
    if result == None:
        insert_sql="INSERT INTO `test`.`url` (`title`,`url`) VALUES('"+title+"','"+url+"')"
        cur.execute(insert_sql)
        conne.commit()


def htmlContentMark(conTent):
    conTent = conTent.replace("<p", "");
    conTent = conTent.replace("</p>", "");
    conTent = conTent.replace("<o:p>", "");
    conTent = conTent.replace("</o:p>", "");
    conTent = conTent.replace("</span>", "");
    conTent = conTent.replace("<span ", "");
    conTent = conTent.replace("&nbsp;", "");
    conTent = conTent.replace('style="TEXT-INDENT: 32pt; mso-char-indent-count: 2.0000" class="MsoNormal">', "");
    conTent = conTent.replace('style="FONT-FAMILY: 宋体; FONT-SIZE: 12pt; mso-spacerun: \'yes\'; mso-font-kerning: 1.0000pt">', "");
    conTent = conTent.replace('style="TEXT-INDENT: 24pt; mso-char-indent-count: 1.5000" class="MsoNormal">', "");
    conTent = conTent.replace("&ldquo;", "");
    conTent = conTent.replace("&rdquo;", "");
    conTent = conTent.replace("<", "");
    return conTent

#下载page内容
def  get_page(url):
    page = requests.get(url)
    page = page.content
    page = page.decode('utf-8')
    return page
#http://www.yangxian.gov.cn/news/yxxw/index.html
#http://www.yangxian.gov.cn/news/yxxw/index_2.html
#http://www.yangxian.gov.cn/news/yxxw/index_3.html
#http://www.yangxian.gov.cn/news/yxxw/index_67.html

base_url='http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10802&cur_page='
connnect_db()
page = 1
while page <= 1:
    #yxnewsurl='http://www.yangxian.gov.cn/news/yxxw/index.html'
    if page == 1:
       url = base_url.replace('&cur_page=','')
       #yxnewsurl = 'http://www.yangxian.gov.cn/info/iList.jsp?cat_id=10802'
    else:
       url = base_url + str(page)

    #print '请求地址:',url
    #print('爬取当中,当前第%d页...' % page,url)
    #newstr = urllib.request.urlopen(url).read()
    newstr = get_page(url);

    href= newstr.find(r'class="red">')
    amark= newstr.find(r'goRight',href)
    html= newstr.find(r'htm',amark)
    newdate= newstr.find(r'</li>',html)

    #一页内容循环读取
    i = 1
    while newdate != -1 and href != -1 and i <= 22:
        title = newstr[html+5:newdate-4]
        url = newstr[html-17:html+3]
        date  = newstr[amark+9:amark+19]
        part  = newstr[href+13:amark-21]
        path = 'http://www.yangxian.gov.cn'+url

        print('-----------------爬取页数%d----------' % page,i,'个新闻')
        print('title:',title)
        print('date:',date)
        print('part:',part)
        print('url:',path)
        #save_link(title,path)

        print('获取文章内容')
        #读取标题
        content = get_page(path);

        titleBegin= content.find(r'class="contentLeft">')
        titleEnd= content.find(r'class="infoMark">',titleBegin)
        title= content[titleBegin+85:titleEnd-73]

        #解析内容
        articleBegin= content.find(r'<div class="info">')
        articleEnd= content.find(r'<div class="friend_link">')
        print('title:',title)
        print('文章开始:',articleBegin) 
        print('文章结束:',articleEnd)
        article= content[articleBegin+25:articleEnd-12]
        #print '文章内容:',htmlContentMark(article)


        #下次内容
        href= newstr.find(r'class="red">',newdate)
        amark= newstr.find(r'goRight',href)
        html= newstr.find(r'htm',amark)
        newdate= newstr.find(r'</li>',html)

        #content = urllib.urlopen(ulr).read();
        #print content
        #filename = ulr[-15:]
        #print filename
        #open(filename,'w').write(content)
        i = i + 1

    else:
        print("find end!")
    page = page + 1
else:
    print('page find end!')











