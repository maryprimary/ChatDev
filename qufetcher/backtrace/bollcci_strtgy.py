"""
cci的策略
"""

from dataclasses import dataclass
import pandas



@dataclass
class BollCciSettings:
    #14
    cci_lookback: int
    #9或者14
    boll_lookback: int
    #
    boll_dev: float


def bollcci_put_position(df: pandas.DataFrame, setting: BollCciSettings):
    '''利用cci进行判断'''
    df['typc'] = (df['close'] + df['high'] + df['low']) / 3
    rll = df['typc'].rolling(window=setting.cci_lookback, min_periods=1)
    ma = rll.mean()
    def _rll_md(rll):
        rllma = rll.mean()
        rllmd = (rll - rllma).abs().mean()
        return rllmd
    md = rll.apply(_rll_md)
    df['cci'] = (df['typc'] - ma) / 0.015 / md
    print(df)
    #
    rll = df['close'].rolling(window=setting.boll_lookback, min_periods=1)
    sma = rll.mean()
    std = rll.std()
    df['boll_up'] = sma + setting.boll_dev*std
    df['boll_dn'] = sma - setting.boll_dev*std
    print(df)
