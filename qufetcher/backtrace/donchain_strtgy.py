"""
cci的策略
"""

from dataclasses import dataclass
import pandas



@dataclass
class DonchainSettings:
    #14
    don_lookback: int



def donchain_put_position(df: pandas.DataFrame, setting: DonchainSettings):
    '''利用cci进行判断'''
    df['don_up'] = df['high'].rolling(window=setting.don_lookback, min_periods=1).max()
    df['don_dn'] = df['low'].rolling(window=setting.don_lookback, min_periods=1).min()
    print(df)
