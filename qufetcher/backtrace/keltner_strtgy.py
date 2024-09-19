"""
atr的策略
"""

from dataclasses import dataclass
import pandas



@dataclass
class KeltnerSettings:
    """
Parameters
----------
atr_lookback : ATR的窗口长度
kel_lookback : SMA的窗口长度
kel_dev: ATR前的系数
    """
    #14
    atr_lookback: int
    #
    kel_lookback: int
    #atr的系数
    kel_dev: float



def keltner_put_position(df:pandas.DataFrame, setting:KeltnerSettings):
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
    df.drop(['high_low', 'scls_high', 'scls_low'], axis=1, inplace=True)
    #
    sma = df['close'].rolling(setting.kel_lookback, min_periods=1).mean()
    df['keltner_up'] = sma + setting.kel_dev*df['atr']
    df['keltner_dn'] = sma - setting.kel_dev*df['atr']
    print(df)
