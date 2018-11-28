#!/usr/local/bin/python
# -*- coding: utf8 -*-

'''
Created on 2016年9月21日

@author: PaoloLiu
'''

import pymysql
import logging
import time


class mysqlpool(object):
    '''
    classdocs
    '''

    def __init__(self, user, password, host, port, database, poolsize):
        '''
        Constructor
        '''

        dbconfig = {
            "user": user,
            "password": password,
            "host": host,
            "port": port,
            "database": database,
            "charset": "utf8"
        }
        try:
            self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_size=poolsize, pool_reset_session=True,
                                                                       **dbconfig)
        except Exception as e:
            logging.warning(e)

    def execute_single_dml(self, strsql):
        try:
            cnx = self.cnxpool.get_connection()
            cursor = cnx.cursor()
            cursor.execute(strsql)
            cursor.close()
            cnx.commit()
        except Exception as e:
            logging.warning(e)
        finally:
            if cnx:
                cnx.close()

    def execute_single_query(self, strsql):

        results = None

        try:
            cnx = self.cnxpool.get_connection()
            cursor = cnx.cursor()
            cursor.execute(strsql)
            results = cursor.fetchall()
            cursor.close()
        except Exception as e:
            logging.warning(e)
        finally:
            if cnx:
                cnx.close()

        return results

    def start_transaction(self):
        try:
            self.cnx = self.cnxpool.get_connection()
        except Exception as e:
            logging.warning(e)

    def end_transaction(self):
        if self.cnx:
            self.cnx.close()

    def commit_transaction(self):
        try:
            self.cnx.commit()
        except Exception as e:
            logging.warning(e)

    def rollback_transaction(self):
        try:
            self.cnx.rollback()
        except Exception as e:
            logging.warning(e)

    def execute_transaction_query(self, strsql):

        results = None

        try:
            cursor = self.cnx.cursor()
            cursor.execute(strsql)
            results = cursor.fetchall()
            cursor.close()
        except Exception as e:
            logging.warning(e)

        return results

    def execute_transaction_dml(self, strsql):

        try:
            cursor = self.cnx.cursor()
            cursor.execute(strsql)
            cursor.close()
        except Exception as e:
            logging.warning(e)


def logger():
    '''
    configure logging
    '''
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s [%(levelname)s] [%(filename)s] [%(threadName)s] [line:%(lineno)d] [%(funcName)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


def test1():
    '''
    事务使用样例
    '''

    cnxpool = mysqlpool("root", "123456", "127.0.0.1", "3306", "test", 3)
    logging.info("begin")
    cnxpool.start_transaction()
    results = cnxpool.execute_transaction_query("select id,name from t1 where id=7 for update")
    cnxpool.commit_transaction()
    for row in results:
        logging.info("id:%d,name:%d" % (row[0], row[1]))
    cnxpool.end_transaction()
    logging.info("end")

if __name__ == '__main__':
    pass
    logger()

    test1()
