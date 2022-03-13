
"""
import sys
import os
cwd=os.path.abspath(os.getcwd())
sys.path.insert(0, cwd+'/binance')
"""
import time
import threading
from binance_socket_oop import Binance_socket
from req_bin import binance_currency_list
import requests

asset_list,currency_list=binance_currency_list()
print(asset_list)
coin_list=[(a+c).lower() for a,c in zip(asset_list,currency_list)]

socket_data=Binance_socket(coin_list)
method_dict={}
data_dict={}
method_list=socket_data.create_method_list()
print(method_list)
for meth in method_list:
    method_dict[meth]=socket_data.subscribe(meth)
print(method_dict)
thread_list = []
for a in range(len(method_list)):
    thread=threading.Thread(target=socket_data.get_data,args=(method_dict,method_list[a],asset_list[a],currency_list[a]))
    time.sleep(1)
    thread_list.append(thread)
for thread in thread_list:
    thread.start()
threading.Thread(target=socket_data.print_data).start()
