#coding=utf-8


from bs4 import BeautifulSoup
import xlwt

with open('cww.xml', 'r',encoding='utf8') as f:
    xml_doc =f.read()   #读取xml文本内容
    # print('xml_doc:',xml_doc)
    f.close()

soup = BeautifulSoup(xml_doc, 'html.parser')
keyword = ['fpdm','fphm','kprq','gmfnsrsbh','je','se','zfbz','xh']  #关键词list

datatable = xlwt.Workbook(encoding='utf-8', style_compression=0)
newsheet = datatable.add_sheet('mxxx', cell_overwrite_ok=True)  #新建excel文档sheet

num = 0 #列
for i in range(len(keyword)):
    newsheet.write(0, num, keyword[i])  #写入每列keyword
    info_list = []
    for se in soup.find_all(keyword[i]):
         info = se.get_text()
         print('info:',i+1,'',info)
         info_list.append(info) #找出所有对应标签内的text组成list
    # print(info_list)
    for i in range(len(info_list)):
        newsheet.write(i+1, num, info_list[i])  #将该list中数据以列写入excel表

    num += 1    #列数加一，继续遍历关键词写入excel表格

datatable.save('liez.xls')