"""
liuwp的策略
"""

from dataclasses import dataclass
import pandas



def liuwp_put_position(df:pandas.DataFrame):
    '''将liuwp策略的position加入df'''
    lowest = df.close.min()
    df['cls_min'] = df.close / lowest
    #和前期高点的对比
    rolling_max = df.close.cummax()
    df['cls_rolling_max'] = df.close / rolling_max
    #和前期的低点对比
    rolling_min = df.close.cummin()
    df['cls_rolling_min'] = df.close / rolling_min
    #
    return df
