import pandas as pd
import matplotlib.pyplot as plt
import pybitflyer
import apiInfo
import time
import dataGetter as dG
from datetime import datetime
import sys


class Order:

    def buy_sell(self, ordertype, ordersize, orderprice):
        api = pybitflyer.API(api_key="WR95knYrj36CabGWHK1gdV", api_secret="2Gv0skryfEFZTBnJ3/WocvSrRVeIbi1vzsZ9sAurqaU=")
        ticker = api.ticker(product_code="FX_BTC_JPY")
        board = api.board(product_code="FX_BTC_JPY")

        if ordertype == "BUY":
            contrary = "SELL"
            profit = int(orderprice * 1.0004) # 買いポジのときの利確
            loss = int(orderprice * 0.99) # 同上、損切ライン
        elif ordertype == "SELL":
            contrary = "BUY"
            profit = int(orderprice * 0.9996)
            loss = int(orderprice * 1.01)


        buy_btc = api.sendparentorder(
                                     order_method="IFDOCO",
                                     parameters=[{
                                         "product_code": "FX_BTC_JPY",
                                         "condition_type": "MARKET",
                                         "side": ordertype, # 買いか？
                                        # "price": orderprice,
                                         "size": ordersize
                                     },
                                         {
                                             "product_code": "FX_BTC_JPY",
                                             "condition_type": "LIMIT",
                                             "side": contrary,
                                             "price": profit, ### えっと？？？
                                             "size": ordersize ### 所持しているビットコインの数量を入れる
                                         },
                                         {
                                             "product_code": "FX_BTC_JPY",
                                             "condition_type": "STOP", # 逆指値注文
                                             "side": contrary,
                                             "price": 0, # ここらへん再考
                                             "trigger_price": loss,
                                             "size": ordersize
                                         }],
                                     #minute_to_expire=10000,
                                     #time_in_force="GTC"
                                     )

        print("ordered: " + str(ordersize) + "BTC at the price of " + str(orderprice))

        print(buy_btc)

        return buy_btc