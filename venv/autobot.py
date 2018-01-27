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

#空のデータフレームを作成 = お金残高用
#account = pd.DataFrame(index=[], columns=['money'])

df = pd.DataFrame(index=[],columns=[])

df = dG.DataGetter()  # DFオブジェクト生成・・・最新の取得情報が入っている。

api = pybitflyer.API(api_key="WR95knYrj36CabGWHK1gdV", api_secret="2Gv0skryfEFZTBnJ3/WocvSrRVeIbi1vzsZ9sAurqaU=")

border = 0.6 # 売買する乖離率の基準値

bought = False # 買いポジション？
sold = False #
pos = False # ポジション有無

money = 1000000 # 1,000,000円
btc = 0
gotPrice = 1

giveBought = 99 # 買いポジを諦めるパーセント
giveSold = 101 # 売りポジを諦めるパーセント

count = 0

order = order.Order()

ordertype = "not_decided"
ordersize = 0
orderprice = 0

Info = apiInfo.Bitflyer()

while True:
    time.sleep(0.5)

    ticker = api.ticker(product_code="FX_BTC_JPY")
    board = api.board(product_code="FX_BTC_JPY")

    isOrdering = api.getparentorders(product_code="FX_BTC_JPY",
                                    parent_order_state="ACTIVE")

    collateral = api.getcollateral()
    money = collateral['collateral'] # 証拠金残高

    if isOrdering == []:
        isOrdering = False
    else:
        isOrdering = True

    now = datetime.now()
    print('now:', now)

    if count == 2: # 60秒経過時、csvにその時のデータを記入、かつ最新データをdfに代入
        Info.csv() # この時点でcsvには瞬間のデータが記述される
        count = 1
        df = dG.DataGetter.datas('')

        # print("{}{: >25}{}{: >10}{}".format('|', 'Variable Name', '|', 'Memory', '|'))
        # print(" ------------------------------------ ")
        # for vars in dir():
        #     if vars.startswith("_") == 0:
        #         print("{}{: >25}{}{: >10}{}".format('|', vars, '|', sys.getsizeof(eval(vars)), '|'))

    elif count == 0: # 初めて処理に入ったとき,dfにデータフレームを代入
        df = dG.DataGetter.datas('')
        count += 1
    else: # それ以外の時は単純にカウントを増やす
        count += 1

    ##################ここから取引判定していく

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

    # div = df.iloc[row,5] # その時の25日移動平均線に対する乖離率 <-ここに(self.df['price'] - self.df['ewma25days']) / self.df['ewma25days'] * 100 その瞬間tickerから取得した値を入れる！

    percent = price_now / gotPrice * 100 # 現在値/取得値 => 値上がり率

    if isOrdering is False and ewma1 > ewma5 and div > border: #div > border and isOrdering is False and ewma1 > ewma3: # 25日平均に対する乖離率3%以上、上がり基調なので流れに乗って買う
        board = api.board(product_code="FX_BTC_JPY")
        price_now = board['mid_price']
        btc = money/price_now
        #print ("bought btc having = "+ str(btc))
        bought = True
        pos = True
        gotPrice = price_now

        ordersize = Decimal(btc).quantize(Decimal('0.0001'), rounding=ROUND_DOWN)
        ordersize = float(ordersize)

        ordertype = "BUY"

        orderprice = int(price_now)

        order.buy_sell(ordertype, ordersize, orderprice)

        Info.recorder(money, gotPrice, ordersize)

    elif isOrdering is False and ewma1 < ewma5 and div < border * -1: # div < border * -1 and isOrdering is False and ewma1 < ewma3: # 同上、下げ基調 6時間移動平均が1日移動平均より↓
        board = api.board(product_code="FX_BTC_JPY")
        price_now = board['mid_price']
        btc = money/price_now
        #money = price_now * btc
        #print ("sold btc having = "+ str(btc))
        sold = True
        pos = True
        gotPrice = price_now

        ordersize = Decimal(btc).quantize(Decimal('0.0001'), rounding=ROUND_DOWN)
        ordersize = float(ordersize)

        ordertype = "SELL"

        orderprice = int(price_now)

        order.buy_sell(ordertype, ordersize, orderprice)

        Info.recorder(money, gotPrice, ordersize)

    # elif percent < giveBought and bought: # 買いポジション持ちだが、値段が下がってきたら諦めてポジション解消。-1%
    #     money = btc * price_now
    #     btc = 0
    #     #print ("諦めた" + str(money))
    #     bought = False
    #     pos = False
    #     gotPrice = 1
    #
    #    # Info.recorder(money, gotPrice, btc)
    #
    # elif percent > giveSold and sold: # 上記の逆。 +1%
    #     money = btc * price_now
    #     btc = 0
    #    #print ("諦めた" + str(money))
    #     sold = False
    #     pos = False
    #     gotPrice = 1
    #
    #   # Info.recorder(money, gotPrice, btc)
    #
    # elif percent > 100.3 and bought:  # 買いポジのあるときは0.03%値上がりで利確する
    #     money = btc * price_now
    #     btc = 0
    #     bought = False
    #     pos = False
    #     gotPrice = 1
    #
    #   #  Info.recorder(money, gotPrice, btc)
    #
    # elif percent < 99.7 and sold:  # 売りポジのときは0.03%値下がり
    #     money = btc * price_now
    #     btc = 0
    #     sold = False
    #     pos = False
    #     gotPrice = 1
    #
    #   #  Info.recorder(money, gotPrice, btc)
    #
    #
    #
    # # やるべきこと・・・実際の取引を行うシステムを作る。
    # # dataframeに time, mid_price, amount を入れる
    # # そのあとewmaなど必要な情報をぶちこみ、実際に発注していく


account.plot()

plt.show()