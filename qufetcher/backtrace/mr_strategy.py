"""
最简单的策略
"""

from dataclasses import dataclass
import pandas

@dataclass
class MRSttgSettings:
    base: str
    lookback: int
    buy_thres: float
    sell_thres: float
    cost: float


def mr_put_posi(df:pandas.DataFrame, mss:MRSttgSettings):
    '''将mr策略的额position和收益放进去'''
    ret_lb = df[mss.base].rolling(mss.lookback, min_periods=1).mean()
    std_lb = df[mss.base].rolling(mss.lookback, min_periods=1).std()
    df['score'] = (df[mss.base] - ret_lb) / std_lb
    df.dropna(inplace=True)
    #
    #当Zscore值小于-1.5且第二天开盘没有涨停发出买入信号设置为1
    df.loc[(df.score < mss.buy_thres) & (df['open'] < df['close'].shift(1) * 1.097), 'signal'] = 1
    #当Zscore值大于1.5且第二天开盘没有跌停发出卖入信号设置为0
    df.loc[(df.score > mss.sell_thres) & (df['open'] > df['close'].shift(1) * 0.903), 'signal'] = 0
    #出现signal的第二天就进行交易
    df['position']=df['signal'].shift(1)
    #position代表是否持有
    #将后续的nan补成之前signal的状态，可能会出现连续相同的signal
    df['position'] = df['position'].ffill()
    #把最开始的部分设置成0
    df['position'] = df['position'].fillna(0)
    return df
