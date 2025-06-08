import sys,json,datetime,math,os, trade_wrapper
relative_path = sys.argv[0].split("trade_operations/norm_trade.py")[0]


# No trades after 3:40pm EST
dt_now = datetime.datetime.now()
if dt_now.hour == 15 and dt_now.minute >= 40:
    path_to_trades = f"{relative_path}trades/"
    for trade_file in os.listdir(path_to_trades):
        trade_wrapper.close_norm_position(path_to_trades+trade_file)
    trade_wrapper.liquidate()
    exit(0)
    
#SPY 121 b/s o/c
stock = sys.argv[1]
strat = sys.argv[2]
buy_or_sell = sys.argv[3]
open_or_close = sys.argv[4]

# Dont sell_to_open QQQ
if buy_or_sell == "sell" and open_or_close == "open" and stock == "QQQ" :
    exit()

trade_file = f"{relative_path}trades/{stock}_{strat}_norm_trade.json"

# close trade if exists
if open_or_close == "close":
    if os.path.isfile(trade_file):
        trade_wrapper.close_norm_position(trade_file)
    exit(0)
    
    
trade_capital = (0.02*trade_wrapper.get_capital())

# get price from trade wrapper
stock_price = float(trade_wrapper.get_price(stock))
stock_qty = max(round(trade_capital/stock_price),1) # qty >= 1

if buy_or_sell == "sell":
    trade_wrapper.trade(stock,trade_wrapper.OrderSide('sell'),stock_qty)
else:    
    trade_wrapper.trade(stock,trade_wrapper.OrderSide('buy'),stock_qty)

json_out = {
    "stock_symbol":stock,
    "stock_qty":stock_qty,
    "direction":buy_or_sell
}
with open(trade_file, 'w') as fp:
    json.dump(json_out, fp)
    