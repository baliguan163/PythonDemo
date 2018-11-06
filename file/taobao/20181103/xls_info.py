#-*-coding:utf-8-*-
import os

__author__ = 'Administrator'

import xlrd
import  pymysql
import  time
import  threading
import  re



if __name__ == "__main__":
    # 打开一个workbook
    # xls_file = [r'精选优质商品清单(内含优惠券)-2018-11-03.xls',
    #             r'聚划算拼团单品（建议转换淘口令传播）2018-11-03.xls',
    #             r'超级好货大额券榜2018-11-03.xls',
    #             r'双11品牌尖货榜2018-11-03.xls',
    #             r'双11好货高佣榜2018-11-03.xls',
    #             r'双11预售实时热销榜2018-11-03.xls']
    info='./file'
    xls_file=os.listdir(info)
    for i in range(0,len(xls_file)):
        print(str(i+1)+ " " + xls_file[i])


    for file in xls_file:
        print('---------------------------------------------')
        filepath = info + '//' + file
        print(filepath)
        workbook = xlrd.open_workbook(filepath)
        worksheets = workbook.sheet_names() # 抓取所有sheet页的名称
        for sheetname in worksheets:
            print(sheetname)
            print('           ---------------------------------------------')
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
            sheetrows = worksheet1.nrows
            sheetrow0 = worksheet1.row_values(0)
            print('           数据行数:' + str(sheetrows) )
            print('           字段列数:' + str(len(sheetrow0)) )





