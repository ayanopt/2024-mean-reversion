import subprocess
import os
import time
import datetime
import holidays

if datetime.date.today() in holidays.US():
    exit(0)
#start price updates

stock_list = ""
stocks = ["SPY"]
for stock in stocks:
    stock_list += stock
    stock_list += " "
subprocess.call(f"python3 stream_wrapper.py {stock_list}&",shell=True)
time.sleep(2)

#trade
for stock in stocks:
    subprocess.call(f"cd norm_trading; ./norm_data_loader.o {stock} &",shell=True)
    time.sleep(0.5)
#start data collection
folders = [f for f in os.listdir("../data") if "data" in f]
stocks = set()
for folder in folders:
    a_stock = folder.split("_")[0]
    b_stock = folder.split("_")[1]
    stocks.add(a_stock)
    stocks.add(b_stock)
    #subprocess.call(f"cd ../data/utils/; ./data_populator.o {a_stock} {b_stock} &",shell=True)