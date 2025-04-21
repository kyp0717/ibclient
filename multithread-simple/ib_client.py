# ib_client.py

import queue

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from loguru import logger

# use to pass msg btw algo module to IB App
algo_request = queue.Queue()

# messages coming from TWS (which is coming from remote server)
tws_response = queue.Queue()


class IBClient(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.order_id = None

    def nextValidId(self, orderId):
        logger.info(f"[IB] Next valid order ID: {orderId}")
        self.order_id = orderId

    def nextId(self):
        self.orderId += 1

    def error(self, reqId, errorCode, errorString, advanceOrderReject):
        logger.error(f" --- ReqId: {reqId} --- ")
        logger.error(f"ErrorCode: {errorCode}, ErrorString: {errorString}")
        logger.error(f"ErrorString: {errorString}")
        logger.error(f"Order Reject: {advanceOrderReject} ")

    def orderStatus(
        self,
        orderId,
        status,
        filled,
        remaining,
        avgFillPrice,
        permId,
        parentId,
        lastFillPrice,
        clientId,
        whyHeld,
        mktCapPrice,
    ):
        msg = {
            "type": "orderStatus",
            "orderId": orderId,
            "status": status,
            "filled": filled,
            "remaining": remaining,
            "avgFillPrice": avgFillPrice,
        }
        tws_response.put(msg)

    def execDetails(self, reqId, contract, execution):
        msg = {
            "type": "execution",
            "symbol": contract.symbol,
            "execId": execution.execId,
            "shares": execution.shares,
            "price": execution.price,
        }
        tws_response.put(msg)

    def tickPrice(self, reqId, tickType, price, attrib):
        msg = {
            "type": "tickPrice",
            "reqId": reqId,
            "tickType": tickType,
            "price": price,
            "attrib": attrib,
        }
        tws_response.put(msg)


def start_ib_client(app):
    app.run()
