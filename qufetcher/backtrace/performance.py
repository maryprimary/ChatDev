"""
从数据计算各项数据
"""

from dataclasses import dataclass
import pandas


@dataclass
class PerfSettings():
    cost: float



def put_capital_ret(df:pandas.DataFrame, ps:PerfSettings):
    '''从交易的信息找到收益'''
    #根据交易信号和仓位计算策略的每日收益率
    df.loc[df.index[0], 'capital_ret'] = 0
    #今天开盘新买入的position在今天的涨幅(扣除手续费)
    #今天open的时候买入caption，到close的时候captial升值多少
    df.loc[df['position'] > df['position'].shift(1), 'capital_ret'] = \
                         (df['close'] / df['open']-1) * (1 - ps.cost) 
    #昨天close时有caption，今天open时交易，captial升值多少
    df.loc[df['position'] < df['position'].shift(1), 'capital_ret'] = \
                   (df['open'] / df['close'].shift(1)-1) * (1 - ps.cost) 
    # 当仓位不变时,如果持有当天的capital是当天的change * caption change=昨天的close到今天的close升值多少
    # 如果没有持有那就不变
    df.loc[df['position'] == df['position'].shift(1), 'capital_ret'] = \
                        (df['close']/df['close'].shift()-1) * df['position']
    #计算标的、策略、指数的累计收益率
    df['capital_line']=(df.capital_ret+1.0).cumprod()
    #df['rets_line']=(df.close.pct_change().dropna()+1.0).cumprod()
    return df
