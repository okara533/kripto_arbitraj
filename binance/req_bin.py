import requests

def binance_currency_list():
    general_data=requests.get("https://www.trbinance.com/open/v1/common/symbols").json()
    general_list=general_data["data"]["list"]
    asset_list=[]
    currency_list=[]
    for item in general_list:
        asset_list.append(item["baseAsset"])
        currency_list.append(item["quoteAsset"])
    return asset_list,currency_list
