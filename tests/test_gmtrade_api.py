import os
#from gmtrade.api import set_token, set_endpoint, account, login
from gmtrade.api import *

# token身份认证
set_token(os.environ['GM_USERTOKEN'])

# 示例中为掘金官方仿真服务地址；如API接入掘金终端，则填空字符串
set_endpoint("api.myquant.cn:9000")

# 登录账户，account_id为账户ID，必填；account_alias为账号别名，选填
a1 = account(account_id=os.environ['GM_USERID'], account_alias='ceshi1')
# 可login多个账户，如login(a1, a2, a3)
login(a1)
#
print(get_cash())
print(get_positions())

#o1 = order_volume("SZSE.000001", 100, OrderSide_Buy, OrderType_Limit, PositionEffect_Open, price=9.00)

print(get_orders())

#print(order_cancel_all())

#print(get_orders())
