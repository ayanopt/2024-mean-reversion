from alpaca.data.live.stock import StockDataStream
import asyncio,sys,time,datetime
from trade_operations.trade_wrapper import key,secret

def write_price(data):
    tmp = dict(data)
    f = open(f"./prices/{tmp['symbol']}_out.txt","w+")
    f.write(str(tmp["price"]))
    f.close()
    
async def load_price(data):
    write_price(data)
    now = datetime.datetime.now()
    if now.hour == 15 and now.minute >= 45:
        await stream.stop_ws()

stream = StockDataStream(api_key=key,secret_key=secret)
stream.subscribe_trades(load_price,*sys.argv[1:])
stream.run()
