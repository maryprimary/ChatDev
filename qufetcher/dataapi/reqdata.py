"""
获取数据
"""

import tushare
import pandas


def get_company_info(code):
    ''''''
    pro = tushare.pro_api()
    df = pro.stock_company(ts_code=code, fields='main_business, business_scope')
    return df


def get_stock_codes():
    '''获取所有的codes'''
    pro = tushare.pro_api()
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code, name')
    return data


def get_stock_bars(code, start, end) -> pandas.DataFrame:
    '''获取k线'''
    #pro = tushare.pro_api()
    df = tushare.pro_bar(ts_code=code, adj='qfq', start_date=start, end_date=end)
    #将交易日期设置为索引值
    df.index = pandas.to_datetime(df.trade_date)
    df=df.sort_index()
    return df


def get_stock_pb(code, start, end) -> pandas.DataFrame:
    '''获取市净率：总市值/净资产'''
    pro = tushare.pro_api()
    df = pro.bak_basic(trade_date=end, ts_code=code, fields='trade_date,ts_code,name,pb')
    return df
