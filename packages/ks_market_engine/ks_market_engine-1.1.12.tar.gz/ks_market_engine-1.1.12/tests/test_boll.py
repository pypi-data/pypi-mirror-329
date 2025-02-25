from decimal import Decimal
from datetime import datetime
import math

import pytest
import asyncio
from .config import CONFIGS

@pytest.mark.asyncio
@pytest.mark.parametrize("client", CONFIGS, indirect=True)
async def test_css(client):
    # res_cn = fundamental_api.css(
    #     vt_symbols=['600519.SSE', '000001.SZSE'],
    #     indicators='ROE,ROETTM,BPS,DIVIDENDYIELDY,LIBILITYTOASSET',
    #     options='ReportDate=MRQ,TradeDate=2024-12-05'
    # )
    from ks_trade_api.constant import SubscribeType, Indicator
    from api import ks_market_engine_api
    from ks_utility.zmqs import zmq
    
    def on_indicator(data):
        print(data)
    ks_market_engine_api.on_indicator = on_indicator

    import time
    time.sleep(3) # todo!!! 为什么需要这个睡眠时间呢？
    print('tttttttttttttttttttttttttt')
    ks_market_engine_api.subscribe(
        vt_symbols=['00700.SEHK', '09988.SEHK'],
        subscribe_types=[SubscribeType.K_DAILY, SubscribeType.K_MINUTE],
        indicators=[Indicator.BOLL]
    )
    
    await client.async_sleep(1000000, log=False)

