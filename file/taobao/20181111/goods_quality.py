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

#
# ---------------------遍历sheet1中所有单元格--------------------------------
# row:['商品一级类目', '店铺名称', '平台类型', '商品id', '商品名称', '商品链接', '商品主图', '商品价格(单位：元)', '收入比率(%)', '开推时间', '优惠券面额', '券后价', '优惠券总量', '优惠券剩余量', '优惠券开始时间', '优惠券结束时间', '推广链接', '备注']
# dd rown: 1721     0:商品一级类目    :美容护肤/美体/精油
# dd rown: 1721     1:店铺名称      :森田药妆官方旗舰店
# dd rown: 1721     2:平台类型      :天猫
# dd rown: 1721     3:商品id      :557662696505
# dd rown: 1721     4:商品名称      :【预售】35片森田药妆玻尿酸补水保湿亮肤修护精华匀亮面膜套装
# dd rown: 1721     5:商品链接      :http://item.taobao.com/item.htm?id=557662696505
# dd rown: 1721     6:商品主图      :http://img.alicdn.com/bao/uploaded/i2/641875610/TB1dNzLbBDH8KJjSszcXXbDTFXa_!!0-item_pic.jpg
# dd rown: 1721     7:商品价格(单位：元):149.00
# dd rown: 1721     8:收入比率(%)   :4.00
# dd rown: 1721     9:开推时间      :2017-11-03
# dd rown: 1721    10:优惠券面额     :无
# dd rown: 1721    11:券后价       :
# dd rown: 1721    12:优惠券总量     :0
# dd rown: 1721    13:优惠券剩余量    :0
# dd rown: 1721    14:优惠券开始时间   :
# dd rown: 1721    15:优惠券结束时间   :
# dd rown: 1721    16:推广链接      :https://s.click.taobao.com/t?e=m%3D2%26s%3DwjLyIMUsYHccQipKwQzePOeEDrYVVa64K7Vc7tFgwiFRAdhuF14FMYLrermjXBh75x%2BIUlGKNpU8zPJvLRDF39ynaO8inv88V%2B4ure15Jrvsae04h05DSylfS%2F6S3PYWnn80kOvQNpQk7%2B9mrZpO5tFVTgmw2g34omfkDJRs%2BhU%3D
# dd rown: 1721    17:备注        :官方推荐

# '商品id',
# '商品名称',
# '商品主图',
# '商品详情页链接地址',
# '商品一级类目',
# '淘宝客链接',
# '商品价格(单位：元)',
# '商品月销量',
# '收入比率(%)',
# '佣金',
# '卖家旺旺',
# '卖家id',
# '店铺名称',
# '平台类型',
# '优惠券id',
# '优惠券总量',
# '优惠券剩余量',
# '优惠券面额',
# '优惠券开始时间',
# '优惠券结束时间',
# '优惠券链接',
# '商品优惠券推广链接'


# DROP TABLE IF EXISTS `choiceness_goods_list`;
# CREATE TABLE `choiceness_goods_list` (
#                `id` int(11) NOT NULL AUTO_INCREMENT,
#                `goods_id`    varchar(16) NOT  NULL,
#                `goods_name`  varchar(64) DEFAULT NULL,
#                `goods_url`    varchar(1024) DEFAULT NULL,
#                `goods_detail_url`    varchar(1024) DEFAULT NULL,
#                `goods_1_category` varchar(32)  DEFAULT  NULL,
#                `tao_bao_ke_url`    varchar(1024) DEFAULT NULL,
#                `goods_price`    varchar(8) DEFAULT NULL,
#                `monthl_sales_volume`  varchar(32)  DEFAULT  NULL,
#                `income_rate`     varchar(8) DEFAULT NULL,
#                `commission`    varchar(8) DEFAULT NULL,
#               `seller_wang_wang`  varchar(64) DEFAULT NULL,
#               `seller_id`  varchar(16) DEFAULT NULL,
#               `shop_name`        varchar(32)  DEFAULT  NULL,
#               `platform_type`    varchar(8) DEFAULT NULL,
#               `discount_coupon_id`    varchar(64) DEFAULT NULL,
#               `discount_coupon_sum`   varchar(8) DEFAULT NULL,
#               `discount_coupon_residue`  varchar(8) DEFAULT NULL,
#                `denomination`    varchar(128) DEFAULT NULL,
#               `discount_coupon_begin_date`  varchar(64) DEFAULT NULL,
#               `discount_coupon_end_date`  varchar(64) DEFAULT NULL,
#               `generalize_url`  varchar(1024) DEFAULT NULL,
#               `discount_coupon_generalize_url`  varchar(1024) DEFAULT NULL,
#               PRIMARY KEY (`id`)
# )ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

#创建表
def create_table():
    global conn
    global cursor
    # sql = """ CREATE TABLE IF NOT EXISTS tian_mao_11(id int PRIMARY KEY AUTO_INCREMENT,
    #           `id` int(11) NOT NULL AUTO_INCREMENT,
    #            `goods_id`    varchar(16) NOT  NULL,
    #            `goods_name`  varchar(64) DEFAULT NULL,
    #            `goods_url`    varchar(1024) DEFAULT NULL,
    #            `goods_detail_url`    varchar(1024) DEFAULT NULL,
    #            `goods_1_category` varchar(32)  DEFAULT  NULL,
    #            `tao_bao_ke_url`    varchar(1024) DEFAULT NULL,
    #            `goods_price`    varchar(8) DEFAULT NULL,
    #            `monthl_sales_volume`  varchar(32)  DEFAULT  NULL,
    #            `income_rate`     varchar(8) DEFAULT NULL,
    #            `commission`    varchar(8) DEFAULT NULL,
    #           `seller_wang_wang`  varchar(64) DEFAULT NULL,
    #           `seller_id`  varchar(16) DEFAULT NULL,
    #           `shop_name`        varchar(32)  DEFAULT  NULL,
    #           `platform_type`    varchar(8) DEFAULT NULL,
    #           `discount_coupon_id`    varchar(64) DEFAULT NULL,
    #           `discount_coupon_sum`   varchar(8) DEFAULT NULL,
    #           `discount_coupon_residue`  varchar(8) DEFAULT NULL,
    #            `denomination`    varchar(128) DEFAULT NULL,
    #           `discount_coupon_begin_date`  varchar(64) DEFAULT NULL,
    #           `discount_coupon_end_date`  varchar(64) DEFAULT NULL,
    #           `generalize_url`  varchar(1024) DEFAULT NULL,
    #           `discount_coupon_generalize_url`  varchar(1024) DEFAULT NULL'''
    # cursor.execute(sql);


# 判断数据是否存在
def fetchallData(sql,data):
    try:
       cursor.execute(sql % data)
       # results = cursor.fetchall()
       return cursor.rowcount
    except:
       print ("Error: unable to fetch data")
       return 0

if __name__ == "__main__":
    #连接数据库
    connnect_db()
    #创建表
    #create_table()

    had_insert_count = 0
    insert_count = 0
    #插入数据库
    # 打开一个workbook
    xls_file = [# r'超级好货大额券榜2018-10-24.xls', #5327
                # r'双11品牌尖货榜2018-10-24.xls',#200
                # r'双11好货高佣榜2018-10-24.xls', #4836
                r'双11预售实时热销榜2018-10-24.xls'] #3532      13895
    for xlsfile in xls_file:
        # print(xlsfile)
        workbook = xlrd.open_workbook(xlsfile)
        # 抓取所有sheet页的名称
        worksheets = workbook.sheet_names()
        # print('工作页名字:%s' % worksheets)
             #定位到sheet1
        for sheetname in worksheets:
                print('工作页名字:%s' % sheetname)
                worksheet1 = workbook.sheet_by_name(sheetname)
                #遍历sheet1中所有行row
                rows_num = worksheet1.nrows
                column_num = worksheet1.row_values(0)
                print('    行数:' + str(rows_num))
                print('字段个数:' + str(len(column_num)))
                print('字段名字:%s' % (column_num))

                for curr_row in range(rows_num):
                    row = worksheet1.row_values(curr_row)
                    if curr_row != 0:
                        print('------------------------------------------------------' + xlsfile +'----------------------------------------------------')
                        for y in range(len(row)):
                            print('行%s->%s 列%-2s:%s:%-10s:%s' % ((rows_num-1, curr_row, y+1,len(row[y]),column_num[y], row[y])))
                        for i in range(len(row)):
                            # if  i == 5:  #商品推广链接
                            #     row[i] = get_short_url(row[i])
                            #     time.sleep(1)
                            #     print('行%s->%s 列%-2s:%-10s:%s' % ((rows_num-1, curr_row + 1, i + 1, column_num[i], row[i])))
                            # if i == 15:  # 优惠券推广链接
                            #     row[i] = get_short_url(row[i])
                            #     # time.sleep(1)
                            #     print('行%s->%s 列%-2s:%-10s:%s' % ((rows_num-1, curr_row + 1, i + 1, column_num[i], row[i])))
                            # if i == 13: #优惠券开始时间   :1540310400000
                                # timeArray = time.localtime(long(row[i]))
                                # Localtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(row[i])))
                                # dt = string.digits(row[i])
                                # dt = datetime.datetime.fromtimestamp(long(row[i],))
                                # otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                                # print(dt);
                            if i == 3:  # 商品id
                                # 判断数据是否存在
                                sql = "SELECT * FROM goods_quality WHERE goods_id='%s'"   #商品id
                                data = (row[i])
                                rowcount = fetchallData(sql,data)
                                # print(data)
                                # print(rowcount)
                                if rowcount > 0:
                                    had_insert_count += 1;
                                    print("这条数据存在，返回继续下一条" + str(had_insert_count))
                                    break
                                else:
                                    insert_count += 1;
                                    print("这条数据不存在，插入数据库" + str(insert_count))

                                    sql = "insert into goods_quality(" \
                                          "category_name," \
                                          "seller_nickname," \
                                          "platform_type," \
                                          "goods_id," \
                                          "goods_name," \
                                          "goods_url," \
                                          "goods_pic_url," \
                                          "goods_price," \
                                          "income_rate," \
                                          "discounts_denomination," \
                                          "discounts_sell_price," \
                                          "discounts_number," \
                                          "discounts_remain_number," \
                                          "discounts_begin_date," \
                                          "discounts_end_date," \
                                          "discounts_generalize_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

                                    # print('sql:',sql)
                                    # print('row:', row)

                                    # 插入数据
                                    # cursor.execute(sql, row)
                                    # conn.commit()

                # time.sleep(3)
                #关闭数据库
                cursor.close()
                conn.close()





