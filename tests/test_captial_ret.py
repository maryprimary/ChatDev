"""
测试ret
"""

import pandas
import numpy
from qufetcher import put_capital_ret, PerfSettings


def test1():
    ''''''
    df = pandas.DataFrame(
        {
            'open':[1, 2, 3, 4, 5, 6, 7, 8],
            'close':[1, 2, 3, 4, 5, 6, 7, 8],
            'position':[0, 0, 0, 0, 1, 1, 1, 1]
        },
        index=pandas.date_range('2024-01-01', '2024-01-08')
    )
    #start=5，end=8，return=8/5
    put_capital_ret(df, PerfSettings(0.0))
    print(df)
    assert numpy.isclose(df.at[df.index[-1], 'capital_line'], 8/5, rtol=1e-8)


def test2():
    df = pandas.DataFrame(
        {
            'open': numpy.random.random(10),
            'close': numpy.random.random(10),
            'position': [0] + list(numpy.random.randint(0, 2, size=9))
        },
        index=pandas.date_range('2024-01-01', '2024-01-10')
    )
    print(df)
    capt = 1.0
    stok = 0.0
    for idx, val in df.iterrows():
        if val['position'] == 1:
            stok += capt / val['open']
            capt = 0
        if val['position'] == 0:
            capt += stok * val['open']
            stok = 0
    #print(df)
    capt = stok * df.iat[-1, df.columns.get_loc('close')] if capt == 0 else capt
    print(capt)
    put_capital_ret(df, PerfSettings(0.0))
    print(df)
    assert numpy.isclose(df.at[df.index[-1], 'capital_line'], capt, rtol=1e-8)
    #if numpy.isclose(df.at[df.index[-1], 'capital_line'], capt, rtol=1e-8):
    #    print('passed')
    #else:
    #    print(df.at[df.index[-1], 'capital_line'], capt)
    #    print('failed')


#test1()
#test2()


