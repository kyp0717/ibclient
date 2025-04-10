import sys

from ibapi.client import EClient, OrderId
from ibapi.ticktype import TickTypeEnum
from ibapi.wrapper import EWrapper
from loguru import logger

# import logging
logger.remove()  # Remove the default
logger.add(sys.stderr, level="TRACE")


class IBApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: OrderId):
        logger.info(f"Initial OrderId from TWS: {orderId}")
        self.orderId = orderId

    def nextId(self):
        self.orderId += 1

    def error(self, reqId, errorCode, errorString, advanceOrderReject):
        logger.error(f" --- ReqId: {reqId} --- ")
        logger.error(f"ErrorCode: {errorCode}, ErrorString: {errorString}")
        logger.error(f"ErrorString: {errorString}")
        logger.error(f"Order Reject: {advanceOrderReject} ")

    def tickPrice(self, reqId, tickType, price, attrib):
        logger.error(f" --- ReqId: {reqId} --- ")
        logger.error(
            f"TickType: {TickTypeEnum.toStr(tickType)}, price: {price}, attrib: {attrib}"
        )
        if tickType == 4:
            self.algo.run(price)

    def tickSize(self, reqId, tickType, size):
        logger.error(f" --- ReqId: {reqId} --- ")
        logger.error(f"TickType: {TickTypeEnum.toStr(tickType)}, size: {size}")
