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

    def enter_trade(self):
        self.nextId()
        self.trade.contract = self.trade.define_contract()
        logger.info(self.trade.contract)
        self.reqMktData(self.orderId, self.trade.contract, "232", False, False, [])

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
        # ask price
        if tickType == 66:
            # the trade has not begin, enter the position
            if self.trade.begin:
                enter = input(
                    f" {self.trade.symbol} : enter trade at {price} - buy? (y/n)"
                )
                if enter == "y":
                    order = self.trade.create_order(
                        self.orderId, action="BUY", lmtprice=price
                    )
                    # self.placeOrder(self.orderId, self.trade.contract, order)
                logger.info("order placed")
                logger.info(order)
                self.trade.begin = False
