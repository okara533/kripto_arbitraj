

from excel_oop import Excel_pars
import time
import threading




def excel_thread():
    while True:

        excel_app.data_pull()
        time.sleep(5)
        excel_app.get_asset_currency()
        excel_app.data_concat()
        excel_app.parse_excel()

if __name__ == '__main__':
    excel_app=Excel_pars("piyasa_takip.xlsx")
    excel_thread()
