# -*- coding: utf-8 -*-

import models
import copy
import datetime
import tushare as ts

from sqlalchemy.sql import desc, asc
from sqlalchemy import func, or_, not_

db_session = None

def active_deal(code, date, start='', end=''):
    if not start:
        start = '09:30:00'
    if not end:
        end = '15:31:00'

    total_buy_volume_qt = db_session.query(func.sum(models.TicksData.volume).label('volume_total'),
                                           func.sum(models.TicksData.amount).label('amount_total')
                                           ).filter(models.TicksData.type == '买盘').filter(models.TicksData.code == code
                                            ).filter(models.TicksData.date == date).filter(models.TicksData.time >= start
                                            ).filter(models.TicksData.time < end).first()
    total_buy_volume = total_buy_volume_qt.volume_total
    total_buy_amount = total_buy_volume_qt.amount_total
    average_buy_price = round(total_buy_amount / total_buy_volume / 100, 2)
    print('{}在{}日{}-{}之间，主动买入：{}手, 金额:{},买入均价:{}'.format(code,date, start,end,total_buy_volume, total_buy_amount, average_buy_price))

    total_sell_volume_qt = db_session.query(func.sum(models.TicksData.volume).label('volume_total'),
                                            func.sum(models.TicksData.amount).label('amount_total')
                                            ).filter(models.TicksData.type == '卖盘').filter(models.TicksData.code == code
                                            ).filter(models.TicksData.date == date).filter(models.TicksData.time >= start
                                            ).filter(models.TicksData.time < end).first()
    total_sell_volume = total_sell_volume_qt.volume_total
    total_sell_amount = total_sell_volume_qt.amount_total
    average_sell_price = round(total_sell_amount / total_sell_volume / 100, 2)
    print('{}在{}日{}-{}之间，主动卖出：{}手，金额:{}，卖出均价:{}'.format(code, date, start,end,total_sell_volume, total_sell_amount, average_sell_price))

    total_volume_qt = db_session.query(func.sum(models.TicksData.volume).label('volume_total'),
                                           func.sum(models.TicksData.amount).label('amount_total')
                                           ).filter(models.TicksData.code == code
                                            ).filter(models.TicksData.date == date).filter(models.TicksData.time >= start
                                            ).filter(models.TicksData.time < end).first()
    total_volume = total_volume_qt.volume_total
    total_amount = total_volume_qt.amount_total


    avg_price = round((total_amount)/(total_volume) / 100, 2)

    return (date, avg_price, total_amount)

def active_deay_day(code, date, start='', end=''):
    result = []
    r = active_deal(code, date)
    result.append(r)

    return result

def active_deal_one_hour(code, date, start='', end=''):
    result = []
    r = active_deal(code, date, end='10:30:00')
    result.append(r)
    r = active_deal(code, date, start='10:30:00', end='11:30:00')
    result.append(r)
    r = active_deal(code, date, start='13:00:00', end='14:00:00')
    result.append(r)
    r = active_deal(code, date, start='14:00:00')
    result.append(r)

    return result

def active_deal_5_minutes(code, date, start='', end=''):
    active_deal(code, date, end='09:35:00')
    active_deal(code, date, start='09:35:00', end='09:40:00')
    active_deal(code, date, start='09:40:00', end='09:45:00')
    active_deal(code, date, start='09:45:00', end='09:50:00')
    active_deal(code, date, start='09:50:00', end='09:55:00')
    active_deal(code, date, start='09:55:00', end='10:00:00')

    active_deal(code, date, start='10:00:00', end='10:05:00')
    active_deal(code, date, start='10:05:00', end='10:10:00')
    active_deal(code, date, start='10:10:00', end='10:15:00')
    active_deal(code, date, start='10:15:00', end='10:20:00')
    active_deal(code, date, start='10:20:00', end='10:25:00')
    active_deal(code, date, start='10:25:00', end='10:30:00')
    active_deal(code, date, start='10:30:00', end='10:35:00')
    active_deal(code, date, start='10:35:00', end='10:40:00')
    active_deal(code, date, start='10:40:00', end='10:45:00')
    active_deal(code, date, start='10:45:00', end='10:50:00')
    active_deal(code, date, start='10:50:00', end='10:55:00')
    active_deal(code, date, start='10:55:00', end='11:00:00')

    active_deal(code, date, start='11:00:00', end='11:05:00')
    active_deal(code, date, start='11:05:00', end='11:10:00')
    active_deal(code, date, start='11:10:00', end='11:15:00')
    active_deal(code, date, start='11:15:00', end='11:20:00')
    active_deal(code, date, start='11:20:00', end='11:25:00')
    active_deal(code, date, start='11:25:00', end='11:30:00')

    active_deal(code, date, start='13:00:00', end='13:05:00')
    active_deal(code, date, start='13:05:00', end='13:10:00')
    active_deal(code, date, start='13:10:00', end='13:15:00')
    active_deal(code, date, start='13:15:00', end='13:20:00')
    active_deal(code, date, start='13:20:00', end='13:25:00')
    active_deal(code, date, start='13:25:00', end='13:30:00')
    active_deal(code, date, start='13:30:00', end='13:35:00')
    active_deal(code, date, start='13:35:00', end='13:40:00')
    active_deal(code, date, start='13:40:00', end='13:45:00')
    active_deal(code, date, start='13:45:00', end='13:50:00')
    active_deal(code, date, start='13:50:00', end='13:55:00')
    active_deal(code, date, start='13:55:00', end='14:00:00')

    active_deal(code, date, start='14:00:00', end='14:05:00')
    active_deal(code, date, start='14:05:00', end='14:10:00')
    active_deal(code, date, start='14:10:00', end='14:15:00')
    active_deal(code, date, start='14:15:00', end='14:20:00')
    active_deal(code, date, start='14:20:00', end='14:25:00')
    active_deal(code, date, start='14:25:00', end='14:30:00')
    active_deal(code, date, start='14:30:00', end='14:35:00')
    active_deal(code, date, start='14:35:00', end='14:40:00')
    active_deal(code, date, start='14:40:00', end='14:45:00')
    active_deal(code, date, start='14:45:00', end='14:50:00')
    active_deal(code, date, start='14:50:00', end='14:55:00')

    active_deal(code, date, start='14:55:00')

    return

def active_deal_15_minutes(code, date, start='', end=''):
    result = []
    r = active_deal(code, date, end='09:45:00')
    result.append(r)
    r = active_deal(code, date, start='09:45:00', end='10:00:00')
    result.append(r)

    r = active_deal(code, date, start='10:00:00', end='10:15:00')
    result.append(r)
    r = active_deal(code, date, start='10:15:00', end='10:30:00')
    result.append(r)
    r = active_deal(code, date, start='10:30:00', end='10:45:00')
    result.append(r)
    r = active_deal(code, date, start='10:45:00', end='11:00:00')
    result.append(r)

    r = active_deal(code, date, start='11:00:00', end='11:15:00')
    result.append(r)
    r = active_deal(code, date, start='11:15:00', end='11:30:00')
    result.append(r)

    r = active_deal(code, date, start='13:00:00', end='13:15:00')
    result.append(r)
    r = active_deal(code, date, start='13:15:00', end='13:30:00')
    result.append(r)
    r = active_deal(code, date, start='13:30:00', end='13:45:00')
    result.append(r)
    r = active_deal(code, date, start='13:45:00', end='14:00:00')
    result.append(r)

    r = active_deal(code, date, start='14:00:00', end='14:15:00')
    result.append(r)
    r = active_deal(code, date, start='14:15:00', end='14:30:00')
    result.append(r)
    r = active_deal(code, date, start='14:30:00', end='14:45:00')
    result.append(r)
    r = active_deal(code, date, start='14:45:00')
    result.append(r)

    return result

def analyse_ticks(code, date=''):
    result = []
    if not date:
        date = datetime.datetime.now().date().strftime("%Y-%m-%d")

    ticks = db_session.query(models.TicksData).filter(models.TicksData.code == code).\
        filter(models.TicksData.date == date).all()
    if ticks:
        # result = active_deal_one_hour(code, date)
        result = active_deay_day(code, date)
    else:
        print('{}在{}日没数据，请先下载数据'.format(code, date))

    return result

def example_ticks_analyse():
    result = []

    day_result = analyse_ticks('000151', '2018-02-22')
    if not day_result:
        print('数据不完整，请使用完整数据进行模型分析')
        exit(1)
    result.append(day_result)

    day_result = analyse_ticks('000151', '2018-02-26')
    if not day_result:
        print('数据不完整，请使用完整数据进行模型分析')
        exit(1)
    result.append(day_result)

    day_result = analyse_ticks('000151', '2018-02-27')
    if not day_result:
        print('数据不完整，请使用完整数据进行模型分析')
        exit(1)
    result.append(day_result)

    day_result = analyse_ticks('000151', '2018-02-28')
    if not day_result:
        print('数据不完整，请使用完整数据进行模型分析')
        exit(1)
    result.append(day_result)

    day_result = analyse_ticks('000151', '2018-03-01')
    if not day_result:
        print('数据不完整，请使用完整数据进行模型分析')
        exit(1)
    result.append(day_result)

    day_result = analyse_ticks('000151', '2018-03-02')
    if not day_result:
        print('数据不完整，请使用完整数据进行模型分析')
        exit(1)
    result.append(day_result)

    day_result = analyse_ticks('000151', '2018-03-06')
    if not day_result:
        print('数据不完整，请使用完整数据进行模型分析')
        exit(1)
    result.append(day_result)

    day_result = analyse_ticks('000151', '2018-03-07')
    if not day_result:
        print('数据不完整，请使用完整数据进行模型分析')
        exit(1)
    result.append(day_result)

    day_result = analyse_ticks('000151', '2018-03-08')
    if not day_result:
        print('数据不完整，请使用完整数据进行模型分析')
        exit(1)
    result.append(day_result)

    day_result = analyse_ticks('000151', '2018-03-09')
    if not day_result:
        print('数据不完整，请使用完整数据进行模型分析')
        exit(1)
    result.append(day_result)

    print (result)
    return

def analyse_his_data(code, start, end):
    df = ts.get_hist_data(code, start=start, end=end)
    row_number = df.iloc[:,0].size

    price_end = 0
    price_start = 0
    rise_percentage = 0
    down_percentage = 0
    sum_percentage = 0
    # import pdb;pdb.set_trace()
    for idx in df.index:
        if idx == 0:
            price_end = df.loc[idx]['close']
        else:
            price_start = df.loc[idx]['close']

        if df.loc[idx]['p_change'] > 0:
            rise_percentage +=  df.loc[idx]['p_change']
        else:
            down_percentage += df.loc[idx]['p_change']

    if row_number:
        sum_percentage = round((price_end / price_start) - 1, 4) * 100

    return sum_percentage, rise_percentage, down_percentage

def three_reds_shape_match(code, **kwargs):
    his_datas = db_session.query(models.StockHisData).filter(models.StockHisData.code == code).order_by(models.StockHisData.date.desc()).all()
    if len(his_datas) < 3:
        return
    his_datas = his_datas[:3]
    name = his_datas[0].name
    rise_percentages = []
    for idx in range(0, 3):
        data = his_datas[idx]

        # 第一天
        if idx == 2:
            if data.close <= data.open:
                return
            percent_change = round((data.close / data.open - 1) * 100,2)
        else:
            if data.close <= his_datas[idx + 1].close:
                return
            percent_change = round((data.close / his_datas[idx + 1].close - 1) * 100,2)
        if percent_change < 1 or percent_change > 3:
            return
        rise_percentages.append(percent_change)

    print('{}({}) 匹配三连阳。近三日阳线涨幅为:{},{},{}'.format(name, code, rise_percentages[2], rise_percentages[1],
                                                  rise_percentages[0]))

def shape_before_date_20days(code, **kwargs):
    if 'date' not in kwargs:
        return

    date = kwargs['date']

    stock_datas = db_session.query(models.StockHisData).filter(models.StockHisData.code == code).filter(
        models.StockHisData.date < date).order_by(models.StockHisData.date.desc()).all()

    if len(stock_datas) < 20:
        return

    name = stock_datas[0].name

    days_close_set20 = []
    for i in range(0, 20):
        days_close_set20.append(stock_datas[i].close)

    min_value = min(days_close_set20)
    days_close_set20.reverse()
    rate_close_set20 = copy.deepcopy(days_close_set20)

    #用最低价除权表示
    for i in range(0, 20):
        rate_close_set20[i] = round((days_close_set20[i]/min_value - 1) * 100,0)

    print('{}({})在{}日之前20个交易日的股价为:{}'.format(name, code, date, rate_close_set20))

# 返回某只股票在指定日期后的3、5、10日内的相对于指定日期收盘价的最大涨幅
def stock_max_rise_after_data(code, date):
    period_1 = 5
    period_2 = 10
    period_3 = 20
    ret = []
    stock_data = db_session.query(models.StockHisData).filter(models.StockHisData.code == code).filter(
        models.StockHisData.date >= date).order_by(models.StockHisData.date.asc()).all()
    if not stock_data:
        return ret
    length = (period_3 + 1) if len(stock_data) > (period_3 + 1) else (period_2 + 1) if len(stock_data) > (period_2 + 1) else (period_1 + 1) if len(stock_data) > (period_1 + 1) else 0
    if length == 0:
        return ret
    price_list = []
    weight_price = stock_data[0].close
    for idx in range(0,length):
        percentage = round((stock_data[idx].close/weight_price - 1) * 100,2)
        price_list.append(percentage)
        if len(price_list) == (period_1 + 1):
            ret.append(max(price_list[1:(period_1 + 1)]))
        if len(price_list) == (period_2 + 1):
            ret.append(max(price_list[(period_1 + 1):(period_2 + 1)]))
        if len(price_list) == (period_3 + 1):
            ret.append(max(price_list[(period_2 + 1):(period_3 + 1)]))

    return ret

# 从给定sample_list的第一日起判断，符合5日均价向上，则返回最后一日日期
def check_sample_average_up(sample_list):
    sample_price = []
    for item in sample_list:
        sample_price.append(item[2])


    for idx in range(0, len(sample_price) - 1):
        if sample_price[idx] == 0 or sample_price[idx + 1] == 0:
            continue
        if sample_price[idx] > sample_price[idx + 1] or sample_list[idx][1] > 4:
            return []


    return [sample_list[-1][0]]

# 从给定sample_list的第一日起判断，符合5日均价向下，则返回最后一日日期
def check_sample_average_down(sample_list):
    sample_price = []
    for item in sample_list:
        sample_price.append(item[2])

    sample_price.reverse()

    for idx in range(0, len(sample_price) - 1):
        if sample_price[idx] == 0 or sample_price[idx + 1] == 0:
            continue
        if sample_price[idx] > sample_price[idx + 1]:
            return []


    return [sample_list[-1][0]]


# 最低值大阳线,样本区间内，最低值第二天为大阳线，涨停更佳
def check_sample_1(sample_list):
    sample_price = []
    for item in sample_list:
        sample_price.append(item[1])
    min_value = min(sample_price)
    max_value = max(sample_price)
    max_value_index = sample_price.index(max_value)
    sample = copy.deepcopy(sample_list)
    for idx in range(0, len(sample)):
        sample[idx] = (sample[idx][0], round((sample[idx][1]/min_value - 1) * 100,2))
        sample_price[idx] = round((sample_price[idx]/min_value - 1) * 100,2)

    ret = []
    for idx in range(0, len(sample)):
        if sample[idx][1] == 0 and idx > max_value_index and idx > 10 and sample[max_value_index][1] > 16:
            # if idx < len(sample) - 2:
            #     if (sample[idx + 2][1] - sample[idx + 1][1]) > (sample[idx + 1][1] - sample[idx][1]) and sample[idx + 2][1] > 8:
            #         ret.append(sample[idx + 2][0])
            if idx < len(sample) - 5:
                # 最低点次日涨幅大于9.5，且最低点5日之前价格低于次日的大张收盘价
                # 大涨后4日内不跌破大涨当日收盘价的1%
                if sample[idx + 1][1] > 9.5 and sample[idx + 1][1] > max(sample_price[(idx - 4):(idx + 1)]) and \
                    min(sample_price[(idx + 2):(idx + 5)]) > (sample[idx + 1][1] - 1):
                    ret.append(sample[idx + 1][0])

    return ret

def his_k_data_analyse(code, **kwargs):
    if 'start' not in kwargs:
        start = ''
    else:
        start = kwargs['start']

    if 'end' not in kwargs:
        end = ''
    else:
        end = kwargs['end']

    if 'interval' not in kwargs:
        interval = 20
    else:
        interval = kwargs['interval']

    if 'offset' not in kwargs:
        offset = 5
    else:
        offset = kwargs['offset']

    # 获得当前stock全部数据
    if start and end:
        his_datas = db_session.query(models.StockHisData).filter(models.StockHisData.code == code).filter(
            models.StockHisData.date >= start).filter(models.StockHisData.date <= end).order_by(
            models.StockHisData.date.asc()).all()
    else:
        his_datas = db_session.query(models.StockHisData).filter(models.StockHisData.code == code).order_by(
            models.StockHisData.date.asc()).all()

    if not his_datas:
        return

    name = his_datas[0].name

    # 将收盘价存入list
    his_datas_price_list = []
    for item in his_datas:
        his_datas_price_list.append((item.date, item.close, item.ma5))

    # import pdb;pdb.set_trace()
    last_date = ''
    while len(his_datas_price_list) > interval:
        interval_offset = 1
        sample_list = his_datas_price_list[:interval]

        # 样本list 与 特征集合进行比较，如果符合则检验其后N天内的相对最低价的最大涨幅是多少，并输出

        # ret = check_sample_1(sample_list)
        # if ret:
        #     # 日期列表
        #     for date in ret:
        #         if last_date and last_date >= date:
        #             continue
        #         last_date = date
        #         max_percentage_list = stock_max_rise_after_data(code, date)
        #         if max_percentage_list:
        #             interval_offset = len(sample_list)
        #             print('{}({})在日期{}符合check_sample_1，短期内最大涨幅为{}'.format(name,code,date,max_percentage_list))

        ret = check_sample_average_up(sample_list)
        if ret:
            date = ret[0]
            max_percentage_list = stock_max_rise_after_data(code, date)
            if max_percentage_list:
                interval_offset = len(sample_list)
                print('{}({})在日期{}符合check_sample_average_up，短期内最大涨幅为{}'.format(name, code, date, max_percentage_list))

        # 清除样本数据的四分之一，最低5日，当且仅当5不大于interval时
        # max_v = max([interval//4, 5])
        # min_v = min([interval, max_v])
        del his_datas_price_list[:max([interval_offset, offset])]

    return

analyse_func_list = [
    # three_reds_shape_match,
    # shape_before_date_20days,
    his_k_data_analyse
]

def stocks_analises(stocklist, **kwargs):
    if not stocklist:
        return
    for stock in stocklist:
        # print('analyse {}({}) result:'.format(stock.name, stock.code))
        for match_func in analyse_func_list:
            try:
                match_func(stock.code, **kwargs)
            except Exception as e:
                print(e)

    print('analyse stocks finished!')

def get_stock_list_by_day_percentage(date, direction, percentage):
    if direction == 'upper':
        stocklist = db_session.query(models.StockHisData).filter(models.StockHisData.date == date).filter(
            models.StockHisData.percentage >= percentage).all()
    elif direction == 'lower':
        stocklist = db_session.query(models.StockHisData).filter(models.StockHisData.date == date).filter(
            models.StockHisData.percentage <= percentage).all()
    else:
        stocklist = []

    return stocklist

def get_stock_list_by_code_list(code_list, all=False):
    stocklist = []
    if all:
        stocklist = db_session.query(models.StockList).filter(models.StockList.name.notlike('%ST%')).all()
    else:
        for code in code_list:
            stock = db_session.query(models.StockList).filter(models.StockList.code == code).first()
            if stock:
                stocklist.append(stock)

    return stocklist

if __name__ == '__main__':
    models.init_db()

    db_session = models.DBSession()

    # 除了st的全部股票列表
    # stocklist = db_session.query(models.StockList).filter(models.StockList.name.notlike('%ST%')).all()

    # stocklist = get_stock_list_by_day_percentage('2018-11-05', 'upper', 7)

    # import pdb;pdb.set_trace()
    stocklist = get_stock_list_by_code_list(['603997'], all=True)

    stocks_analises(stocklist, date='2018-11-05', up_gt=6, interval=12, offset=2, start='2018-09-31', end='2018-11-12')

    # i = 1
    # for stock in stocklist:
    #     sum_percentage, rise_percentage, down_percentage = analyse_his_data(stock.code, '2018-11-06', '2018-11-05')
    #     print ('seq:{},{}({}):'.format(i,stock.name,stock.code))
    #     i += 1

    #example_ticks_analyse()

