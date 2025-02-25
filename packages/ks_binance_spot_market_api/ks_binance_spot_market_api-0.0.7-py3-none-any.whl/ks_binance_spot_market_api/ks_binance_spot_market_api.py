from binance.spot import Spot
from binance.websocket.spot.websocket_stream import SpotWebsocketStreamClient
import json
from datetime import datetime, timedelta
from ks_trade_api.utility import extract_vt_symbol, generate_vt_symbol
from ks_trade_api.constant import (
    CHINA_TZ, US_EASTERN_TZ,
    Exchange as KsExchange, Product as KsProduct, SubscribeType as KsSubscribeType,
    RetCode as KsRetCode, RET_OK as KS_RET_OK, RET_ERROR as KS_RET_ERROR, ErrorCode as KsErrorCode,
    Currency as KsCurrency, Direction as KsDirection, Offset as KsOffset, Status as KsStatus,
    OrderType as ksOrderType, TimeInForce as KsTimeInForce, TradingHours as KsTradingHours,
    Product as ksProduct, Interval as KsInterval, Adjustment as KsAdjustment
)
from ks_trade_api.object import (
    ErrorData, ContractData, MyTickData, MyBookData, MyRawTickData, QuoteData, MyAccountData, MyOrderData, 
    MyTradeData, MyPositionData, BarData
)
# from ks_trade_api.base_trade_api import RateLimitChecker
from ks_utility import datetimes
from decimal import Decimal
from dateutil.parser import parse
from ks_trade_api.base_market_api import BaseMarketApi
from ks_trade_api.base_trade_api import BaseTradeApi
from ks_trade_api.constant import Environment
from ks_utility.numbers import to_decimal
from typing import Optional, Union, Tuple, List
from logging import DEBUG, INFO, WARNING, ERROR
import traceback
from time import sleep
import sys
import pydash
from pandas import DataFrame
import pandas as pd
from ks_coinmarketcap_api import KsCoinmarketcapAPI

RATES_INTERVAL: int = 60

class SubType():
    TICKER = 'TICKER'
    ORDER_BOOK = 'ORDER_BOOK'
    USER_DATA = 'USER_DATA'

class TrdSide():
    BUY = 'BUY'
    SELL = 'SELL'
    SELL_SHORT = 'SELL_SHORT'
    BUY_BACK = 'BUY_BACK'

class Action():
    SUBSCRIBE = SpotWebsocketStreamClient.ACTION_SUBSCRIBE
    UNSUBSCRIBE = SpotWebsocketStreamClient.ACTION_UNSUBSCRIBE

class EventType():
    OUTBOUND_ACCOUNT_POSITION = 'outboundAccountPosition'
    EXECUTION_REPORT = 'executionReport' # 现货的成交事件名称
    ORDER_TRADE_UPDATE = 'ORDER_TRADE_UPDATE' # 合约的成交时间名称

class ExecutionType():
    NEW = 'NEW'
    CANCELED  = 'CANCELED'
    REPLACED = 'REPLACED'
    REJECTED  = 'REJECTED'
    TRADE = 'TRADE'
    EXPIRED = 'EXPIRED'
    TRADE_PREVENTION  = 'TRADE_PREVENTION'

class OrderType():
    ABSOLUTE_LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    STOP = 'STOP'

class TimeInForce():
    GTC = 'GTC'
    IOC = 'IOC'
    FOK = 'FOK'

class NewOrderRespType():
    ACK = 'ACK'
    RESULT = 'RESULT'
    FULL = 'FULL'

INTERVAL_KS2MY = {
    KsInterval.MINUTE: '1m',
    KsInterval.HOUR: '1h',
    KsInterval.DAILY: '1d',
    KsInterval.WEEKLY: '1w'
}

TIF_KS2MY = {
    KsTimeInForce.GTD: TimeInForce.GTC,
    KsTimeInForce.IOC: TimeInForce.IOC,
    KsTimeInForce.FOK: TimeInForce.FOK
}

SUBTYPE_KS2MY = {
    KsSubscribeType.USER_ORDER: KsSubscribeType.USER_ORDER,
    KsSubscribeType.USER_TRADE: KsSubscribeType.USER_TRADE,
    KsSubscribeType.USER_POSITION: KsSubscribeType.USER_POSITION,
    KsSubscribeType.TRADE: SubType.TICKER,
    KsSubscribeType.BOOK: SubType.ORDER_BOOK
}

ORDERTYPE_KS2MY = { 
    ksOrderType.LIMIT: OrderType.ABSOLUTE_LIMIT,
    ksOrderType.MARKET: OrderType.MARKET
}

SIDE_KS2MY = {
    f'{KsDirection.LONG.value},{KsOffset.OPEN.value}': TrdSide.BUY,
    f'{KsDirection.SHORT.value},{KsOffset.CLOSE.value}': TrdSide.SELL,
    f'{KsDirection.SHORT.value},{KsOffset.CLOSETODAY.value}': TrdSide.SELL,
    f'{KsDirection.SHORT.value},{KsOffset.CLOSEYESTERDAY.value}': TrdSide.SELL,

    f'{KsDirection.SHORT.value},{KsOffset.OPEN.value}': TrdSide.SELL,
    f'{KsDirection.LONG.value},{KsOffset.CLOSE.value}': TrdSide.BUY,
    f'{KsDirection.LONG.value},{KsOffset.CLOSETODAY.value}': TrdSide.BUY,
    f'{KsDirection.LONG.value},{KsOffset.CLOSEYESTERDAY.value}': TrdSide.BUY,
}

def extract_my_symbol(my_symbol: str):
    return my_symbol, KsExchange.BINANCE

def symbol_my2ks(my_symbol: str):
    if not my_symbol:
        return ''
    return generate_vt_symbol(my_symbol, KsExchange.BINANCE)

def symbol_ks2my(vt_symbol: str):
    if not vt_symbol:
        return ''
    symbol, ks_exchange = extract_vt_symbol(vt_symbol)
    return symbol


def side_ks2my(direction: KsDirection, offset: KsOffset):
    key = f'{direction.value},{offset.value}'
    return SIDE_KS2MY.get(key)

# 定义一个自定义错误类
class MyError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
        # futu没有错误代码。。只能用文字先替代
        if '购买力不足' in message:
            self.code = KsErrorCode.BUY_POWER_EXCEEDED
        elif '频率太高' in message:
            self.code = KsErrorCode.RATE_LIMITS_EXCEEDED


class KsBinanceSpotMarketApi(BaseMarketApi):
    gateway_name: str = 'KS_BINANCE_SPOT'

    def __init__(self, setting: dict):
        self.api_key = setting.get('api_key')
        self.api_secret = setting.get('api_secret')
        self.is_test = Environment(setting.get('environment', 'REAL')) == Environment.TEST
        self.http_url = 'https://testnet.binance.vision' if self.is_test else 'https://api.binance.com'
        self.socket_url = 'wss://testnet.binance.vision' if self.is_test else 'wss://stream.binance.com:9443'
        gateway_name = setting.get('gateway_name', self.gateway_name)
        dd_secret = setting.get('dd_secret')
        dd_token = setting.get('dd_token')
        BaseMarketApi.__init__(self, gateway_name=gateway_name, dd_secret=dd_secret, dd_token=dd_token)
        
        self.sub_id: int = 0 # 订阅流的id，从0开始，依次递增
        self.sub_ids: dict = {} # 区分book和tick等的订阅id号

        if setting.get('coinmarketcap.access_token'):
            self.coinmarketcap_api = KsCoinmarketcapAPI(access_token=setting.get('coinmarketcap.access_token'))
        else:
            self.coinmarketcap_api = None

        self.init_handlers()


    # 初始化行回调和订单回调
    def init_handlers(self):
        self.http_client: Spot = Spot(self.api_key, self.api_secret, base_url=self.http_url)

        def on_message_book(_, message):
            # breakpoint()
            data = json.loads(message)
            if 'result' in data and data['result'] == None:
                return
            self.on_book(self.book_my2ks(data))
        
        # socket行情
        def on_message_trade(_, message):
            # breakpoint()
            data = json.loads(message)
            if 'result' in data and data['result'] == None:
                return
            self.on_tick(self.tick_my2ks(data))

        def on_message_userdata(_, message):
            # breakpoint()
            data = json.loads(message)
            
            if 'result' in data and data['result'] == None:
                return
            if data['e'] == EventType.EXECUTION_REPORT:
                if data['x'] == ExecutionType.TRADE:
                    self.on_deal({
                        'security_type': security_type,
                        'contract_type': contract_type,
                        'data': {
                            'code': data['s'],
                            'order_id': data['i'],
                            'price': Decimal(data['L']),
                            'qty': Decimal(data['l']),
                            'remark': data['c']
                        }
                    })
            elif data['e'] == EventType.ORDER_TRADE_UPDATE:
                if data['o']['x'] == ExecutionType.TRADE:
                    self.on_deal({
                        'security_type': security_type,
                        'contract_type': contract_type,
                        'data': {
                            'code': data['o']['s'],
                            'order_id': data['o']['i'],
                            'price': Decimal(data['o']['L']),
                            'qty': Decimal(data['o']['l']),
                            'remark': data['o']['c']
                        }
                    })
            self.log(data)

        self.socket_client_trade: SpotWebsocketStreamClient = SpotWebsocketStreamClient(on_message=on_message_trade)
        self.socket_client_book: SpotWebsocketStreamClient = SpotWebsocketStreamClient(on_message=on_message_book)
        # self.socket_client_userdata: SpotWebsocketStreamClient = SpotWebsocketStreamClient(on_message=on_message_userdata)
        

    # 由于现货的杠杆都在spotclient上，所以要用账号类型区分
    def get_sub_id(self, symbol, sub_type):
        id = f'symbol={symbol},sub_type={sub_type}'
        if self.sub_ids.get(id):
            return self.sub_ids.get(id)

        self.sub_id += 1
        self.sub_ids[id] = self.sub_id
        return self.sub_ids[id]
        

    # 订阅行情
    def subscribe(self, vt_symbols, vt_subtype_list, extended_time=True, action=Action.SUBSCRIBE) -> tuple[KsRetCode, Optional[ErrorData]]:
        if not vt_symbols:
            return KS_RET_OK, None
        
        if isinstance(vt_symbols, str):
            vt_symbols = [vt_symbols]

        my_symbols = [symbol_ks2my(x) for x in vt_symbols]
        my_subtype_list = [SUBTYPE_KS2MY.get(x) for x in vt_subtype_list]
        
        if KsSubscribeType.USER_ORDER in my_subtype_list:
            my_subtype_list.remove(KsSubscribeType.USER_ORDER)     

        if KsSubscribeType.USER_TRADE in my_subtype_list:
            my_subtype_list.remove(KsSubscribeType.USER_TRADE)
        

        # futu没有持仓回调
        if KsSubscribeType.USER_POSITION in my_subtype_list:
            my_subtype_list.remove(KsSubscribeType.USER_POSITION)

        # 剩下的是订阅行情
        if my_subtype_list:
            for symbol in my_symbols:
                # book
                if SubType.ORDER_BOOK in my_subtype_list:
                    sub_id = self.get_sub_id(symbol=symbol, sub_type=KsSubscribeType.BOOK)
                    self.socket_client_book.book_ticker(symbol, id=sub_id, action=action)
                    self.log({'sub_id': sub_id, 'symbol': symbol, 'sub_type': KsSubscribeType.BOOK }, tag='subscribe_book')
                # tick
                if SubType.TICKER in my_subtype_list:
                    sub_id = self.get_sub_id(symbol=symbol, sub_type=KsSubscribeType.TICK)
                    self.socket_client_trade.agg_trade(symbol, id=sub_id, action=action)
                    self.log({'sub_id': sub_id, 'symbol': symbol, 'sub_type': KsSubscribeType.TICK}, tag='subscribe_trade')
                sleep(0.5)

        return KS_RET_OK, None


    # 获取静态信息
    def query_contract(self, vt_symbol: str) -> tuple[KsRetCode, ContractData]:
        exchange_info = self.http_client.exchange_info()
        symbol, exchange = extract_vt_symbol(vt_symbol)

        lot_size = Decimal('0')
        min_notional = Decimal('0')
        pricetick = None
        target = pydash.find(exchange_info['symbols'], lambda x: x['symbol'] == symbol)
        if target:
            lot_filter = pydash.find(target['filters'], lambda x: x['filterType'] == 'LOT_SIZE')
            lot_size = to_decimal(lot_filter["minQty"]) if lot_filter else Decimal(0)

            notional_filter = pydash.find(target['filters'], lambda x: x['filterType'] == 'NOTIONAL')
            if notional_filter:
                min_notional = Decimal(notional_filter.get('minNotional') or '0')

            price_filter = pydash.find(target['filters'], lambda x: x['filterType'] == 'PRICE_FILTER')
            if price_filter:
                pricetick = Decimal(price_filter.get('tickSize') or '0')

        
        contract = ContractData(
            symbol=symbol,
            exchange=exchange,
            product=KsProduct.SPOT,
            size=Decimal('1'),
            min_volume=lot_size,
            min_notional=min_notional,
            pricetick=pricetick,
            name=symbol,
            gateway_name=self.gateway_name
        )

        return KS_RET_OK, contract
    
    # 获取静态信息 # todo! ks_trader_wrapper中使用到df=False要修正那边
    def query_contracts(
            self,
            vt_symbols: Optional[List[str]] = None,
            exchanges: Optional[list[KsExchange]] = None,
            products: Optional[List[KsProduct]] = None,
            df: bool = True
        ) -> tuple[KsRetCode, Union[list[ContractData], DataFrame]]:
        if vt_symbols:
            my_symbols = [symbol_ks2my(x) for x in vt_symbols]
            ret, data = self.quote_ctx.get_stock_basicinfo('US', code_list=my_symbols) # futu接口如果指定code_list，会忽略exchange
            if ret == RET_ERROR:
                error = self.get_error(vt_symbols, data, msg=data)
                return KS_RET_ERROR, error
        else:
            data = pd.DataFrame()
            # my_products = [PRODUCT_KS2MY.get(x) for x in products]
            # my_exchanges = [MARKET_KS2MY.get(x) for x in exchanges]
            exchange_info = self.http_client.exchange_info()
            data = pd.DataFrame(exchange_info['symbols'])
        
        if df:
            data['vt_symbol'] = [symbol_my2ks(x) for x in data['symbol']]
            data['product'] = ksProduct.SPOT.value
            data['size'] = '1'
            data['min_volume'] = data['filters'].transform(lambda x: pydash.find(x, lambda y: y['filterType'] == 'LOT_SIZE')['minQty'] or '0')
            # data['min_notional'] = data['filters'].transform(lambda x: pydash.find(x, lambda y: y['filterType'] == 'NOTIONAL')['minNotional'] or '0')
            data['pricetick'] = data['filters'].transform(lambda x: pydash.find(x, lambda y: y['filterType'] == 'PRICE_FILTER')['tickSize'] or '0')
            data['name'] = data['symbol']
            data['gateway'] = self.gateway_name
            return KS_RET_OK, data[['vt_symbol', 'product', 'size', 'min_volume', 'pricetick', 'name', 'gateway']]
        
        contracts: list[ContractData] = []
        for index, contract_data in data.iterrows():
            symbol, exchange = extract_my_symbol(contract_data.code)
            contract = ContractData(
                symbol=symbol,
                exchange=exchange,
                sub_exchange=contract_data.exchange_type,
                product=KsProduct.EQUITY,
                size=Decimal('1'),
                min_volume=Decimal(str(contract_data.lot_size)),
                # pricetick=Decimal('0.01'), # todo! 低价股是0.001这里以后要处理
                name=contract_data.get('name'),
                gateway_name=self.gateway_name
            )
            contract.exchange_type = contract_data.exchange_type
            contracts.append(contract)
        return KS_RET_OK, contracts
    
    # todo! ks_trader_rapper没有适配好
    def query_quotes_24hr(self, vt_symbols: list[str], df: bool = True) -> Union[KsRetCode, list[QuoteData]]:
        if not vt_symbols:
            return KsRetCode, []
        
        my_symbols = [symbol_ks2my(x) for x in vt_symbols]
        tickers = self.http_client.ticker_24hr(symbols=my_symbols)
        data = pd.DataFrame(tickers)
        tz = CHINA_TZ
        data['vt_symbol'] = [symbol_my2ks(x) for x in data['symbol']]
        data['datetime'] = pd.to_datetime(data['closeTime'], unit='ms').dt.tz_localize('UTC').dt.tz_convert(tz)
        data['volume'] = data['volume'].astype(str)
        data['turnover'] = data['quoteVolume'].astype(str)
        data['last_price'] = data['lastPrice'].astype(str)
        data['open_price'] = data['openPrice'].astype(str)
        data['high_price'] = data['highPrice'].astype(str)
        data['low_price'] = data['lowPrice'].astype(str)
        data['pre_close'] = data['prevClosePrice'].astype(str)
        return KS_RET_OK, data[['vt_symbol', 'datetime', 'volume', 'turnover', 'last_price', 'open_price', 'high_price', 'low_price', 'pre_close']]
    
    # todo! ks_trader_rapper没有适配好
    def query_quotes(self, vt_symbols: list[str], df: bool = True) -> Union[KsRetCode, list[QuoteData]]:
        if not vt_symbols:
            return KsRetCode, []
        
        my_symbols = [symbol_ks2my(x) for x in vt_symbols]
        all_df = pd.DataFrame()
        for i, my_symbol in enumerate(my_symbols):
            self.log(f'[{i}/{len(my_symbols)}]fetching {my_symbol}...')
            try:
                data_k = self.http_client.klines(symbol=my_symbol, interval='1d', limit=2)
                data_k = pd.DataFrame(data_k, columns=['ts_open', 'open', 'high', 'low', 'close', 'volume', 'ts_close', 'turnover', 'num', 'buy', 'sell', 'unkown'])
            except:
                return KS_RET_ERROR, self.get_error(symbol=my_symbol, interval='1d', limit=2)

            tz = CHINA_TZ
            data_k['symbol'] = my_symbols[i]
            data_k['vt_symbol'] = vt_symbols[i]
            data_k['datetime'] = pd.to_datetime(data_k.ts_close, unit='ms').dt.tz_localize('UTC').dt.tz_convert(tz)
            data_k['volume'] = data_k.volume
            data_k['turnover'] = data_k.turnover
            data_k['open_price'] = data_k.open
            data_k['high_price'] = data_k.high
            data_k['low_price'] = data_k.low
            data_k['last_price'] = data_k.close
            data_k['pre_close'] = data_k.close.shift()
            columns = ['vt_symbol', 'symbol', 'datetime', 'volume', 'turnover', 'open_price', 'high_price', 'low_price', 'last_price', 'pre_close']
            if len(data_k) > 1:
                data_k = data_k[columns][1:] # 最后一根是实时K线
            else:
                data_k = data_k[columns][0:]
            all_df = pd.concat([all_df, data_k], ignore_index=True)
        
        if self.coinmarketcap_api:
            data1 = self.coinmarketcap_api.listings_latest()
            data1 = data1['data']
            cap_df = pd.DataFrame([{
                'symbol': x['symbol'] + 'USDT',
                'circular_market_cap': x['quote']['USDT']['market_cap'],
                'total_market_cap': x['quote']['USDT']['fully_diluted_market_cap']
            } for x in data1])
            cap_df = cap_df[cap_df.circular_market_cap>0]
            all_df = all_df.merge(cap_df[['symbol', 'circular_market_cap', 'total_market_cap']], on='symbol', how='left')
            all_df.drop_duplicates(subset=['symbol'], keep='first', inplace=True) # 有些是重复数据
        else:
            all_df['circular_market_cap'] = ''
            all_df['total_market_cap'] = ''
        return KS_RET_OK, all_df[['vt_symbol', 'datetime', 'volume', 'turnover', 'last_price', 'open_price', 'high_price', 'low_price', 'pre_close', 'circular_market_cap', 'total_market_cap']]
    
    # todo 这里默认先不管是不是df都返回df，后续在处理非df 
    # n 最大1000
    def query_history_n(
            self,
            vt_symbol: str,
            n: int,
            interval: KsInterval,
            adjustment: KsAdjustment,
            df: bool = True
        ) -> tuple[KsRetCode, Union[list[BarData], DataFrame]]:
        """
        Query bar history data.
        """
        my_symbol = symbol_ks2my(vt_symbol)
        my_interval = INTERVAL_KS2MY.get(interval)
        try:
            data = self.http_client.klines(symbol=my_symbol, interval=my_interval, limit=n+1)
        except:
            return KS_RET_ERROR, self.get_error(symbol=my_symbol, interval=my_interval, limit=n+1)
        data_k = pd.DataFrame(data, columns=['ts_open', 'open', 'high', 'low', 'close', 'volume', 'ts_close', 'turnover', 'num', 'buy', 'sell', 'unkown'])

        
        tz = CHINA_TZ
        data_k['vt_symbol'] = vt_symbol
        data_k['datetime'] = pd.to_datetime(data_k.ts_close, unit='ms').dt.tz_localize('UTC').dt.tz_convert(tz)
        data_k['interval'] = interval.value
        data_k['volume'] = data_k.volume.astype(str)
        data_k['turnover'] = data_k.turnover.astype(str)
        data_k['open'] = data_k.open.astype(str)
        data_k['high'] = data_k.high.astype(str)
        data_k['low'] = data_k.low.astype(str)
        data_k['close'] = data_k.close.astype(str)
        return KS_RET_OK, data_k[['vt_symbol', 'datetime', 'interval', 'volume', 'turnover', 'open', 'high', 'low', 'close']][:-1] # 最后一根是实时K线
    
    def query_book(self, vt_symbol: str) -> tuple[KsRetCode,  MyBookData]:
        my_symbol = symbol_ks2my(vt_symbol)
        ret_sub, sub_data = self.quote_ctx.subscribe([my_symbol], [SubType.ORDER_BOOK], subscribe_push=False)
        # 先订阅买卖摆盘类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
        ret_code = RET_ERROR
        ret_data = None
        if ret_sub == RET_OK:  # 订阅成功
            ret, data = self.quote_ctx.get_order_book(my_symbol, num=5)  # 获取一次 3 档实时摆盘数据
            if ret == RET_OK:
                ret_code = KS_RET_OK
                ret_data = self.book_my2ks(data)
            else:
                ret_data = ret_data
        else:
            ret_data = sub_data
        return ret_code, ret_data
    
    def book_my2ks(self, data) -> MyBookData:
        book: MyBookData = MyBookData(
            symbol=data['s'],
            exchange=KsExchange.BINANCE,
            datetime=datetimes.now(),
            name=data['s'],
            bid_price_1=to_decimal(data['b']),
            bid_volume_1=to_decimal(data['B']),
            ask_price_1=to_decimal(data['a']),
            ask_volume_1=to_decimal(data['a']),
            gateway_name=self.gateway_name
        )
        return book
    
    def tick_my2ks(self, data) -> MyRawTickData:
        tick: MyRawTickData = MyRawTickData(
            symbol=data['s'],
            exchange=KsExchange.BINANCE,
            datetime=datetime.fromtimestamp(data['T']/1000).astimezone(CHINA_TZ),
            name=data['s'],
            volume=to_decimal(data['q']),
            last_price=to_decimal(data['p']),
            gateway_name=self.gateway_name
        )
        return tick
    
    def trade_my2ks(self, data) -> MyTradeData:
        trade: MyTradeData = MyTradeData(
            symbol=data['s'],
            exchange=KsExchange.BINANCE,
            datetime=datetime.fromtimestamp(data['T']/1000).astimezone(CHINA_TZ),
            name=data['s'],
            volume=to_decimal(data['q']),
            last_price=to_decimal(data['p']),
            gateway_name=self.gateway_name
        )
        return trade

        
    def query_ticks(self, vt_symbol: str, length: int = 1) -> Union[KsRetCode, list[MyRawTickData]]:
        if not vt_symbol:
            return KsRetCode, []
        
        my_symbol = symbol_ks2my(vt_symbol)
        ret_sub, data_sub = self.quote_ctx.subscribe([my_symbol], [SubType.TICKER], subscribe_push=False, extended_time=True)
        # 先订阅 K 线类型。订阅成功后 OpenD 将持续收到服务器的推送，False 代表暂时不需要推送给脚本
        if ret_sub == RET_OK:  # 订阅成功
            ret_quote, data_quote = self.quote_ctx.get_rt_ticker(my_symbol, length)  # 获取订阅股票报价的实时数据
            quotes: list[QuoteData] = []
            if ret_quote == RET_OK:
                for index, quote in data_quote.iterrows():
                    symbol, exchange = extract_my_symbol(quote.code)
                    tz = CHINA_TZ if exchange == KsExchange.SEHK else US_EASTERN_TZ
                    dt = tz.localize(parse(f'{quote.time}')).astimezone(CHINA_TZ)
                    quotes.append(MyRawTickData(
                        gateway_name=self.gateway_name,
                        symbol=symbol,
                        exchange=exchange,
                        datetime=dt,
                        volume=Decimal(str(quote.volume)),
                        last_price=Decimal(str(quote.price))
                    ))
                return KS_RET_OK, quotes
            else:
                return KS_RET_ERROR, self.get_error(vt_symbol=vt_symbol, msg=data_quote)
        else:
            return KS_RET_ERROR, self.get_error(vt_symbol=vt_symbol, msg=data_sub)


    # 关闭上下文连接
    def close(self):
        self.socket_client_book.stop()
        self.socket_client_trade.stop()
        # self.socket_client_userdata.stop()


        