"""
获取个股的基本信息
"""
import pandas
from datetime import datetime, timedelta
from qufetcher.dataapi.reqdata import get_company_info, get_stock_bars
from qufetcher.dataapi.reqdata import get_stock_pb
from qufetcher.backtrace.mr_strategy import mr_put_posi, MRSttgSettings
from qufetcher.backtrace.liuwp_strtgy import liuwp_put_position


def get_basicinfo(code):
    '''获取基本信息'''
    df = get_company_info(code)
    print(df)
    #return " ".join(df.loc[0, :])
    return df.iat[0, 1]


def get_mr_score(code, dataf:pandas.DataFrame=None):
    '''获取最近20天的Zscore'''
    if dataf is None:
        now = datetime.now()
        d7before = now - timedelta(40)
        print(now.strftime(r"%Y%m%d"), d7before.strftime(r"%Y%m%d"))
        dataf = get_stock_bars(code, d7before.strftime(r"%Y%m%d"), now.strftime(r"%Y%m%d"))
    #print(df)
    mr_put_posi(dataf, MRSttgSettings('pct_chg', 20, -1.5, 1.5, 0.0))
    #print(df)
    return dataf.iloc[-1, dataf.columns.get_loc('score')]


def get_liuwp_score(code, dataf:pandas.DataFrame=None):
    '''获取最近的liuwp score'''
    if dataf is None:
        now = datetime.now()
        d7before = now - timedelta(40)
        print(now.strftime(r"%Y%m%d"), d7before.strftime(r"%Y%m%d"))
        dataf = get_stock_bars(code, d7before.strftime(r"%Y%m%d"), now.strftime(r"%Y%m%d"))
    #
    dataf = liuwp_put_position(dataf)
    #print(dataf)
    return dataf.iloc[-20:, map(dataf.columns.get_loc, ['cls_min', 'cls_rolling_max', 'cls_rolling_min'])]

#def get_lowest_and_pb(code):
#    '''获取最近一年的最低点和当前的市净率'''
#    now = datetime.now()
#    ybefore = now - timedelta(360)
#    df = get_stock_bars(code, ybefore.strftime(r"%Y%m%d"), now.strftime(r"%Y%m%d"))
#    lowest = df.close.min()
#    ndm = df.iat[-1, df.columns.get_loc('close')] / lowest
#    #df = get_stock_pb(code, ybefore.strftime(r"%Y%m%d"), now.strftime(r"%Y%m%d"))
#    #print(df)
#    return ndm#, df.pb.iat[-1]

