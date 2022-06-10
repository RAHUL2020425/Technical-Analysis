from kiteconnect import KiteTicker,KiteConnect
import pandas as pd
# from py_mysql import *
from datetime import datetime, timedelta
import talib

if __name__ == '__main__':
    api_key=open('api_key.txt','r').read()
    api_secret = open('api_secret.txt','r').read()

    kite = KiteConnect(api_key=api_key)

    access_token = open('access_token.txt', 'r').read()

    kite.set_access_token(access_token)

    # print(kite.login_url())
    # data = kite.generate_session("mXUDbNDFq4QLk9jYxC0DzvB3tU8RL6bO", api_secret=api_secret)
    # print(data['access_token'])
    # kite.set_access_token(data['access_token'])
    # with open('access_token.txt', 'w') as ak:
    #     ak.write(data['access_token'])



    # # Dates between which we need historical data
    from_date = datetime.strftime(datetime.now() - timedelta(100), '%Y-%m-%d')
    to_date = datetime.today().strftime('%Y-%m-%d')

    # Interval(minute, day, 3 minute, 5 minute...)
    interval = "5minute"
    current_signal = ''
    tokens = {738561: 'RELIANCE', 341249: 'HDFCBANK'}
    # kws=KiteTicker(api_key,data['access_token'])

    # while True:
        # if (datetime.now().second == 0) and ((datetime.now().minute) % 5 == 0):
    for token in tokens:
        records = kite.historical_data(token,from_date=from_date,to_date=to_date,interval=interval)
        df = pd.DataFrame(records)
        df.drop(df.tail(1).index, inplace=True)
        # print(df)
        open = df['open'].values
        high = df['high'].values
        low = df['low'].values
        close = df['close'].values
        volume = df['volume'].values

        sma5 = talib.SMA(close,5)
        sma20 = talib.SMA(close,20)
        print(sma5[-1])
        print(sma20[-1])

        # order_id = kite.place_order(tradingsymbol=tokens[token],
        #                             variety= kite.VARIETY_REGULAR,
        #                             exchange=kite.EXCHANGE_NSE,
        #                             transaction_type=kite.TRANSACTION_TYPE_BUY,
        #                             quantity=1,
        #                             order_type=kite.ORDER_TYPE_MARKET,
        #                             product=kite.PRODUCT_MIS)
        #bracket order
        price = kite.ltp('NSE:'+ tokens[token])
        print(price)
        ltp = price['NSE:'+ tokens[token]]['last_price']
        print(ltp)
        # kite.place_order(
        #     variety=kite.VARIETY_BO,
        #     exchange=kite.EXCHANGE_NSE,
        #     order_type=kite.ORDER_TYPE_LIMIT,
        #     tradingsymbol=tokens[token],
        #     transaction_type=kite.TRANSACTION_TYPE_BUY,
        #     quantity=1,
        #     price=ltp,
        #     squareoff=10,
        #     stoploss=2,
        #     trailing_stoploss=1,
        #     validity=kite.VALIDITY_DAY,
        #     product=kite.PRODUCT_MIS)

        # print(kite.orders())
        # print(kite.ltp('NSE:RELIANCE'))

                # if (sma5[-2] < sma20[-2]) and (sma5[-1] > sma20[-1]):
                #     buy_order_id = kite.place_order(tradingsymbol=tokens[token], exchange="NSE", quantity=1,transaction_type="BUY", order_type="MARKET", product="CNC")
                #     # current_signal = 'buy'
                #
                # if (sma5[-2] > sma20[-2]) and (sma5[-1] < sma20[-1]):
                #     sell_order_id = kite.place_order(tradingsymbol=tokens[token], exchange="NSE", quantity=1,transaction_type="SELL", order_type="MARKET", product="CNC")
                #     # current_signal = 'sell'


        # def on_ticks(ws,ticks):
        #     insert_tick=insert_ticks(ticks)
        #     # print(ticks)
        #
        # def on_connect(ws,response):
        #     ws.subscribe(tokens)
        #     ws.set_mode(ws.MODE_FULL,tokens)
        #
        # kws.on_ticks=on_ticks
        # kws.on_connect=on_connect
        # kws.connect()