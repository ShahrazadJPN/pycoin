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

df = dG.DataGetter(path)  # DFオブジェクト生成・・・最新の取得情報が入っている。

api = pybitflyer.API(api_key=apiKey, api_secret=apiSecret)

border = 4 # 売買する乖離率の基準値
gotPrice = 1
count = 0

order = order.Order()
ordertype = "not_decided"
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
    money = collateral['collateral'] # 証拠金残高

    if isOrdering == []:
        isOrdering = False
    else:
        isOrdering = True

    now = datetime.now()
    print('now:', now)

    if count == 60: # 60秒経過時、csvにその時のデータを記入、かつ最新データをdfに代入
        Info.csv(product,path) # この時点でcsvには瞬間のデータが記述される
        count = 1
        df = dG.DataGetter.datas('')
    elif count == 0: # 初めて処理に入ったとき,dfにデータフレームを代入
        df = dG.DataGetter.datas('')
        count += 1
    else: # それ以外の時は単純にカウントを増やす
        count += 1

    row = len(df.index) - 1 # データフレームの行数マイナス1 = データフレームの最終行
    price_now = board['mid_price']

    dayDiv = df.iloc[row,6] # 1日移動平均に対する乖離率
    days5Div = df.iloc[row,7] # 5日移動平均に対する乖離率

    ewma1 = df.iloc[row,2] # 1min移動平均
    ewma5 = df.iloc[row,3] # 3min
    ewma25 = df.iloc[row,4]
    ewma3 = df.iloc[row,8] # 3日
    ewma6h = df.iloc[row,9] # 6時間移動平均

    div = (price_now - ewma25) / ewma25 * 100
    percent = price_now / gotPrice * 100 # 現在値/取得値 => 値上がり率

    if div > border and isOrdering is False and ewma1 > ewma3: # 25日平均に対する乖離率3%以上、上がり基調なので流れに乗って買う
        board = api.board(product_code=product)
        price_now = board['mid_price']
        gotPrice = price_now
        ordersize = Decimal(btc).quantize(Decimal('0.0001'), rounding=ROUND_DOWN)
        ordersize = float(ordersize)
        ordertype = "BUY"
        orderprice = int(price_now)

        order.buy_sell(ordertype, ordersize, orderprice,product,apiKey,apiSecret)
        Info.recorder(money, gotPrice, ordersize)

    elif div < border * -1 and isOrdering is False and ewma1 < ewma3: # 同上、下げ基調 6時間移動平均が1日移動平均より↓
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