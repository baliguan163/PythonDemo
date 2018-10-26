#-*-coding:utf-8-*- 
__author__ = 'Administrator'

import xlrd
import  pymysql
import  time
import  threading
import  re



if __name__ == "__main__":
    # 打开一个workbook
    xls_file = [r'精选优质商品清单(内含优惠券)-2018-10-24.xls',
                r'聚划算拼团单品（建议转换淘口令传播）2018-10-24.xls',

                r'超级好货大额券榜2018-10-24.xls',
                r'双11品牌尖货榜2018-10-24.xls',
                r'双11好货高佣榜2018-10-24.xls',
                r'双11预售实时热销榜2018-10-24.xls']
    for xlsfile in xls_file:
        # print(xlsfile)
        workbook = xlrd.open_workbook(xlsfile)
        # 抓取所有sheet页的名称
        worksheets = workbook.sheet_names()
        # print('工作页名字:%s' % worksheets)
             #定位到sheet1
        for sheetname in worksheets:
                # print('工作页名字:%s' % sheetname)
                worksheet1 = workbook.sheet_by_name(sheetname)
                # """
                # #通过索引顺序获取
                # worksheet1 = workbook.sheets()[0]
                # #或
                # worksheet1 = workbook.sheet_by_index(0)
                #
                # #遍历所有sheet对象
                # for worksheet_name in worksheets:
                # worksheet = workbook.sheet_by_name(worksheet_name)
                # 遍历sheet1中所有行row
                num_rows = worksheet1.nrows
                row0 = worksheet1.row_values(0)
                # print('    行数:%s' % (num_rows))
                # print('字段个数:' + str(len(row0) + " 行数:" + num_rows))
                print('字段名字%s:%s' % (len(row0),row0))




