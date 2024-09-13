"""
获取数据
"""

import tushare
import pandas


def get_stock_codes():
    '''获取所有的codes'''


def get_stock_bars(code, start, end):
    '''获取k线'''
    #pro = tushare.pro_api()
    df = tushare.pro_bar(ts_code=code, adj='qfq', start_date=start, end_date=end)
    #将交易日期设置为索引值
    df.index = pandas.to_datetime(df.trade_date)
    df=df.sort_index()
    return df

