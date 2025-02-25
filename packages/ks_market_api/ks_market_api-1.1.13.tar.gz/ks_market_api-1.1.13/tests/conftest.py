# conftest.py
from logging import DEBUG, INFO, WARNING, ERROR
import pytest
import os
import asyncio


@pytest.fixture
def client(request, monkeypatch):
    # 设置环境变量 CONFIG 的值
    CONFIG_NAME = request.param['config_name']

    monkeypatch.setenv('CONFIG', CONFIG_NAME)
    assert(os.getenv('CONFIG') == CONFIG_NAME)

    from main import KsMarketEngine
    from ks_trade_api.utility import get_file_path, load_json

    gateway_config_name = 'gateway_config.json'
    gateway_config_path = get_file_path(gateway_config_name)
    config = load_json(gateway_config_path)
    setting = config['ks_market_api']['setting']
    KsMarketEngine(setting)

    class Client():
        async def async_sleep(self, seconds: int = 5, log: bool = True):
            count = seconds
            while count > 0:
                await asyncio.sleep(1)
                count -= 1
                log and self.log(f'--------async_sleep-------->: {count}')
    return Client()