# -*- coding: utf-8 -*-
"""
时间: 2019/8/6 16:42

作者: shichao

更改记录:

重要说明:
"""
import sys
import time
import datetime
import threading

## 导入psycopg2包
import psycopg2

msglist = []
msglist_lock = threading.Lock()

TABLE_COUNTS = 1000

## 连接到一个给定的数据库
conn = psycopg2.connect(database="demo-db", user="demo-user",
                        password="password", host="10.6.3.29", port="54321")

## 建立游标，用来执行数据库操作
cursor = conn.cursor()

def create_tables(n):
    for i in range(n):
        cursor.execute("CREATE TABLE table_{}(id int, k1 CHAR(8) , k2 int , k3 TIMESTAMP )".format(i))

    conn.commit()

def insert_one_data(tablename, k1, k2):
    # import pdb;pdb.set_trace()
    sql = "insert into {} (k1, k2, k3) values ('{}', {}, '{}')".format(tablename, k1, k2, datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'))
    cursor.execute(sql)

def savedata():
    global msglist

    while True:
        with msglist_lock:
            msg_count = len(msglist)
            if msg_count < 100000:
                sql_list = ['table_{}'.format(i) for i in range(TABLE_COUNTS)]
                msglist += sql_list
        print('save {} data...'.format(msg_count))
        time.sleep(1)

def close_pg():
    ## 关闭游标
    cursor.close()

    ## 关闭数据库连接
    conn.close()

def insert_table():
    global msglist
    global json_list
    threading.Thread(target=savedata).start()

    while True:
        step = 1000
        with msglist_lock:
            publist = msglist[:step]
            msglist = msglist[step:]

        pub_count = len(publist)
        if pub_count == 0:
            continue

        for tb in publist:
            insert_one_data(tb, 'std1', 200)

        try:
            conn.commit()
        except Exception as e:
            print(e)

def main():
    # create_tables(TABLE_COUNTS)

    insert_table()

    close_pg()

    return 0

if __name__ == '__main__':
    sys.exit(main())