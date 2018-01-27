import pandas as pd
import matplotlib.pyplot as plt
import pybitflyer
import apiInfo
import time
import dataGetter as dG
from datetime import datetime
import sys
import order
from decimal import (Decimal, ROUND_DOWN)

apiKey = "WR95knYrj36CabGWHK1gdV"
apiSecret = "2Gv0skryfEFZTBnJ3/WocvSrRVeIbi1vzsZ9sAurqaU="
path = "C:\\Users\\Kei\\Desktop\\bitflyer2.csv"
product = "FX_BTC_JPY"

df = pd.DataFrame(index=[],columns=[])
df = dG.DataGetter(path)  # Create dataframe obj.
api = pybitflyer.API(api_key=apiKey, api_secret=apiSecret)

border = 4 # border of divergence to decide to buy/sell
gotPrice = 1 #
count = 0 #

order = order.Order()
ordertype = ""
ordersize = 0
orderprice = 0

Info = apiInfo.Bitflyer(product,apiKey,apiSecret,path)

while True:
    time.sleep(0.5)

    ticker = api.ticker(product_code=product)
    board = api.board(product_code=product)

    isOrdering = api.getparentorders(product_code=product,
                                    parent_order_state="ACTIVE")

    collateral = api.getcollateral()
    money = collateral['collateral'] # cash in your account

    if isOrdering == []:
        isOrdering = False
    else:
        isOrdering = True

    now = datetime.now()
    print('now:', now)

    if count == 60: # 60 secs (circa)
        Info.csv(product,path) #
        count = 1
        df = dG.DataGetter.datas('')
    else: # それ以外
        df = dG.DataGetter.datas('')
        count += 1

    row = len(df.index) - 1 # last row of the df
    price_now = board['mid_price']


    ewma1 = df.iloc[row,2] # ewma 1 day
    ewma5 = df.iloc[row,3] # 5 days
    ewma25 = df.iloc[row,4] 25 days
    ewma3 = df.iloc[row,8] # 3 days

    div = (price_now - ewma25) / ewma25 * 100
    percent = price_now / gotPrice * 100 #

    if div > border and isOrdering is False and ewma1 > ewma3: #
        board = api.board(product_code=product)
        price_now = board['mid_price']
        gotPrice = price_now
        ordersize = Decimal(btc).quantize(Decimal('0.0001'), rounding=ROUND_DOWN)
        ordersize = float(ordersize)
        ordertype = "BUY"
        orderprice = int(price_now)

        order.buy_sell(ordertype, ordersize, orderprice,product,apiKey,apiSecret)
        Info.recorder(money, gotPrice, ordersize)

    elif div < border * -1 and isOrdering is False and ewma1 < ewma3: #
        board = api.board(product_code=product)
        price_now = board['mid_price']
        btc = money/price_now
        gotPrice = price_now
        ordersize = Decimal(btc).quantize(Decimal('0.0001'), rounding=ROUND_DOWN)
        ordersize = float(ordersize)
        ordertype = "SELL"
        orderprice = int(price_now)

        order.buy_sell(ordertype, ordersize, orderprice,product, apiKey, apiSecret)
        Info.recorder(money, gotPrice, ordersize)