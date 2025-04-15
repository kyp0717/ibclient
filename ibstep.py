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
        # c = self.trade.define_contract()
        # print(c)

        # self.trade.contract_buy = self.reqContractDetails(self.orderId, c)
        # d = self.reqContractDetails(self.orderId, c)
        # print(d)

    def nextId(self):
        self.orderId += 1
        self.trade.contract = self.trade.define_contract()
        logger.info(self.trade.contract)

    def error(self, reqId, errorCode, errorString, advanceOrderReject):
        logger.error(f" --- ReqId: {reqId} --- ")
        logger.error(f"ErrorCode: {errorCode}, ErrorString: {errorString}")
        logger.error(f"ErrorString: {errorString}")
        logger.error(f"Order Reject: {advanceOrderReject} ")

    def tickPrice(self, reqId, tickType, price, attrib):
        logger.info(f" --- ReqId: {reqId} --- ")
        logger.info(
            f"TickType: {TickTypeEnum.toStr(tickType)}, price: {price}, attrib: {attrib}"
        )
        self.trade.order = self.trade.define_order(
            reqId=self.orderId, action="BUY", lmtprice=price
        )
        logger.info(self.trade.order)
