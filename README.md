# Public version of algorithm development
My anti-microservice behemoth. I developed this in 2024, wanting a simple and clean mean reversion algorithm.


launcher starts (price_stream, pair_data_loaders)
    price stream updates prices with each trade

    data_loader fetches prices every 10 seconds and calculates divergence
    data_loader calls pair_trader
        trader checks if divergence is high enough for a trade
        trader closes trades if window runs out or P/L is reached
        trader calls stock_trade
            stock_trade shorts and longs the stocks
            stock_trade creates trade files under /trades
