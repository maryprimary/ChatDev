"""
测试atr
"""

from qufetcher.backtrace.bollcci_strtgy import bollcci_put_position, BollCciSettings 
from qufetcher import get_stock_bars



def main():
    '''入口'''
    df = get_stock_bars('000001.SZ', '20240820', '20240911')
    bollcci_put_position(df, BollCciSettings(14, 14, 3.4))


if __name__ == "__main__":
    main()

