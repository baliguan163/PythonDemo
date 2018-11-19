import MySQLdb


class MysqldbHelper:
    # 获取数据库连接
    def getCon(self):
        try:
            conn = MySQLdb.connect(host='localhost', user='root', passwd='123456', db='tools', port=33086, charset='utf8')
            return conn
        except MySQLdb.Error as e:
            print("Mysqldb Error:%s" % (e))

    # 查询方法，使用con.cursor(MySQLdb.cursors.DictCursor),返回结果为字典
    def select(self, sql):
        try:
            con = self.getCon()
            print(con)
            cur = con.cursor(MySQLdb.cursors.DictCursor)
            count = cur.execute(sql)
            fc = cur.fetchall()
            return fc
        except MySQLdb.Error as e:
            print("Mysqldb Error:%s" % e)
        finally:
            cur.close()
            con.close()

    # 带参数的更新方法,eg:sql='insert into pythontest values(%s,%s,%s,now()',params=(6,'C#','good book')
    def updateByParam(self, sql, params):
        try:
            con = self.getCon()
            cur = con.cursor()
            count = cur.execute(sql, params)
            con.commit()
            return count
        except MySQLdb.Error as e:
            con.rollback()
            print("Mysqldb Error:%s" % e)
        finally:
            cur.close()
            con.close()

    # 不带参数的更新方法
    def update(self, sql):
        try:
            con = self.getCon()
            cur = con.cursor()
            count = cur.execute(sql)
            con.commit()
            return count
        except MySQLdb.Error as e:
            con.rollback()
            print("Mysqldb Error:%s" % e)
        finally:
            cur.close()
            con.close()


if __name__ == "__main__":
    db = MysqldbHelper()

    def get():
        sql = "select * from pythontest"
        fc = db.select(sql)
        for row in fc:
            print(row["ptime"])


    def ins():
        sql = "insert into pythontest values(5,'数据结构','this is a big book',now())"
        count = db.update(sql)
        print
        count


    def insparam():
        sql = "insert into pythontest values(%s,%s,%s,now())"
        params = (6, 'C#', 'good book')
        count = db.updateByParam(sql, params)
        print(count)


    def delop():
        sql = "delete from pythontest where pid=4"
        count = db.update(sql)
        print("the：" + str(count))


    def change():
        sql = "update pythontest set pcontent='c# is a good book' where pid=6"
        count = db.update(sql)
        print(count)

    # get()
    # ins()
    # insparam()
    # delop()
