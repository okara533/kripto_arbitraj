import xlwings as xw
import pandas as pd
import time
import numpy as np
from data import Data

class Excel_pars:
    def __init__(self,excel_file):
        self.raw_data=pd.DataFrame()
        self.asset=["BTC"]
        self.currency=["TRY"]
        self.main_exchange="BtcTurk"
        self.df=pd.DataFrame()
        self.wb=xw.Book(excel_file)
    def data_pull(self):
        get_data=Data()
        get_data.concanate_df()
        self.raw_data=get_data.main_df
    def data_process(self,a,c):
        partial_df=pd.DataFrame()
        filter_df=self.raw_data[(self.raw_data["asset"]==a)&(self.raw_data["currency"]==c)]
        filter_len=len(filter_df)
        if filter_len>0:
            #bid
            filter_df_bid=filter_df.sort_values("bid",ascending=False)
            partial_df["filter_df_bid_exchange"]=filter_df_bid["exchange"].values
            partial_df["filter_df_bid"]=filter_df_bid["bid"].values
            #ask
            filter_df_ask=filter_df.sort_values("ask",ascending=True)
            partial_df["filter_df_ask"]=filter_df_ask["ask"].values
            partial_df["filter_df_ask_exchange"]=filter_df_ask["exchange"].values
            #spread
            filter_df["spread"]=filter_df["ask"]-filter_df["bid"]
            filter_df_spread=filter_df.sort_values("spread",ascending=True)
            partial_df["filter_df_spread_exchange"]=filter_df_spread["exchange"].values
            partial_df["filter_df_spread"]=filter_df_spread["spread"].values
            partial_df["filter_df_spread_perc"]=(filter_df_spread["spread"].values)/(filter_df_spread["bid"].values)
            #arbt
            fexo_df=filter_df[filter_df["exchange"]==self.main_exchange]
            if len(fexo_df)>0:
                filter_df=filter_df[filter_df["exchange"]!=self.main_exchange]
                filter_df=filter_df.sort_values("exchange",ascending=True)
                fex_ask=fexo_df["ask"].values[0]
                fex_bid=fexo_df["bid"].values[0]
                yuksek_arbt_df=np.append((filter_df["ask"]-fex_bid)*-1,None)
                dusuk_arbt_df=np.append(filter_df["bid"]-fex_ask,None)
                partial_df["filter_df_arbt_exchange"]=np.append(filter_df["exchange"].values,None)
                partial_df["filter_df_yuksek_arbt"]=yuksek_arbt_df
                partial_df["filter_df_yuksek_arbt_perc"]=[x/fex_ask if x!=None else None for x in yuksek_arbt_df]

                partial_df["filter_df_dusuk_arbt"]=dusuk_arbt_df
                partial_df["filter_df_dusuk_arbt_perc"]=[x/fex_bid if x!=None else None for x in dusuk_arbt_df ]

        return partial_df

    def data_concat(self):
        self.df=pd.DataFrame()
        for a,c in zip(self.asset,self.currency):
            partial_df=self.data_process(a,c)
            if len(partial_df)>0:
                number_of_empty=10-len(partial_df)
                empty_data=[]
                for i in range(number_of_empty):
                    empty_list=[None for x in partial_df.columns]
                    empty_data.append(empty_list)
                empty_df=pd.DataFrame(empty_data,columns=partial_df.columns)
                partial_df=partial_df.append(empty_df)

                self.df=pd.concat([self.df,partial_df])

    def get_asset_currency(self):
        wb=self.wb
        sht=wb.sheets["config"]
        self.asset=sht.range("A2:A100").value
        self.currency=sht.range("B2:B100").value
        self.main_exchange=sht.range("D2").value
    def parse_excel(self,):
        wb=xw.Book("piyasa_takip.xlsx")
        sht=wb.sheets["data"]
        sht.range("A1").value=self.df
