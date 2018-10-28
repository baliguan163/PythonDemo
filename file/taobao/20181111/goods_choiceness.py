#coding=utf-8
#######################################################
#filename:
#author:
#date:xxxx-xx-xx
#function：读excel文件中的数据
#######################################################
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
       results = cursor.fetchall()
       return results
    except:
       print ("Error: unable to fetch data")
       return 0


if __name__ == "__main__":
    #连接数据库
    connnect_db()
    #创建表
    # create_table()

    #插入数据库
    # workbook = xlrd.open_workbook(r'聚划算拼团单品（建议转换淘口令传播）2018-10-24.xls')
    # workbook = xlrd.open_workbook(r'超级好货大额券榜2018-10-24.xls')
    # workbook = xlrd.open_workbook(r'双11品牌尖货榜2018-10-24.xls')
    # workbook = xlrd.open_workbook(r'双11好货高佣榜2018-10-24.xls')
    # workbook = xlrd.open_workbook(r'双11预售实时热销榜2018-10-24.xls')
    # workbook = xlrd.open_workbook(r'聚划算拼团单品（建议转换淘口令传播）2018-10-24.xls')
    # 打开一个workbook
    xls_file = ['精选优质商品清单(内含优惠券)-2018-10-24.xls']  # 10000
    for xlsfile in xls_file:
        # print(xlsfile)
        workbook = xlrd.open_workbook(xlsfile)
        # 抓取所有sheet页的名称
        worksheets = workbook.sheet_names()
        # print('工作页名字:%s' % worksheets)
        # 定位到sheet1
        for sheetname in worksheets:
            print('工作页名字:%s' % sheetname)
            worksheet1 = workbook.sheet_by_name(sheetname)

            # 遍历sheet1中所有行row
            """
            #通过索引顺序获取
            worksheet1 = workbook.sheets()[0]
            #或
            worksheet1 = workbook.sheet_by_index(0)
            """

            """
            #遍历所有sheet对象
            for worksheet_name in worksheets:
            worksheet = workbook.sheet_by_name(worksheet_name)
            """
            # 遍历sheet1中所有行row
            rows_num = worksheet1.nrows
            column_num = worksheet1.row_values(0)
            print('    行数:' + str(rows_num))
            print('字段个数:' + str(len(column_num)))
            print('字段名字:%s' % (column_num))

            for curr_row in range(rows_num):
                row = worksheet1.row_values(curr_row)
                if curr_row != 0:
                    print('------------------------------------------------------' + xlsfile + '----------------------------------------------------')
                    for y in range(len(row)):
                        print('行%s->%s 列%-2s:%-10s:%s' % ((rows_num - 1, curr_row, y + 1, column_num[y], row[y])))

                    for i in range(len(row)):
                        if i == 0:  # 商品id
                            # 判断数据是否存在
                            sql = "SELECT goods_id FROM goods_choiceness WHERE goods_id='%s'"  # 商品id
                            data = (row[i])
                            results = fetchallData(sql, data)
                            # print(data)
                            # print(len(results))
                            # print(results)
                            if len(results) > 0:
                                print("这条数据存在，返回继续下一条")
                                continue
                            else:
                                print("这条数据不存在，插入数据库")
                                sql = "insert into goods_choiceness(" \
                                      "goods_id," \
                                      "goods_name," \
                                      "goods_url," \
                                      "goods_detail_url," \
                                      "goods_1_category," \
                                      "tao_bao_ke_url," \
                                      "goods_price," \
                                      "monthl_sales_volume," \
                                      "income_rate," \
                                      "commission," \
                                      "seller_wang_wang," \
                                      "seller_id," \
                                      "shop_name," \
                                      "platform_type," \
                                      "discount_coupon_id," \
                                      "discount_coupon_sum," \
                                      "discount_coupon_residue," \
                                      "denomination," \
                                      "discount_coupon_begin_date," \
                                       "discount_coupon_end_date," \
                                       "generalize_url," \
                                        "discount_coupon_generalize_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                # print('sql:',sql)
                                # 插入数据
                                # cursor.execute(sql, row)
                                # conn.commit()
                #
                # # #遍历sheet1中所有列col
                # num_cols = worksheet1.ncols
                # # for curr_col in range(num_cols):
                # #     col = worksheet1.col_values(curr_col)
                # #     print('---------------------遍历sheet1中所有列--------------------------------')
                # #     print('tt col:%s' %(curr_col))
                # #     print('tt  is:%s' % (col))
                #
                # # 遍历sheet1中所有单元格cell
                # for rown in range(num_rows):
                #     # print('---------------------遍历sheet1中所有单元格--------------------------------')
                #     row = worksheet1.row_values(0)
                #     # print('row:%s' % (row))
                #     for coln in range(num_cols):
                #         cell = worksheet1.cell_value(rown, coln)
                #         # ('dd rown:%5s %5s:%-10s:%s' % (rown, coln, row[coln], cell))
                #
                #

                        # """
                        # #其他写法：
                        # cell = worksheet1.cell(rown,coln).value
                        # print cell
                        # #或
                        # cell = worksheet1.row(rown)[coln].value
                        # print cell
                        # #或
                        # cell = worksheet1.col(coln)[rown].value
                        # print cell
                        # #获取单元格中值的类型，类型 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                        # cell_type = worksheet1.cell_type(rown,coln)
                        # print cell_type

            # time.sleep(3)
            #关闭数据库
            cursor.close()
            conn.close()





