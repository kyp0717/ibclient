import sys

import ibapi.wrapper as ibmsg
from ibapi.client import EClient, OrderId
from ibapi.ticktype import TickTypeEnum
from loguru import logger

from trade import Trade

# import logging
logger.remove()  # Remove the default
logger.add(sys.stderr, level="TRACE")


class IB(ibmsg.EWrapper, EClient):
    def __init__(self, tr: Trade):
        EClient.__init__(self, self)
        self.trade = tr

    def nextValidId(self, orderId: OrderId):
        logger.info(f"Initial OrderId from TWS: {orderId}")
        self.orderId = orderId

    def nextId(self):
        self.orderId += 1

    def enter_trade(self, action: str):
        self.nextId()
        self.trade.contract = self.trade.define_contract()
        logger.info(self.trade.contract)
        self.trade.fn_buy_order = self.trade.create_order_fn(
            self.orderId, action=action
        )
        self.reqMktData(self.orderId, self.trade.contract, "232", False, False, [])

    def exit_trade(self):
        self.nextId()
        self.trade.contract = self.trade.define_contract()
        logger.info(self.trade.contract)
        self.trade.fn_sell_order = self.trade.create_order_fn(
            self.orderId, action="SELL"
        )

    def error(self, reqId, errorCode, errorString, advanceOrderReject):
        logger.error(f" --- ReqId: {reqId} --- ")
        logger.error(f"ErrorCode: {errorCode}, ErrorString: {errorString}")
        logger.error(f"ErrorString: {errorString}")
        logger.error(f"Order Reject: {advanceOrderReject} ")

    def tickPrice(self, reqId, tickType, price, attrib):
        logger.info(f" --- ReqId {reqId} : [self.trade.symbol] --- ")
        logger.info(
            f"TickType: {TickTypeEnum.toStr(tickType)}, price: {price}, attrib: {attrib}"
        )
        orderstate = self.reqOpenOrders()
        logger.info(f"orderstate: {orderstate}")

        # delay ask price
        # if tickType == 2:
        if orderstate is None and tickType == 66:
            # the trade has not begin, enter the position
            # if self.trade.begin and self.trade.open_order:
            if not self.trade.active:
                enter = input(
                    f" {self.trade.symbol} : enter trade at {price} - buy? (y/n)"
                )
                if enter == "y":
                    order_fn = self.trade.fn_buy_order("price")
                    order = order_fn(lmtprice=price)
                    self.placeOrder(self.orderId, self.trade.contract, order)
                logger.info("order placed")
                logger.info(order)
                self.trade.active = True

    def openOrder(
        self,
        orderId: ibmsg.OrderId,
        contract: ibmsg.Contract,
        order: ibmsg.Order,
        orderState: ibmsg.OrderState,
    ):
        logger.info(
            f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}"
        )
        return orderState
