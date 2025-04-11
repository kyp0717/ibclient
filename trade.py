from dataclasses import dataclass
from enum import Enum

from ibapi.client import Contract, Order


class TradeSignal(Enum):
    BUY = 1
    SELL = 2
    HOLD = 3


@dataclass
class PriceChange:
    val: float = 0.0
    cct: float = 0.0


class Trade:
    def __init__(self, symbol):
        self.symbol: str = symbol
        self.size: int = 0
        self.position: int = 0
        self.stoploss: float = 0.0
        self.entry: bool = False
        self.entry_price: float = 0.0
        self.exit_price: float = 0.0
        self.active: bool = False
        self.end: bool = False
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

    def define_order(self, reqId: int, lmtprice: float):
        self.order.symbol = self.symbol
        self.order.orderId = reqId
        self.order.action = "BUY"
        self.order.orderType = "LMT"
        self.order.lmtPrice = lmtprice
        self.order.totalQuantity = 100
