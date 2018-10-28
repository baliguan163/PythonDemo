#coding=utf-8
#######################################################
#filename:
#author:
#date:xxxx-xx-xx
#function：读excel文件中的数据
#######################################################
import datetime
import string

import requests
import xlrd
import  pymysql
import  time
import  threading
import  re

#创建锁，用于访问数据库
# lock = threading._allocate_lock()
global conn
global cursor
global count;


def get_short_url(url):
    """
    获取百度短网址
    @param url: {str} 需要转换的网址
    @return: {str} 成功：转换之后的短网址，失败：原网址
    """
    api = "http://dwz.cn/admin/create"
    data = {
        "url": url
    }
    response = requests.post(api, json=data)
    if response.status_code != 200:
        return url
    result = response.json()
    code = result.get("Code")
    if code == 0:
        return result.get("ShortUrl")
    else:
        return url

#连接数据库
def connnect_db():
    global conn
    global cursor
    conn = pymysql.connect(host='localhost',user='root',passwd='123456',db='test',charset='utf8')
    cursor = conn.cursor()
    conn.select_db('test')

def fetDataCount(sql,data):
    try:
       cursor.execute(sql % data)
       # results = cursor.fetchall()
       return cursor.rowcount
    except:
       print ("Error: unable to fetch data")
       return 0


def fetDataSum(sql,data):
    try:
       cursor.execute(sql % data)
       results = cursor.fetchall()
       # print(results)
       for data in results:
           return data[0]
    except:
       print ("Error: unable to fetch data")
       return 0


if __name__ == "__main__":
    connnect_db()

    sql = "SELECT count(*) FROM goods_choiceness"  # 商品id
    data = ()
    # rowcount = fetDataCount(sql, data)
    sum = fetDataSum(sql, data);
    print('sum:' + str(sum))

    for i in range(1,sum+1):
    # for i in range(1, 3):
        # print(i)
        sql = "SELECT * FROM goods_choiceness WHERE id='%s'"  # 商品id
        data = (i)
        cursor.execute(sql % data)
        results = cursor.fetchall()
        # print(results)
        for data in results:
            print('------------------------------------------------------------')
            # print(data)
            # for y in data:
            #     print(y)
            longUrl1 =  data[6]
            # longUrl2 =  data[21]
            longUrl3 = data[22]
            longUrl1Len = len(longUrl1);
            # longUrl2Len = len(longUrl2)
            longUrl3Len = len(longUrl3)
            print('总:',sum,'->',i,' 淘宝客链接:',longUrl1Len,longUrl1)
            # print('总:',sum,'->',i,' 优惠券链接',longUrl2Len,longUrl2)
            print('总:', sum, '->', i, ' 商品优惠券推广链接', longUrl3Len, longUrl3)

            if longUrl1Len > 100:
                shortUrl1 = get_short_url(longUrl1)
                shortUrl1Len = len(shortUrl1);
                # print(shortUrl1Len, shortUrl1)
                # 更新数据库  商品推广链接
                # sql = "UPDATE  goods_quality SET goods_url='%s' WHERE id='%d'"  # 商品id
                sql = "UPDATE goods_choiceness SET tao_bao_ke_url = '%s'  WHERE id = '%s'" % (shortUrl1,i)

                data = (shortUrl1, i)
                cursor.execute(sql)
                conn.commit()
                # results = cursor.fetchall()
                # print(results)
                if cursor.rowcount  == 1:
                    print(str(shortUrl1Len),shortUrl1,'淘宝客链接更新ok')
                else:
                    print(str(shortUrl1Len),shortUrl1,'淘宝客链接更新ng')

            if longUrl3Len > 100:
                shortUrl3 = get_short_url(longUrl3)
                shortUrl3Len = len(shortUrl3);
                # print(shortUrl3Len, shortUrl3)
                # 更新数据库  优惠券推广链接
                sql = "UPDATE goods_choiceness SET discount_coupon_generalize_url='%s' WHERE id='%s'   "  # 商品id
                data = (shortUrl3,i)
                cursor.execute(sql % data)
                conn.commit()
                # results = cursor.fetchall()
                # print(results)
                if cursor.rowcount  == 1:
                    print(str(shortUrl3Len),shortUrl3,'优惠券推广链接更新ok')
                else:
                    print(str(shortUrl3Len),shortUrl3,'优惠券推广链接新ng')

    print('关闭数据库')
    # 关闭数据库
    cursor.close()
    conn.close()



