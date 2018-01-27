import pandas as pd
import matplotlib.pyplot as plt
import pybitflyer
import apiInfo
import time
import dataGetter as dG
from datetime import datetime
import sys


class Order:

    def buy_sell(self, ordertype, ordersize, orderprice,product,apiKey,apiSecret):
        api = pybitflyer.API(api_key=apiKey, api_secret=apiSecret)
        ticker = api.ticker(product_code=product)
        board = api.board(product_code=product)

        if ordertype == "BUY":
            contrary = "SELL"
            profit = int(orderprice * 1.002) # 買いポジのときの利確
            loss = int(orderprice * 0.99) # 同上、損切ライン
        elif ordertype == "SELL":
            contrary = "BUY"
            profit = int(orderprice * 0.998)
            loss = int(orderprice * 1.01)


        buy_btc = api.sendparentorder(
                                     order_method="IFDOCO",
                                     parameters=[{
                                         "product_code": product,
                                         "condition_type": "LIMIT",
                                         "side": ordertype, # 買いか？
                                         "price": orderprice,
                                         "size": ordersize
                                     },
                                         {
                                             "product_code": product,
                                             "condition_type": "LIMIT",
                                             "side": contrary,
                                             "price": profit, ###
                                             "size": ordersize ### 所持しているビットコインの数量を入れる
                                         },
                                         {
                                             "product_code": product,
                                             "condition_type": "STOP", # ストップ注文
                                             "side": contrary,
                                             "price": 0, # ここら??
                                             "trigger_price": loss,
                                             "size": ordersize
                                         }],
                                     #minute_to_expire=10000,
                                     #time_in_force="GTC"
                                     )

        print("ordered: "+ ordertype + str(ordersize) + "BTC at the price of " + str(orderprice))

        print(buy_btc)

        return buy_btc