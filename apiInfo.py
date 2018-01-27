import pybitflyer
import pandas as pd
from datetime import datetime as dt

class Bitflyer:
    def __init__(self):
        self.api = pybitflyer.API(api_key="WR95knYrj36CabGWHK1gdV", api_secret="2Gv0skryfEFZTBnJ3/WocvSrRVeIbi1vzsZ9sAurqaU=")
        self.ticker = self.api.ticker(product_code="FX_BTC_JPY")
        self.board = self.api.board(product_code="FX_BTC_JPY")

    def csv(self):

        self.ticker = self.api.ticker(product_code="FX_BTC_JPY")
        self.board = self.api.board(product_code="FX_BTC_JPY")

        time = self.ticker['timestamp']
        bestAsk = self.ticker['best_ask'] # 一番安い売値 = 買うときはこちら
        bestBid = self.ticker['best_bid'] # 一番高い買値 = 売るときはこちら
        lastPrice = self.ticker['ltp'] # 最終取引値 -> 値動きの判断に利用する
        volume = self.ticker['volume']
        midPrice = self.board['mid_price']

        time = time.replace("T", " ")

        if time.find(".") == - 1:
            tdatetime = dt.strptime(time, '%Y-%m-%d %H:%M:%S')
            tdatetime = tdatetime.timestamp()
        else:
            tdatetime = dt.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
            tdatetime = tdatetime.timestamp()

        time = tdatetime

        print(time)

        w = pd.DataFrame([[time, lastPrice, midPrice]]) # 取得したティッカーをデータフレームに入れる

        w.to_csv("C:\\Users\\Kei\\Desktop\\bitflyer2.csv", index=False, encoding="utf-8",mode='a', header=False)    #CSVにかきこわえる

    def recorder(self,money,price,btc):

        self.money = money
        self.price = price
        self.btc = btc

        time = self.ticker['timestamp']
        time = time.replace("T", " ")

        w = pd.DataFrame([[self.money,time,self.price]])

        w.to_csv("C:\\Users\\Kei\\Desktop\\record.csv", index=False, encoding="utf-8",mode='a', header=False)    #CSVにかきこわえる

        print("資産：" + str(money) + "　売買価格：" + str(price))

# このクラスで、apiで取得したティッカー情報を蓄積していく。LTP(最終取引価格)を使って値段とする？
# ポジションを持っていないときはbestbid, bestaskで売り買い。買えるだけ買う。