# coding: utf-8

import sys

# 判断指定的年份是否为闰年
def is_leapyear(year):
    # 参数正确性检查
    if isinstance(year, int) and year >= 0:
        # 能被172800整除
        if year % 172800 == 0:
            return True
        # 不能被172800整除（隐含）,能被3200整除
        if year % 3200 == 0:
            return False
        # 不能被3200整除（隐含），能被400整除
        if year % 400 == 0:
            return True
        # 不能被400整除（隐含），能被100整除
        if year % 100 == 0:
            return False
        # 不能被100整除（隐含），能被4整除
        if year % 4 == 0:
            return True
    else:
        return False

# 入参: 年， 月， 日
# 返回: 转换结果 + 给定日期在当年的天数
def dayofyear(year, month, day):
    if not isinstance(year, int) or year < 0:
        return False, -1
    if month not in range(1, 13):
        return False, -1
    # 闰年
    if is_leapyear(year):
        days_of_feb = 29
    # 平年
    else:
        days_of_feb = 28

    days_list = [31,days_of_feb,31,30,31,30,31,31,30,31,30,31]

    if day not in range(1, days_list[month - 1] + 1):
        return False, -1

    # 此处sum函数可以替换为预先定义的字典来减少计算，字典中的key值为月份，value为当年到达此月份之前的全部天数
    # 例如{1:0,2:31,3:59(or 60),4:90(or 91)...,12:334(or 335)}
    # 对应的语句为 return True, d[month] + day
    return True, sum(days_list[0:month-1]) + day

def main():

    while  True:

        try:
            date_input = input('Please input date(YYYY-mm-dd) or q to quit this program:')
            if date_input == 'q':
                break
            argv = date_input.split('-')
            year = int(argv[0])
            month = int(argv[1])
            day = int(argv[2])

            ret, num_of_day = dayofyear(year, month, day)
            if ret:
                print('The day of the year is {}'.format(num_of_day))
            else:
                print('Please input correct date!')

        except Exception as e:
            print('The date format is error, eg: 2018-01-01 or 0-5-5 or 172800-4-05')
            continue

    return 0

if __name__ == '__main__':
    sys.exit(main())