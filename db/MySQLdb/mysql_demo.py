#coding=utf-8
import MySQLdb

try:
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='tools',charset='utf8')
    cur=conn.cursor()
    count = cur.execute('select * from user')
    row = cur.fetchall()
    print('there has %s rows record' % count)
    for result in row:
        #print result
        print('ID: %s info %s' % result)
        #print result[1]a

    cur.execute('update user set age=55 where age=20')
    conn.commit()
    
    cur.close()
    conn.close()
except MySQLdb.Error as e:
     print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

