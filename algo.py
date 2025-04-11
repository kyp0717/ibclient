from dataclasses import dataclass
from enum import Enum

from ibapi.client import Contract, Order

from ibclient import IBApp


class TradeSignal(Enum):
    BUY = 1
    SELL = 2
    HOLD = 3


@dataclass
class PriceChange:
    val: float = 0.0
    cct: float = 0.0


class Algo:
    def __init__(self, ib: IBApp):
        self.ib = ib
        self.symbol: str = None
        self.size: int = 0
        self.position: int = 0
        self.stoploss: float = 0.0
        self.trade_entry: float = 0.0
        self.trade_exit: float = 0.0
        self.trade_complete: bool = False
        self.priceChange = PriceChange()
        self.contract = Contract()
        self.order = Order()

    def price_change(self, last) -> PriceChange:
        v1 = self.trade_entry - self.last
        v2 = v1 / last * 100
        self.priceChange.val = v1
        self.priceChange.pct = v2

    def define_contract(self):
        self.contract.symbol = self.symbol
        self.contract.secType = "STK"
        self.contract.currency = "USD"
        self.contract.exchange = "SMART"
        self.contract.primaryExchange = "NASDAQ"

    def define_order(self):
        self.contract.symbol = self.symbol
        self.contract.secType = "STK"
        self.contract.currency = "USD"
        self.contract.exchange = "SMART"
        self.contract.primaryExchange = "NASDAQ"

    def enter_trade(self, last):
        self.define_contract()
        self.define_order()

        if self.trade_complete == False and self.position == 0:
            self.ib.placeOrder

    def track(self, last_price):
        pass
