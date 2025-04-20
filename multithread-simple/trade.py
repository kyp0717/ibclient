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


@dataclass
class TrackId:
    buy: int = None
    sell: int = None
    reqMktData: int = None


class Trade:
    def __init__(self, symbol):
        self.symbol: str = symbol
        self.size: int = 0
        self.position: int = 0
        self.stoploss: float = 0.0
        self.begin: bool = True
        self.active: bool = False
        self.end: bool = False
        self.entry_price: float = 0.0
        self.exit_price: float = 0.0
        self.priceChange = PriceChange()
        self.fn_buy_order = None
        self.fn_sell_order = None
        self.lastprice: float = 0.0
        self.contract = None

    def price_change(self, last) -> PriceChange:
        v1 = self.trade_entry - self.last
        v2 = v1 / last * 100
        self.priceChange.val = v1
        self.priceChange.pct = v2

    def price_change_pct(self, price) -> float:
        v1 = self.trade_entry - self.last
        v2 = v1 / price * 100
        return v2

    def define_contract(self) -> Contract:
        contract = Contract()
        contract.symbol = self.symbol
        contract.secType = "STK"
        contract.currency = "USD"
        contract.exchange = "SMART"
        contract.primaryExchange = "NASDAQ"
        return contract

    # order is define in the tickPrice function
    # price dependency
    def create_order_fn(self, reqId: int, action: str):
        order = Order()

        def create_order(lmtprice: float):
            order.symbol = self.symbol
            order.orderId = reqId
            order.action = action
            order.orderType = "LMT"
            order.lmtPrice = lmtprice
            order.totalQuantity = 100
            return order

        return create_order
