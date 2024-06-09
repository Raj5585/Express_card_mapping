# import requests
# def get_exchange_rates(destination_currency, currency_date):
#     url = "http://192.168.100.197:9001/OnlineAccOpening/getequivalentinfo" 
#     payload = {
#         "destination_Currency": destination_currency,
#         "currency_Date": currency_date
#     }
#     auth = ('CRMUser1', 'CRM@p1')
#     token =  'Q1JNVXNlcjpDUk1AcDE='
#     response = requests.post(url, json=payload,  headers={'Authorization': f'Token {token}'}, timeout= 30)
#     print(response)
#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#         buy_rate = data.get("buy_Rate")
#         sell_rate = data.get("sell_Rate")
#         mid_rate = data.get("mid_Rate")
#         print buy_rate, sell_rate, mid_rate
#     else:
#         print("Failed to retrieve exchange rates. Status code:", response.status_code)
#         return None, None, None
# destination_currency = "USD"
# currency_date = "15-May-2023"
# buy_rate, sell_rate, mid_rate = get_exchange_rates(destination_currency, currency_date)
# mid_rate_dollar = mid_rate
# seling_rate_dollar = sell_rate
# print(mid_rate_dollar)
# print(seling_rate_dollar)
# import cx_Oracle,oracledb
# import pandas as pd

# query = " select  ACT_AMT from sblpsd.tbl_daily_transaction where Ref_NUM = '001493066345'  " 

# user = 'fcjglhist'
# password = 'fcjglhist'
# host_name = '10.60.100.1'
# port = '1521'
# service = 'SBLDB'
# try:
#     dsn_tns = oracledb.makedsn(host_name, port, service_name=service) 
#     conn = oracledb.connect(user=user,  password=password, dsn=dsn_tns )
#     cursor = conn.cursor()
#     cursor.execute(query)
#     data = cursor.fetchone()
#     print(conn)
#     # df_ora = pd.read_sql(query, con=conn)

#     print(df_ora)
#     conn.close()
# except Exception as e:
#     print(f'error occured { e }')
    
import shutil
from app  import Constants


def zip_folder(folder_path, zip_filename):
    shutil.make_archive(zip_filename, 'zip', folder_path)

zip_folder(Constants.final_path,f'BTRT_{Constants.present_date}')