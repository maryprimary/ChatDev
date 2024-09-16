
from .backtrace.performance import PerfSettings, put_capital_ret
from .dataapi.reqdata import get_stock_bars, get_company_info, get_stock_codes


import os
import tushare
tushare.set_token(os.environ['TUSHARE_API_KEY'])
