import subprocess,json,os,time
from alpaca.data.historical.option import OptionHistoricalDataClient
from alpaca.data.requests import OptionLatestQuoteRequest,OptionChainRequest
from alpaca.trading.requests import OrderRequest
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderType,OrderSide,TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest

key = "x"
secret = "x"
trader = TradingClient(key,secret,paper=True)

def get_capital():
    return 26_026

def get_price(ticker):
    """
    return most recent trade price
    """
    f = open(f"../prices/{ticker}_out.txt","r")
    ret = float(f.read())
    f.close()
    return ret

def sell_trades(trade_file, TRADE_QTY = 1):
    """
    delete trade_file (txt comma seperated), sell trade within file
    """
    trades = open(trade_file).read().split(",")
    for symbol in trades:
        trade(symbol,'sell',TRADE_QTY)
    subprocess.call(f"rm {trade_file}",shell = True)

def liquidate():
    """
    close all trades and cancel open orders
    """
    trader.close_all_positions(cancel_orders=True) 
    
def trade(symbol, direction, TRADE_QTY):
    """
    buy qty of symbol, direction = 'buy' or 'sell'
    """
    order_req = OrderRequest(symbol = symbol, qty = TRADE_QTY, side = OrderSide(direction),
                             type = OrderType('market'), time_in_force = TimeInForce('day'))
            
    trader.submit_order(order_req)
    
def buy(trade_file, query_symbol, type, TRADE_QTY = 1):
    """
    deprecated till options trading resumes, creates comma seperated trade
    """
    trade(query_symbol,'buy', TRADE_QTY)
    curr_file = open(trade_file,"a+")
    # write trade file ex - SPY240222C00453000, QQQ240222P00402000
    curr_file.write(f"{query_symbol}{',' if type == 'call' else ''}")
    
def get_quote_options(query_symbol):
    """
    get price for option
    """
    #create client
    client = OptionHistoricalDataClient(key, secret)
    req = OptionLatestQuoteRequest(symbol_or_symbols=query_symbol)
    quote = client.get_option_latest_quote(request_params = req)
    return quote

def cancel(order_id=None):
    if not order_id:
        trader.cancel_orders()
    else:
        trader.cancel_order_by_id(order_id)
        
def close_pair_position(trade_file):
    """
    delete trade file (json), close pair trade
    """
    json_in = json.loads(open(trade_file,"r").read())
    trade(json_in["long_symbol"],OrderSide('sell'),json_in["long_qty"])
    trade(json_in["short_symbol"],OrderSide('buy'),json_in["short_qty"])
    os.remove(trade_file)
    
def close_norm_position(trade_file):
    """
    delete trade file (json), close norm trade
    """
    json_in = json.loads(open(trade_file,"r").read())
    if json_in["direction"] == "sell":
        trade(json_in["stock_symbol"],OrderSide('buy'),json_in["stock_qty"])
    else:
        trade(json_in["stock_symbol"],OrderSide('sell'),json_in["stock_qty"])
    os.remove(trade_file)