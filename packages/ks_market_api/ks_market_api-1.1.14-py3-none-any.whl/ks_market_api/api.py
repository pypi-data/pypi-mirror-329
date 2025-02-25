from ks_utility.zmqs import ZmqPublisher, ZmqSubscriber
from ks_trade_api.constant import SubscribeType, Indicator, Timing
from .config import GATEWAY_CONFIG
import json
import traceback

class KsMarketApi(ZmqPublisher, ZmqSubscriber):
    def __init__(self, setting: dict = {}):
        pub_address: str = setting.get('zmq', {}).get('pub_address')
        sub_address: str = setting.get('zmq', {}).get('sub_address')
        if not sub_address:
            sub_address = GATEWAY_CONFIG['ks_market_api']['setting']['zmq']['pub_address']
        if not pub_address:
            pub_address = GATEWAY_CONFIG['ks_market_api']['setting']['zmq']['sub_address']
        ZmqPublisher.__init__(self, pub_address)
        ZmqSubscriber.__init__(self, sub_address)

    def subscribe(
            self,
            vt_symbols: list[str] = [], 
            subscribe_types: list[SubscribeType] = [], 
            indicators: list[Indicator] = [],
            data_time_types: list[Timing] = []
        ):
        subscribe_types = [x.value for x in subscribe_types]
        indicators = [x.value for x in indicators]
        data_time_types = [x.value for x in data_time_types]
        self.send('subscribe', {'vt_symbols': vt_symbols, 'subscribe_types': subscribe_types, 'indicators': indicators, 'data_time_types': data_time_types})

    def on_indicator(self, indicator):
        pass

    def on_message(self, topic: str, msg: str):
        msg_data = json.loads(msg)
        try:
            getattr(self, topic)(msg_data)
        except:
            pass # todo 消息队列处理

if __name__ == '__main__':
    ks_market_api = KsMarketApi()
