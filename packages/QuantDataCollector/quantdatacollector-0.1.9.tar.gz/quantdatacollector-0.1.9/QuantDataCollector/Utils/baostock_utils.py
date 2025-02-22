"""
author: tianxu

description:
  和baostock库相关的一些工具方法
  比如判断baostock数据是否更新等
"""
import time
import sys
import os
import baostock as bs

# baostock库每日最新数据更新时间：
# 当前交易日17:30，完成日K线数据入库；
STOCK_KDATA_UPDATE_TIME_DAY = 0
STOCK_KDATA_UPDATE_TIME_HOUR = 17
STOCK_KDATA_UPDATE_TIME_MIN = 30

# 当前交易日20:30，完成分钟K线数据入库；
STOCK_KDATA_MINUTE_UPDATE_TIME_DAY = 0
STOCK_KDATA_MINUTE_UPDATE_TIME_HOUR = 20
STOCK_KDATA_MINUTE_UPDATE_TIME_MIN = 30

# 第二自然日1:30，完成前交易日“其它财务报告数据”入库；
STOCK_OTHER_FINANCE_DATA_UPDATE_TIME_DAY = 1
STOCK_OTHER_FINANCE_DATA_UPDATE_TIME_HOUR = 1
STOCK_OTHER_FINANCE_DATA_UPDATE_TIME_MIN = 30

class BaostockError(Exception):
    pass

def is_trade_day(day):
    sys.stdout = open(os.devnull, 'w') # baostock login会强制打印，这里关闭其打印
    lg = bs.login()
    if lg.error_code != '0':
        #登陆失败
        sys.stdout = sys.__stdout__ # 离开时记得打开打印功能
        raise BaostockError("baostock: login failed!, error code = " + lg.error_code)
    rs = bs.query_trade_dates(start_date=day, end_date=day)

    if rs.error_code != '0':
        bs.logout()
        sys.stdout = sys.__stdout__
        raise BaostockError("baostock: query_trade_dates error:" + rs.error_msg)

    trade_dates = rs.get_row_data()
    try:
        res = bool(int(trade_dates[1]))
    except:
        raise BaostockError("index error")
    finally:
        bs.logout()
        sys.stdout = sys.__stdout__ # 离开时记得打开打印功能
    return res

def is_k_data_updated(day = None):
    """判断baostock库中，某一天的非分钟级k线数据是已经更新

    判断baostock库上day(日期，格式为'2021-3-20')的k线数据是否已经更新

    Args:
      day: 需要判断的日期，格式为'YYYY-MM-DD'，可省略，省略时判断当前日期K线是否已经更新

    Returns:
      bool: 已经更新返回True，否则返回False

    Raises:
      ValueError: 如果输入日期的格式不对，会跑出ValueError
    """
    if(not day):
        day = getDate()

    lt = time.localtime(time.time())
    year,month,day = day.split('-')

    if (lt.tm_year > int(year)):
        return True

    if (lt.tm_year < int(year)):
        return False

    if (lt.tm_mon > int(month)):
        return True

    if (lt.tm_mon < int(month)):
        return False

    if (lt.tm_mday > int(day) + STOCK_KDATA_UPDATE_TIME_DAY):
        return True

    if (lt.tm_mday < int(day) + STOCK_KDATA_UPDATE_TIME_DAY):
        return False

    if (lt.tm_hour > STOCK_KDATA_UPDATE_TIME_HOUR):
        return True

    if (lt.tm_hour < STOCK_KDATA_UPDATE_TIME_HOUR):
        return False

    if (lt.tm_min > STOCK_KDATA_UPDATE_TIME_MIN):
        return True

    return False

def is_fin_data_updated(day = None):
    """判断baostock库中，某一天的财经信息是否已经更新

    判断baostock库上day(日期，格式为"2021-3-20")的财经信息是否已经更新

    Args:
      day: 需要判断的日期，格式为'YYYY-MM-DD'，可省略，省略时判断当前日期的财经信息是否已经更新

    Returns:
      bool: 已经更新返回True，否则返回False

    Raises:
      ValueError: 如果输入日期的格式不对，会跑出ValueError
    """
    if(not day):
        day = getDate()

    lt = time.localtime(time.time())
    year,month,day = day.split('-')

    if (lt.tm_year > int(year)):
        return True

    if (lt.tm_year < int(year)):
        return False

    if (lt.tm_mon > int(month)):
        return True

    if (lt.tm_mon < int(month)):
        return False

    if (lt.tm_mday > int(day) + STOCK_OTHER_FINANCE_DATA_UPDATE_TIME_DAY):
        return True

    if (lt.tm_mday < int(day) + STOCK_OTHER_FINANCE_DATA_UPDATE_TIME_DAY):
        return False

    if (lt.tm_hour > STOCK_OTHER_FINANCE_DATA_UPDATE_TIME_HOUR):
        return True

    if (lt.tm_hour < STOCK_OTHER_FINANCE_DATA_UPDATE_TIME_HOUR):
        return False

    if (lt.tm_min > STOCK_OTHER_FINANCE_DATA_UPDATE_TIME_MIN):
        return True

    return False
