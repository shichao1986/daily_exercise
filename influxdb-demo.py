# -*- coding: utf-8 -*-
"""
时间: 2019/8/2 12:03

作者: shichao

更改记录:

重要说明:
时序数据库查询返回结果按照时间顺序排列
"""
import random
import time
import datetime
import threading
import copy
from datetime import timedelta

from influxdb import InfluxDBClient

client = InfluxDBClient('10.6.3.29', port=8086, username='root',password='password', timeout=10)  # timeout 超时时间 10秒

dblist = client.get_list_database()

client.switch_database('mydb')

msglist = []
msglist_lock = threading.Lock()

json_item = {
        "measurement": "table_X",
        "tags": {
            "stuid": "stuid1"
        },
        #   "2018-05-16T21:58:00Z"
        "time": '',
        "fields": {
            "value": float(random.randint(0, 1000))
        }
    }


def savedata():
    global msglist
    global json_list

    while True:
        print('start save data...')
        with msglist_lock:
            msg_count = len(msglist)
            if msg_count < 100000:
                json_list = []
                base_time = datetime.datetime.now()

                for i in range(1000):
                    data_time = base_time + timedelta(microseconds=1*i)
                    data_item = copy.deepcopy(json_item)
                    data_item['measurement'] = 'table_{}'.format(i)
                    data_item['time'] = data_time.strftime('%Y-%m-%dT%H:%M:%S.%f')
                    json_list.append(data_item)
                msglist += json_list
        # import pdb; pdb.set_trace()
        time.sleep(1)

threading.Thread(target=savedata).start()

while True:
    step = 1000
    with msglist_lock:
        publist = msglist[:step]
        msglist = msglist[step:]

    pub_count = len(publist)
    if pub_count == 0:
        continue
    ret = client.write_points(publist, batch_size=pub_count)

    print('{},{}'.format(ret, pub_count))


# print('查看数据库所有表\n')
# tables = client.query('show measurements;')
# print(tables)

# print('查询表记录')
# rows = client.query('select value from table1;')
# print(rows)


# import pdb;pdb.set_trace()
