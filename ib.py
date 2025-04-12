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
        self.reqContractDetails(self.orderId, self.trade.contract)

    def error(self, reqId, errorCode, errorString, advanceOrderReject):
        logger.error(f" --- ReqId: {reqId} --- ")
        logger.error(f"ErrorCode: {errorCode}, ErrorString: {errorString}")
        logger.error(f"ErrorString: {errorString}")
        logger.error(f"Order Reject: {advanceOrderReject} ")

    def contractDetails(self, reqId: int, contractDetails: ibmsg.ContractDetails):
        self.trade.contractDetails = contractDetails

    def tickPrice(self, reqId, tickType, price, attrib):
        logger.info(f" --- ReqId: {reqId} --- ")
        logger.info(
            f"TickType: {TickTypeEnum.toStr(tickType)}, price: {price}, attrib: {attrib}"
        )
        # ask price
        if tickType == 2:
            # the trade has not begin, enter the position
            if self.trade.begin:
                enter = input(f" Last price is {price} - buy / sell")
                if enter == "b":
                    self.trade.define_order(self.orderId, action="BUY", lmtprice=price)
                    self.placeOrder(
                        self.orderId, self.trade.contractDetails, self.trade.order
                    )
        # bid price
        if tickType == 1:
            if self.trade.active:
                print(f"Current Bid Price - {price}")
                print(f"Entry Price - {self.trade.entry_price}")
                print
                pass

    def tickSize(self, reqId, tickType, size):
        logger.error(f" --- ReqId: {reqId} --- ")
        logger.error(f"TickType: {TickTypeEnum.toStr(tickType)}, size: {size}")

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

    def orderStatus(
        self,
        orderId: OrderId,
        status: str,
        filled: ibmsg.Decimal,
        remaining: ibmsg.Decimal,
        avgFillPrice: float,
        permId: int,
        parentId: int,
        lastFillPrice: float,
        clientId: int,
        whyHeld: str,
        mktCapPrice: float,
    ):
        logger.info(
            f"orderId: {orderId} - status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}"
        )
        logger.info(
            f"orderId: {orderId} - permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}"
        )
        logger.info(
            f"orderId: {orderId} -clientId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}"
        )

    def execDetails(
        self, reqId: int, contract: ibmsg.Contract, execution: ibmsg.Execution
    ):
        print(f"reqId: {reqId}, contract: {contract}, execution: {execution}")
