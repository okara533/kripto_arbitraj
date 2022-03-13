import websocket,json
import pandas as pd
import time
class Fexobit_socket:
    def __init__(self):
        self.df=pd.DataFrame({"bid":0,"ask":0},index=["YOK"])
    def connect_socket(self):
        socket="wss://stream.fexobit.com/pricechange/full?x-auth=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MzU5MzE2NDEsImp0aSI6IjNjMmExMjFiLTNkNTktNDE5My1iZWU2LTJiMjFkNmM4MTdhZCJ9.rI_VmBP3rQa5oMGhPC_fS6Noro4WwNh80rTToFZhq5c"
        ws=websocket.WebSocket()
        ws.connect(socket)
        return ws
    def get_data(self,ws):
        #ws=self.connect_socket()
        data = ws.recv()
        if data != "":
            msg = json.loads(data)

        else:
            msg = "data yok"
        return msg

    def prepare_data(self,ws):
        while True:
            msg=self.get_data(ws)
            try:
                check=self.df.loc[msg["symbol"]]
            except:
                check=[]
            df_=pd.DataFrame({"bid":msg["bestBid"],"ask":msg["bestAsk"]},index=[msg["symbol"]])

            if len(check)==0:
                self.df=pd.concat([self.df,df_])
            else:
                self.df.drop(msg["symbol"],inplace=True)
                self.df=pd.concat([self.df,df_])
    def print_data(self):
        while True:
            self.df.to_csv("fexobit_data.csv")
            time.sleep(0.5)
