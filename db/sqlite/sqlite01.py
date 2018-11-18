#coding=utf-8
import  sqlite3
con=sqlite3.connect('sqlitedemo01')
cur=con.cursor()
#r=cur.execute('create table people(name VARCHAR(30),age INT ,sex CHAR(1))')
#con.commit()
# print r

r=cur.execute('insert into people(name,age,sex) values(\'jee\',21,\'F\')')
con.commit()
#print r

r=cur.execute('select * from people')
print(r)
s=cur.fetchall()
m=len(s)
print(m)


cur.close()
con.close()




