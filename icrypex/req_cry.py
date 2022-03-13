import requests
import time
from datetime import datetime
import pandas as pd

def icrypex_currency_list(s):
    general_data=s.get("https://api.icrypex.com/open/v1/common/symbols").json()
    general_list=general_data["Data"]
    asset_list=[]
    currency_list=[]
    for item in general_list:
        asset_list.append(item["baseasset"])
        currency_list.append(item["quoteAsset"])
    return asset_list,currency_list

def get_orderbook(a,c,s):
    general_data=s.get(f"https://api.icrypex.com/open/v1/market/depth?symbol={a}/{c}&limit=500").json()
    return general_data


def data_process(s,a_l,c_l):
    df_list=[]
    for a,c in zip(a_l,c_l):
        symbol_bests={}
        bid_ask=get_orderbook(a,c,s)["Data"]

        best_bid=float(bid_ask["bids"][-1]["price"])
        count_bid=-1
        while best_bid<float(bid_ask["bids"][count_bid-1]["price"]):
            count_bid-=1
            best_bid=float(bid_ask["bids"][count_bid]["price"])

        best_ask=float(bid_ask["asks"][-1]["price"])
        count_ask=-1
        while best_ask>float(bid_ask["asks"][count_ask-1]["price"]):
            count_ask-=1
            best_ask=float(bid_ask["asks"][count_ask]["price"])
        count=-1
        while best_ask<best_bid:
            best_ask=float(bid_ask["asks"][count_ask+count]["price"])
            best_bid=float(bid_ask["bids"][count_bid+count]["price"])
            count-=1

        symbol_bests["asset"]=a
        symbol_bests["currency"]=c
        symbol_bests["bid"]=best_bid
        symbol_bests["ask"]=best_ask
        df_list.append(symbol_bests)
    df=pd.DataFrame(df_list)
    return df
