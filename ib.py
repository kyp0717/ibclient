import sys

from ibapi.client import EClient, OrderId
from ibapi.ticktype import TickTypeEnum
from ibapi.wrapper import ContractDetails, EWrapper
from loguru import logger

from trade import Trade

# import logging
logger.remove()  # Remove the default
logger.add(sys.stderr, level="TRACE")


class IB(EWrapper, EClient):
    def __init__(self, tr: Trade):
        EClient.__init__(self, self)
        self.trade = tr

    def nextValidId(self, orderId: OrderId):
        logger.info(f"Initial OrderId from TWS: {orderId}")
        self.orderId = orderId

    def nextId(self):
        self.orderId += 1
        self.trade.contract = self.trade.define_contract()
        self.trade.define_order(self.orderId, action="BUY", lmtprice=1.0)
        self.reqContractDetails(self.orderId, self.trade.contract)

    def error(self, reqId, errorCode, errorString, advanceOrderReject):
        logger.error(f" --- ReqId: {reqId} --- ")
        logger.error(f"ErrorCode: {errorCode}, ErrorString: {errorString}")
        logger.error(f"ErrorString: {errorString}")
        logger.error(f"Order Reject: {advanceOrderReject} ")

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        self.trade.contractDetails = contractDetails

    def tickPrice(self, reqId, tickType, price, attrib):
        logger.error(f" --- ReqId: {reqId} --- ")
        logger.error(
            f"TickType: {TickTypeEnum.toStr(tickType)}, price: {price}, attrib: {attrib}"
        )
        if tickType == 4:
            # the trade has not begin, enter the position
            if not self.trade.entry:
                enter = input(f" Last price is {price} - buy / sell")
                if enter == "b":
                    self.placeOrder()

    def tickSize(self, reqId, tickType, size):
        logger.error(f" --- ReqId: {reqId} --- ")
        logger.error(f"TickType: {TickTypeEnum.toStr(tickType)}, size: {size}")
