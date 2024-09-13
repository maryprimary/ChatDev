"""
测试K线相关功能
"""

from qufetcher import get_stock_bars
from visualizer.utils import visualize_dataframe, send_msg

def test1():
    ''''''
    df = get_stock_bars('000001.SZ', '20240101', '20240911')
    print(df)
    visualize_dataframe(df, 'close')
    send_msg('qufetcher', '这是数据')

test1()
