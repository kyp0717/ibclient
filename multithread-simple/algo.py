# algo.py

import queue
import sys
import threading

from ib_client import algo_request, tws_response
from ibapi.contract import Contract
from ibapi.order import Order
from loguru import logger

# import logging
logger.remove()  # Remove the default
logger.add(sys.stderr, level="TRACE")


def trading_algo():
    logger.info("starting algorithm...")

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
    algo_request.put({"type": "place_order", "contract": contract, "order": order})

    # Wait for status
    while True:
        try:
            msg = tws_response.get(timeout=5)
            if msg["type"] == "orderStatus":
                logger.info(f"[Algo] Order {msg['orderId']} status: {msg['status']}")
                if msg["status"] in ("Filled", "Cancelled"):
                    break
        except queue.Empty:
            logger.info("[Algo] Waiting for order status...")
            continue

    logger.info("[Algo] Algorithm finished.")


def run_algo():
    thread = threading.Thread(target=trading_algo)
    thread.start()
