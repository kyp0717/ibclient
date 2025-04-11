import sys

from ibapi.client import EClient, OrderId
from ibapi.ticktype import TickTypeEnum
from ibapi.wrapper import ContractDetails, EWrapper, Order
from ibclient import Trade
from loguru import logger

# import logging
logger.remove()  # Remove the default
logger.add(sys.stderr, level="TRACE")


class IB(EWrapper, EClient):
    def __init__(self, trade: Trade):
        EClient.__init__(self, self)
        self.trade = trade

    def nextValidId(self, orderId: OrderId):
        logger.info(f"Initial OrderId from TWS: {orderId}")
        self.orderId = orderId

    def nextId(self) -> (ContractDetails, Order):
        self.orderId += 1
        self.contract = self.trade.define_contract()
        order = self.trade.define_order()
        self.reqContractDetails(self.orderId, ctx, order)

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
            self.algo.run(price)

    def tickSize(self, reqId, tickType, size):
        logger.error(f" --- ReqId: {reqId} --- ")
        logger.error(f"TickType: {TickTypeEnum.toStr(tickType)}, size: {size}")

    def enter_trade(self, last):
        sel

    def run(self, last_price):
        if self.algo.trade_active == False and self.algo.trade_complete == False:
            enter_trade()
            pass
