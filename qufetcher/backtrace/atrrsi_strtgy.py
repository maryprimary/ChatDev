"""
atr的策略
"""

from dataclasses import dataclass
import pandas


@dataclass
class AtrRsiSettings:
    #14
    atr_lookback: int
    #9或者14
    rsi_lookback: int
    #
    rsi_buy: float



def atrrsi_put_position(df:pandas.DataFrame, setting:AtrRsiSettings):
    '''利用atr寻找位置'''
    df['high_low'] = df['high'] - df['low']
    df['scls_high'] = (df.shift()['close'] - df['high']).abs()
    df['scls_low'] = (df.shift()['close'] - df['low']).abs()
    #
    mask1 = df['high_low'] > df['scls_high']
    df.loc[mask1, 'tr'] = df['high_low']
    df.loc[~mask1, 'tr'] = df['scls_high']
    #
    mask2 = df['tr'] > df['scls_low']
    df.loc[~mask2, 'tr'] = df['scls_low']
    #后面的补充前面的
    df.bfill(inplace=True)
    #
    df['atr'] = df['tr'].rolling(window=setting.atr_lookback, min_periods=1).mean()
    #
    def _rs_value(rll):
        '''计算rs值'''
        mask1 = rll > 0.0
        return -rll[mask1].sum() / rll[~mask1].sum()
    df['rs'] = df['change'].rolling(window=setting.rsi_lookback).apply(_rs_value)
    df['rsi'] = 100.0 - 100.0/(1 + df['rs'])
    df.drop(['high_low', 'scls_high', 'scls_low'], axis=1, inplace=True)
    #
    df.loc[df['rsi'] < setting.rsi_buy, 'signal'] = 1
    df['position'] = df['signal'].shift(1)
    #前面的补充后面的
    df['position'].ffill(inplace=True)
    #把最开始的部分设置成0
    df['position'].fillna(0, inplace=True)
    print(df)