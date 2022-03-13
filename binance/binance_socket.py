import websocket,json
import time
import threading

def subscribe(meth):
    socket=f"wss://stream-cloud.trbinance.com/ws"
    ws = websocket.WebSocket()
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
    return ws
def binancetr(ws):
    data = ws.recv()
    if data != "":
        msg = json.loads(data)
    else:
        msg = "data yok"
    return msg


def get_data(i):
    meth=methods_list[i]
    while True:
        data_dict[meth]=binancetr(method_dict[meth])

def print_data():
    while True:
        time.sleep(1)
        print(data_dict)
        with open('binance_data.json', 'w') as outfile:
            json.dump(data_dict, outfile)

methods_list=["btctry@depth5","ethtry@depth5","soltry@depth5","busdtry@depth5","chztry@depth5"]
method_dict={}
data_dict={}

for meth in methods_list:
    method_dict[meth]=subscribe(meth)

thread_list = []

for a in range(len(methods_list)):
    thread=threading.Thread(target=get_data,args=[a])
    time.sleep(1)
    thread_list.append(thread)
for thread in thread_list:
    thread.start()
threading.Thread(target=print_data).start()
"""
for thread in thread_list:
    thread.join()
threading.Thread(target=print_data).join()
"""
