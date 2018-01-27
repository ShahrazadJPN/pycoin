import pandas as pd
import matplotlib.pyplot as plt
import pybitflyer
import apiInfo
import time
from datetime import datetime

#空のデータフレームを作成 = お金残高用
account = pd.DataFrame(index=[], columns=['money'])

#df = pd.read_csv("http://api.bitcoincharts.com/v1/trades.csv?symbol=coincheckJPY",

df = pd.read_csv("C:\\Users\\Kei\\Desktop\\1sec.csv",
                 header=None,
                 parse_dates=True,
                 date_parser=lambda x: datetime.fromtimestamp(float(x)),
                 index_col='datetime',
                 names=['datetime', 'price', 'amount'])

df["price"].plot()
#df['ewma5'] = pd.ewma(df['price'],span=21000) # だいたい一日あたりの加重移動平均
df['ewma1day'] = pd.ewma(df['price'],span=60) # 1日の加重移動平均
df['ewma5days'] = pd.ewma(df['price'],span=180) # だいたい5日あたりの加重移動平均
df['ewma25days'] = pd.ewma(df['price'],span=3600) # だいたい25日あたりの加重移動平均
df['ewma1day'].plot()
df['ewma5days'].plot()
df['ewma25days'].plot()
df['divergence'] = (df['price'] - df['ewma25days']) / df['ewma25days'] * 100 # 5 日移動平均に対する界入り率
df['1dayDiv'] = (df['price'] - df['ewma1day']) / df['ewma1day'] * 100 # 1日移動平均に対するそのときの乖離率
df['5dayDiv'] = (df['price'] - df['ewma5days']) / df['ewma5days'] * 100 # 5日移動平均に対するそのときの乖離率

api = pybitflyer.API(api_key="WR95knYrj36CabGWHK1gdV", api_secret="2Gv0skryfEFZTBnJ3/WocvSrRVeIbi1vzsZ9sAurqaU=")

bought = False
sold = False
pos = False # ポジション有無
money = 10000000 # 1,000,000円
btc = 0
i = -1
gotPrice = 0

Info = apiInfo.Bitflyer()

for div in df['divergence']: # divは25日平均

    # df.iloc[i,0] <=これがその時のBTCの値段

    i += 1

    if i < 60:
        continue

    dayDiv = df.iloc[i,6] # 1日移動平均に対する乖離率
    days5Div = df.iloc[i,7] # 5日移動平均に対する乖離率

    ewma1 = df.iloc[i,2] # 一日移動平均
    ewma5 = df.iloc[i,3]
    ewma25 = df.iloc[i,4]

    print(div)

    failed = df.iloc[i,0] / gotPrice * 100 # 現在のポジションの取得値/現在値 <97% or 103%> で諦める？

    # if div > 22:
    #     giveBought = 95
    #     giveSold = 101
    # elif div < -22:
    #     giveBought = 99
    #     giveSold = 105
    # elif div > 15 and ewma1 < ewma5:
    #     giveBought = 99
    #     giveSold = 101
    # elif div < -15 and ewma1 > ewma5:
    #     giveBought = 99
    #     giveSold = 101
    # else:
    #     giveBought = 99
    #     giveSold = 101

    giveBought = 99
    giveSold = 101

    if  pos is False and ewma1 > ewma5 and div > 0.3:  #div > 4 and pos is False and ewma1 > ewma5: # 25日平均に対する乖離率3%以上、上がり基調なので流れに乗って買う

        btc = money/df.iloc[i,0]
        money = df.iloc[i,0]*btc
        #print ("bought btc having = "+ str(btc))
        bought = True
        pos = True
        gotPrice = df.iloc[i,0]
        series = pd.Series([money],index=account.columns)
        account = account.append(series, ignore_index=True)
    elif pos is False and ewma1 < ewma5 and div < -0.3: #div < -4 and pos is False and ewma1 < ewma5: # 同上、下げ基調
        btc = money/df.iloc[i,0]
        money = df.iloc[i, 0] * btc
        #print ("sold btc having = "+ str(btc))
        sold = True
        pos = True
        gotPrice = df.iloc[i, 0]
        series = pd.Series([money],index=account.columns)
        account = account.append(series, ignore_index=True)
    elif failed < giveBought and bought: # 買いポジション持ちだが、値段が下がってきたら諦めてポジション解消。-1%
        money = btc * df.iloc[i,0]
        btc = 0
        #print ("諦めた" + str(money))
        bought = False
        pos = False
        gotPrice = 0
        series = pd.Series([money],index=account.columns)
        account = account.append(series, ignore_index=True)
    elif failed > giveSold and sold: # 上記の逆。 +1%1
        money = (btc * gotPrice) + ((btc * gotPrice) - (btc * df.iloc[i,0]))
        btc = 0
       #print ("諦めた" + str(money))
        sold = False
        pos = False
        gotPrice = 0
        series = pd.Series([money],index=account.columns)
        account = account.append(series, ignore_index=True)
    elif failed > 100.05 and bought:  # 買いポジのあるときは0.03%値上がりで利確する
        money = btc * df.iloc[i,0]
        btc = 0
        bought = False
        pos = False
        gotPrice = 0
        series = pd.Series([money],index=account.columns)
        account = account.append(series, ignore_index=True)
    elif failed < 99.95 and sold: # 売りポジのときは0.03%値下がり
        money = (btc * gotPrice) + ((btc * gotPrice) - (btc * df.iloc[i,0]))
        btc = 0
        sold = False
        pos = False
        gotPrice = 0
        series = pd.Series([money], index=account.columns)
        account = account.append(series, ignore_index=True)



    print(i)

account.plot()

plt.show()