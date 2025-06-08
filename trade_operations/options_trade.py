# This file remains WIP



import sys,math,datetime,math,os,trade_wrapper
relative_path = sys.argv[0].split("options_trade.py")[0]

# No trades after 4pm EST
# also close all trades
dt_now = datetime.datetime.now()
if dt_now.hour == 15 and dt_now.minute >= 30:
    for trade in os.listdir(f"{relative_path}trades"):
        trade_wrapper.sell_trades(trade_file = relative_path+"trades/"+trade)
    exit(0)
    
#SPY QQQ 500.350000 431.465000 121
call = sys.argv[1]
put = sys.argv[2]
long_price = float(sys.argv[3])
short_price = float(sys.argv[4])
strat = (sys.argv[5])

if strat == "121":
    exit()
    
trade_file = f"{relative_path}trades/{strat}_trade.txt"

# close trade if exists
if os.path.isfile(trade_file):
    trade_wrapper.sell_trades(trade_file)
    exit(0)
    
# approx price to match
x = -0.001
call_price = math.floor((1-x)*long_price)
put_price = math.ceil((1+x)*short_price)

# currently doing 0DTE/1DTE based on time
day_offset = 3 if dt_now.weekday() == 4 else 1
#day_offset = 0 if dt_now.hour <= 13 else (3 if dt_now.weekday() == 4 else 1)
yymmdd = (dt_now+datetime.timedelta(days=day_offset)).strftime("%y%m%d")
for type in ["call","put"]:
    curr_price = str(globals()[f"{type}_price"])
    # SPY240222C00453000 format  
    format = "".join(["0" for _ in range(8-(len(curr_price)+3))])+f"{curr_price}"+"0"*3
    query_symbol = f"{globals()[type]}{yymmdd}{type[0].upper()}{format}"
    trade_wrapper.buy(trade_file,query_symbol,type)
    

