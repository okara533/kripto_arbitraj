import websocket,json
import time
class Binance_socket:
    def __init__(self,coin_list):
        self.coin_list=coin_list
        self.data_dict={}
    def subscribe(self,meth):
        socket=f"wss://stream-cloud.trbinance.com/ws"
        ws=websocket.WebSocket()
        ws.connect(socket)
        ws.send(
            json.dumps(

                    {
                      "method": "SUBSCRIBE",
                      "params": [meth],
                      "id": 1
                    }

            )
        )
        data = ws.recv()
        if data != "":
            msg = json.loads(data)
        else:
            msg = "data yok"
        print(msg)
        print(f"{meth} web socket kanalı açıldı")

        return ws
    def binancetr(self,ws,asset,currency):
        data = ws.recv()

        if data != "":
            msg = json.loads(data)
            msg["asset"]=asset
            msg["currency"]=currency
        else:
            msg = "data yok"
        return msg


    def get_data(self,method_dict,a,asset,currency):
        while True:
            self.data_dict[a]=self.binancetr(method_dict[a],asset,currency)

    def print_data(self):
        while True:
            time.sleep(1)
            #print(self.data_dict)
            with open('binance_data.json', 'w') as outfile:
                json.dump(self.data_dict, outfile)
    def create_method_list(self):
        methods_list=[x.lower()+"@depth5" for x in self.coin_list]
        return methods_list
