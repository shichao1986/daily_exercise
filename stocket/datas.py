# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
import tushare as ts
import datetime
import models

sock_list = []
engine = create_engine('postgresql://sock-user:sock-password@10.6.3.29:15432/sock-db')

db_session = None

def ticks_get_date(sock_list, date=''):
    # import pdb;pdb.set_trace()
    today_data = datetime.datetime.now().date().strftime("%Y-%m-%d")
    if (not date) or (date == today_data):
        target_data = today_data
        func = ts.get_today_ticks
        use_date = False
    else:
        target_data = date
        func = ts.get_tick_data
        use_date = True
    for sock in sock_list:
        print('download {} ...'.format(sock))
        df = func(sock, date=target_data, src='tt') if use_date else func(sock)
        # df = df[df['time'].str.contains('09:30:[0-9]{2}')]
        df['code'] = sock
        df['date'] = target_data
        print('')
        print('download finished! save to db ...')
        table_name = 'ticks_table'
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print('save finished!')

def init_sock_list():

    socklist = db_session.query(models.StockList).all()
    if socklist:
        print('sock list has been inited')
        return

    df = ts.get_today_all()
    table_name = 'stocks_list'
    del df['changepercent']
    del df['trade']
    del df['open']
    del df['high']
    del df['low']
    del df['settlement']
    del df['volume']
    del df['turnoverratio']
    del df['amount']
    del df['per']
    del df['pb']
    del df['mktcap']
    del df['nmc']
    df.to_sql(table_name, engine, if_exists='append', index=False)
    print('save finished!')

def get_all_sock_his_data(start, end, code=''):
    # 除了st的全部股票列表
    if code:
        stocklist = db_session.query(models.StockList).filter(models.StockList.name.notlike('%ST%')).filter(
            models.StockList.code == code).all()
    else:
        stocklist = db_session.query(models.StockList).filter(models.StockList.name.notlike('%ST%')).all()

    i = 1
    table_name = 'stock_his_data'
    # import pdb;pdb.set_trace()
    for stock in stocklist:
        df = ts.get_k_data(stock.code, start=start, end=end)
        df['name'] = stock.name
        #根据日期进行查重操作，对于数据库中已经存在的数据从df中剥离
        idx = 0
        # total_row = df.iloc[:,0].size
        while idx < df.iloc[:,0].size:
            date = df.iloc[idx]['date']
            d = db_session.query(models.StockHisData).filter(models.StockHisData.code == stock.code).filter(
                models.StockHisData.date == date).first()
            if not d:
                idx += 1
            else:
                df.drop(df.index[idx],inplace=True)

        df.to_sql(table_name, engine, if_exists='append', index=False)
        print('seq:{},{}({}) save to db succeed'.format(i, stock.name, stock.code))
        i += 1


    return

def update_percentage(code='',start='', end=''):
    # 除了st的全部股票列表
    if code:
        stocklist = db_session.query(models.StockList).filter(models.StockList.name.notlike('%ST%')).filter(
            models.StockList.code == code).all()
    else:
        stocklist = db_session.query(models.StockList).filter(models.StockList.id > 0).filter(
            models.StockList.name.notlike('%ST%')).all()


    i = 1
    for stock in stocklist:
        print('seq {}:try to update {}({}) percentage...'.format(i, stock.name, stock.code))
        i += 1
        if start and end:
            stock_datas = db_session.query(models.StockHisData).filter(models.StockHisData.code == stock.code).filter(
                models.StockHisData.date >= start).filter(models.StockHisData.date <= end).order_by(
                models.StockHisData.date.asc()).all()
        else:
            stock_datas = db_session.query(models.StockHisData).filter(models.StockHisData.code == stock.code).order_by(
                models.StockHisData.date.asc()).all()
        last_data = None
        for data in stock_datas:
            if not last_data:
                last_data = data
                continue
            else:
                data.percentage = round((data.close / last_data.close - 1) * 100, 2)
            last_data = data
            db_session.merge(data)
            db_session.commit()

    return

def update_ma5(code='',start='', end=''):
    # 除了st的全部股票列表
    if code:
        stocklist = db_session.query(models.StockList).filter(models.StockList.name.notlike('%ST%')).filter(
            models.StockList.code == code).all()
    else:
        stocklist = db_session.query(models.StockList).filter(models.StockList.id > 0).filter(
            models.StockList.name.notlike('%ST%')).all()


    i = 1
    for stock in stocklist:
        print('seq {}:try to update {}({}) ma5...'.format(i, stock.name, stock.code))
        i += 1
        if not start and not end:
            stock_datas = db_session.query(models.StockHisData).filter(models.StockHisData.code == stock.code).filter(
                models.StockHisData.date >= start).filter(models.StockHisData.date <= end).order_by(
                models.StockHisData.date.asc()).all()
        else:
            stock_datas = db_session.query(models.StockHisData).filter(models.StockHisData.code == stock.code).order_by(
                models.StockHisData.date.asc()).all()

        if len(stock_datas) < 5:
            continue

        for idx in range(4, len(stock_datas)):
            total = sum([stock_datas[idx].close, stock_datas[idx-1].close, stock_datas[idx-2].close, stock_datas[idx-3].close, stock_datas[idx-4].close])
            stock_datas[idx].ma5 = round(total/5, 2)
            db_session.merge(stock_datas[idx])
            db_session.commit()

    return


if __name__ == '__main__':

    sock_list = ['000151']

    models.init_db()

    db_session = models.DBSession()

    init_sock_list()

    get_all_sock_his_data('2018-11-12', '2018-11-20')

    update_percentage(start='2018-11-12', end='2018-11-20')

    update_ma5(start='2018-11-06', end='2018-11-20')

    db_session.close()

    #ticks_get_date(sock_list, date='2018-03-05')

    # df = ts.get_today_ticks('300274')
    # # engine = create_engine('postgresql+psycopg2://sock-user:sock-password@10.6.3.29:15432/sock-db')
    #
    # #存入数据库
    # df.to_sql('tick_data',engine, if_exists='append', index_label='id')
    # df.filter()
    # import pdb;pdb.set_trace()

#追加数据到现有表
#df.to_sql('tick_data',engine,if_exists='append')