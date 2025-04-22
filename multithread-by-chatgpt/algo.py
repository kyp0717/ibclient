# algo.py

import threading
import queue

from ib_worker import from_ib_queue, to_ib_queue
from ibapi.contract import Contract
from ibapi.order import Order


def trading_algo():
    print("[Algo] Starting algorithm...")

    # Create contract
    contract = Contract()
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"

    # Create market order
    order = Order()
    order.action = "BUY"
    order.orderType = "MKT"
    order.totalQuantity = 10

    # Send order
    to_ib_queue.put({"type": "place_order", "contract": contract, "order": order})

    # Wait for status
    while True:
        try:
            msg = from_ib_queue.get(timeout=5)
            if msg["type"] == "orderStatus":
                print(f"[Algo] Order {msg['orderId']} status: {msg['status']}")
                if msg["status"] in ("Filled", "Cancelled"):
                    break
        except queue.Empty:
            print("[Algo] Waiting for order status...")
            continue

    print("[Algo] Algorithm finished.")


def run_algo():
    thread = threading.Thread(target=trading_algo)
    thread.start()
