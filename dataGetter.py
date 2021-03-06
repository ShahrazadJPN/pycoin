import pandas as pd
import matplotlib.pyplot as plt
import pybitflyer
import apiInfo
import time
from datetime import datetime
import sys

class DataGetter:

    df = pd.DataFrame(index=[],columns=[])
    df_length = 0
    df_path = "tobedecided"

    def __init__(self,path): # インスタンス生成と同時にその瞬間のデータを引っ張り出す
        DataGetter.df_path = path

        DataGetter.df = pd.read_csv(path,  # dataframe を代入しなおす
                         header=None,
                         parse_dates=True,
                         date_parser=lambda x: datetime.fromtimestamp(float(x)),
                         index_col='datetime',
                         names=['datetime', 'price', 'amount'])

        DataGetter.df["price"].plot()
        DataGetter.df['ewma1day'] = pd.ewma(DataGetter.df['price'], span=1440)  # 1日の加重移動平均
        DataGetter.df['ewma5days'] = pd.ewma(DataGetter.df['price'], span=7200)  # だいたい5日あたりの加重移動平均
        DataGetter.df['ewma25days'] = pd.ewma(DataGetter.df['price'], span=36000)  # だいたい25日あたりの加重移動平均
        DataGetter.df['ewma1day'].plot()
        DataGetter.df['ewma5days'].plot()
        DataGetter.df['ewma25days'].plot()
        DataGetter.df['divergence'] = (DataGetter.df['price'] - DataGetter.df['ewma25days']) / DataGetter.df['ewma25days'] * 100  # 5 日移動平均に対する界入り率
        DataGetter.df['1dayDiv'] = (DataGetter.df['price'] - DataGetter.df['ewma1day']) / DataGetter.df['ewma1day'] * 100  # 1日移動平均に対するそのときの乖離率
        DataGetter.df['5dayDiv'] = (DataGetter.df['price'] - DataGetter.df['ewma5days']) / DataGetter.df['ewma5days'] * 100  # 5日移動平均に対するそのときの乖離率
        DataGetter.df['ewma3days'] = pd.ewma(DataGetter.df['price'], span=4320)  # 3日移動平均
        DataGetter.df['ewma6hours'] = pd.ewma(DataGetter.df['price'], span=360)  # 6時間移動平均

        DataGetter.df_length = len(DataGetter.df.index)

    def datas(self):

        DataGetter.df = pd.read_csv(DataGetter.df_path,  # dataframe を代入しなおす
                         header=None,
                         parse_dates=True,
                         date_parser=lambda x: datetime.fromtimestamp(float(x)),
                         index_col='datetime',
                         names=['datetime', 'price', 'amount'])

        DataGetter.df['ewma1day'] = pd.ewma(DataGetter.df['price'], span=1440)  # 1日の加重移動平均
        DataGetter.df['ewma5days'] = pd.ewma(DataGetter.df['price'], span=7200)  # だいたい5日あたりの加重移動平均
        DataGetter.df['ewma25days'] = pd.ewma(DataGetter.df['price'], span=36000)  # だいたい25日あたりの加重移動平均
        DataGetter.df['divergence'] = (DataGetter.df['price'] - DataGetter.df['ewma25days']) / DataGetter.df['ewma25days'] * 100  # 5 日移動平均に対する界入り率
        DataGetter.df['1dayDiv'] = (DataGetter.df['price'] - DataGetter.df['ewma1day']) / DataGetter.df['ewma1day'] * 100  # 1日移動平均に対するそのときの乖離率
        DataGetter.df['5dayDiv'] = (DataGetter.df['price'] - DataGetter.df['ewma5days']) / DataGetter.df['ewma5days'] * 100  # 5日移動平均に対するそのときの乖離率
        DataGetter.df['ewma3days'] = pd.ewma(DataGetter.df['price'], span=4320)  # 3日移動平均
        DataGetter.df['ewma6hours'] = pd.ewma(DataGetter.df['price'], span=360)  # 6時間移動平均

        DataGetter.df_length = len(DataGetter.df.index)

        return DataGetter.df

