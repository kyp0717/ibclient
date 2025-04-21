# algo.py

import queue
import sys
import threading

from ib_client import algo_request, tws_response
from loguru import logger

from trade import Trade

# import logging
logger.remove()  # Remove the default
logger.add(sys.stderr, level="TRACE")


def req_price(t: Trade):
    # Send request

    c = t.define_contract()
    algo_request.put({"type": "req_ask", "contract": c})

    # Wait for status
    while True:
        try:
            msg = tws_response.get(timeout=5)
            if msg["type"] == "orderStatus":
                logger.info(f"[Algo] Order {msg['orderId']} status: {msg['status']}")
                if msg["status"] in ("Filled"):
                    logger.info(f"[Algo] Order {msg['orderId']} -- Filled")
                    logger.info(
                        f"[Algo] Order {msg['orderId']} status: {msg['status']}"
                    )
                    break
                if msg["status"] in ("Cancelled"):
                    # TODO - exit the trade
                    break
        except queue.Empty:
            logger.info("[Algo] Waiting for order status...")
            continue


def enter_trade(t: Trade):
    c = t.define_contract()
    o = t.create_order_fn()
    # Send order
    algo_request.put({"type": "place_order", "contract": c, "order": o})

    # Wait for status
    while True:
        try:
            msg = tws_response.get(timeout=5)
            if msg["type"] == "orderStatus":
                logger.info(f"[Algo] Order {msg['orderId']} status: {msg['status']}")
                if msg["status"] in ("Filled"):
                    logger.info(f"[Algo] Order {msg['orderId']} -- Filled")
                    logger.info(
                        f"[Algo] Order {msg['orderId']} status: {msg['status']}"
                    )
                    break
                if msg["status"] in ("Cancelled"):
                    # TODO - exit the trade
                    break
        except queue.Empty:
            logger.info("[Algo] Waiting for order status...")
            continue


def algo(t: Trade):
    logger.info("Starting algorithm...")

    logger.info("Entering trade...")
    enter_trade(t)

    logger.info("[Algo] Algorithm finished.")


def run_algo():
    thread = threading.Thread(target=trading_algo)
    thread.start()
