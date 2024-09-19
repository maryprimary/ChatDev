"""
测试atr
"""

from qufetcher.backtrace.atrrsi_strtgy import atrrsi_put_position, AtrRsiSettings
from qufetcher import get_stock_bars



def main():
    '''入口'''
    df = get_stock_bars('000001.SZ', '20240820', '20240911')
    atrrsi_put_position(df, AtrRsiSettings(14, 14, 30))


if __name__ == "__main__":
    main()







