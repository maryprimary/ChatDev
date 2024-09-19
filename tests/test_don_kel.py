"""
测试atr
"""

from qufetcher.backtrace.keltner_strtgy import KeltnerSettings, keltner_put_position
from qufetcher.backtrace.donchain_strtgy import DonchainSettings, donchain_put_position
from qufetcher import get_stock_bars



def main():
    '''入口'''
    df = get_stock_bars('000001.SZ', '20240820', '20240911')
    keltner_put_position(df, KeltnerSettings(14, 14, 2.0))
    donchain_put_position(df, DonchainSettings(14))



if __name__ == "__main__":
    main()

