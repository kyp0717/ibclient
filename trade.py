from dataclasses import dataclass
from enum import Enum

from ibapi.client import Contract, Order
from ibapi.wrapper import ContractDetails


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
        self.begin: bool = True
        self.active: bool = False
        self.end: bool = False
        self.entry_price: float = 0.0
        self.exit_price: float = 0.0
        self.priceChange = PriceChange()
        self.contract_buy = ContractDetails()
        self.contract_sell = ContractDetails()
        self.order = Order()
        self.orderId_buy = None
        self.orderId_sell = None
        self.lastprice: float = 0.0

        self.define_contract()

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
        self.contract = Contract()
        self.contract.symbol = self.symbol
        self.contract.secType = "STK"
        self.contract.currency = "USD"
        self.contract.exchange = "SMART"
        self.contract.primaryExchange = "NASDAQ"

    # order is define in the tickPrice function
    # price dependency
    def define_order(self, reqId: int, action: str, lmtprice: float) -> Order:
        self.order.symbol = self.symbol
        self.order.orderId = reqId
        self.order.action = action
        self.order.orderType = "LMT"
        self.order.lmtPrice = lmtprice
        self.order.totalQuantity = 100
