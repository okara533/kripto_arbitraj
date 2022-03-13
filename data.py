import requests
import pandas as pd
import json
import time
import os
import sys
import os
cwd=os.path.abspath(os.getcwd())
sys.path.insert(0, cwd+'/icrypex')
import req_cry

class Data:
    def __init__(self):
        self.main_df=pd.DataFrame()
    def symbol_chopper(self,x,method="asset"):
        currency=["USDT","TRY","BTC","BUSD","BNB","USDC"]
        flag=False
        for cur in currency:
            if cur==x[-1*len(cur):]:
                if method=="asset":
                    y=x.split(cur)[0]
                else:
                    y=cur
                flag=True
            elif flag:
                pass
            else:
                y="YOK"
        return y

    def btcturk(self):
        result=requests.get("https://api.btcturk.com/api/v2/ticker").json()
        df=pd.DataFrame(result["data"])
        df["asset"]=df["pairNormalized"].apply(lambda x:x.split("_")[0])
        df["currency"]=df["pairNormalized"].apply(lambda x:x.split("_")[1])
        df=df[["asset","currency","bid","ask"]]
        df["exchange"]="BtcTurk"
        return df

    def paribu(self):
        result=requests.get("https://www.paribu.com/ticker").json()
        df=pd.DataFrame()
        df["asset"]=[x.split("_")[0] for x in result.keys()]
        df["currency"]=[x.split("_")[1] for x in result.keys()]
        df["currency"]=df["currency"].apply(lambda x:"TRY" if x=="TL" else x)
        ask_list=[]
        bid_list=[]
        for asset in result.keys():
            ask=result[asset]["lowestAsk"]
            ask_list.append(ask)
            bid=result[asset]["highestBid"]
            bid_list.append(bid)
        df["bid"]=bid_list
        df["ask"]=ask_list
        df["exchange"]="Paribu"
        return df

    def binancetr(self):
        result=pd.read_json("binance/binance_data.json")
        check=len(result)>3
        while not check:
            time.sleep(0.3)
            result=pd.read_csv("binance/binance_data.json")
            check=len(result)>3

        df_list=[]
        for asset in result.columns:
            df_dict={}
            df_dict["asset"]=result[asset]["asset"]
            df_dict["currency"]=result[asset]["currency"]
            df_dict["bid"]=result[asset]["bids"][0][0]
            df_dict["ask"]=result[asset]["asks"][0][0]
            df_list.append(df_dict)
        df=pd.DataFrame(df_list)
        df["exchange"]="BinanceTR"
        #print(df)
        return df
    def bitexen(self):
        result=requests.get("https://www.bitexen.com/api/v1/ticker/").json()
        result=result["data"]["ticker"]
        df_list=[]
        for coin in result.keys():
            df_dict={}
            df_dict["asset"]=result[coin]["market"]["base_currency_code"]
            df_dict["currency"]=result[coin]["market"]["counter_currency_code"]
            df_dict["bid"]=result[coin]["bid"]
            df_dict["ask"]=result[coin]["ask"]
            df_dict["exchange"]="Bitexen"
            df_list.append(df_dict)
        df=pd.DataFrame(df_list)
        return df
    def fexobit(self):
        df=pd.read_csv("fexobit/fexobit_data.csv")
        check=len(df)>3
        while not check:
            time.sleep(0.3)
            df=pd.read_csv("fexobit/fexobit_data.csv")
            check=len(df)>3


        df["asset"]=df.iloc[:,0].apply(self.symbol_chopper)
        df["currency"]=df.iloc[:,0].apply(self.symbol_chopper,args=["currency"])
        df["exchange"]="Fexobit"
        df=df[["asset","currency","bid","ask","exchange"]]
        return df

    def bitci(self):
        api={"apitoken":"nkM+r4QxK0END2A9p/DpzV4dZ6uTbBcKjSBNYLv1LwVAUQkrW77FzGc3TqsO/v4Et0mVhNhD0rk2nkTumHwSrinxv3NxnXUKAy83JZ8D2zJeAv/gd6W2pyqaJYlrLuZoMOOwxuAW2GOi0Bj7jdg1MGOnpU2z2+iRiRiwttJgVJHv94BHtYMVbpWFtwcXqsQg"}
        result=requests.get("https://api.binance.com/api/v3/ticker/bookTicker",headers=api).json()
        df=pd.DataFrame(result)
        df["asset"]=df.iloc[:,0].apply(self.symbol_chopper)
        df["currency"]=df.iloc[:,0].apply(self.symbol_chopper,args=["currency"])
        df["exchange"]="Bitçi"
        df=df[["asset","currency","bidPrice","askPrice","exchange"]]
        df.columns=["asset","currency","bid","ask","exchange"]
        return df

    def binance(self):
        result=requests.get("https://api.binance.com/api/v3/ticker/bookTicker").json()
        df=pd.DataFrame(result)
        df["asset"]=df["symbol"].apply(self.symbol_chopper)
        df["currency"]=df["symbol"].apply(self.symbol_chopper,args=["currency"])
        df["exchange"]="Binance"
        df=df[["asset","currency","bidPrice","askPrice","exchange"]]
        df.columns=["asset","currency","bid","ask","exchange"]
        return df

    def ftx(self):
        result=requests.get("https://ftx.com/api/markets").json()
        df=pd.DataFrame(result["result"])
        df=df[df["type"]=="spot"]
        df=df[["baseCurrency","quoteCurrency","bid","ask"]]
        df["exchange"]="FTX"
        df.columns=["asset","currency","bid","ask","exchange"]
        return df

    def icrypex(self):
        s=requests.Session()
        a_l,c_l=req_cry.icrypex_currency_list(s)
        df=req_cry.data_process(s,a_l,c_l)
        df["exchange"]="Icrypex"
        return df

    def concanate_df(self):

        #btcturk
        try:
            btcturk_df=self.btcturk()
        except Exception as e:
            btcturk_df=pd.DataFrame()
            print("BTCTURK")
            print(e)
        #paribu
        try:
            paribu_df=self.paribu()
        except Exception as e:
            paribu_df=pd.DataFrame()
            print("paribu")
            print(e)
        #bitexen
        try:
            bitexen_df=self.bitexen()
        except Exception as e:
            bitexen_df=pd.DataFrame()
            print("bitexen")
            print(e)
        #fexobit
        try:
            fexobit_df=self.fexobit()
        except Exception as e:
            fexobit_df=pd.DataFrame()
            print("fexobit")
            print(e)
        #binanceTR
        try:
            binancetr_df=self.binancetr()
        except Exception as e:
            binancetr_df=pd.DataFrame()
            print("binanceTR")
            print(e)
        #binance
        try:
            binance_df=self.binance()
        except Exception as e:
            binance_df=pd.DataFrame()
            print("binance")
            print(e)
        #ftx
        try:
            ftx_df=self.ftx()
        except Exception as e:
            ftx_df=pd.DataFrame()
            print("ftx")
            print(e)

        #icrypex
        try:
            icrypex_df=self.icrypex()
        except Exception as e:
            icrypex_df=pd.DataFrame()
            print("icrypex")
            print(e)

        #icrypex
        try:
            bitci_df=self.bitci()
        except Exception as e:
            bitci_df=pd.DataFrame()
            print("bitci")
            print(e)
        self.main_df=pd.concat([btcturk_df,paribu_df,bitexen_df,fexobit_df,binancetr_df,binance_df,ftx_df,icrypex_df,bitci_df])
        self.main_df=self.main_df[(self.main_df["asset"]!="YOK")&(self.main_df["currency"]!="YOK")]
        self.main_df["bid"]=pd.to_numeric(self.main_df["bid"])
        self.main_df["ask"]=pd.to_numeric(self.main_df["ask"])
