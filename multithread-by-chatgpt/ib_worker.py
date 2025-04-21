# ib_worker.py

import queue
import threading

from ibapi.client import EClient
from ibapi.wrapper import EWrapper

to_ib_queue = queue.Queue()
from_ib_queue = queue.Queue()


class IBApp(EWrapper, EClient):
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
        from_ib_queue.put(msg)

    def execDetails(self, reqId, contract, execution):
        msg = {
            "type": "execution",
            "symbol": contract.symbol,
            "execId": execution.execId,
            "shares": execution.shares,
            "price": execution.price,
        }
        from_ib_queue.put(msg)


def start_ib_client(app):
    app.run()


def start_ib_worker(app):
    def ib_worker_loop():
        while True:
            try:
                command = to_ib_queue.get(timeout=1)
                if command["type"] == "place_order":
                    contract = command["contract"]
                    order = command["order"]
                    app.placeOrder(app.order_id, contract, order)
                    print(f"[Worker] Placed order ID: {app.order_id}")
                    app.order_id += 1
            except queue.Empty:
                continue

    thread = threading.Thread(target=ib_worker_loop, daemon=True)
    thread.start()
