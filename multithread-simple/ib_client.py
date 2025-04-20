# ib_client.py

import queue

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

# use to pass msg btw algo module to IB App
algo_request = queue.Queue()

# messages coming from TWS (which is coming from remote server)
tws_response = queue.Queue()


class IBClient(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.order_id = None

    def nextValidId(self, orderId):
        print(f"[IB] Next valid order ID: {orderId}")
        self.order_id = orderId

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


def start_ib_client(app):
    app.run()
