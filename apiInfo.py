import pybitflyer
import pandas as pd
from datetime import datetime as dt

class Bitflyer:

    def __init__(self,product,apiKey,apiSecret,path):

        self.api = pybitflyer.API(api_key=apiKey, api_secret=apiSecret)
        self.ticker = self.api.ticker(product_code=product)
        self.board = self.api.board(product_code=product)
        self.product = product
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.path = path

    def csv(self,product,path):

        self.ticker = self.api.ticker(product_code=product)
        self.board = self.api.board(product_code=product)

        time = self.ticker['timestamp']
        lastPrice = self.ticker['ltp'] # 最終取引値 -> 値動きの判断に利用する
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

        w.to_csv(path, index=False, encoding="utf-8",mode='a', header=False)    #CSVにかきこわえる

    def recorder(self,money,price,btc):

        self.money = money
        self.price = price
        self.btc = btc

        time = self.ticker['timestamp']
        time = time.replace("T", " ")

        w = pd.DataFrame([[self.money,time,self.price]])

        w.to_csv(self.path, index=False, encoding="utf-8",mode='a', header=False)    #CSVにかきこわえる

        print("資産：" + str(money) + "　売買価格：" + str(price))

# このクラスで、apiで取得したティッカー情報を蓄積していく。LTP(最終取引価格)を使って値段とする？
# ポジションを持っていないときはbestbid, bestaskで売り買い。買えるだけ買う。