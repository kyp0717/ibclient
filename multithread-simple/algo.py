# algo.py

import queue
import sys
import threading

from ib_client import IBClient, tws_response
from loguru import logger

from trade import Trade

# import logging
logger.remove()  # Remove the default
logger.add(sys.stderr, level="TRACE")


def req_price(t: Trade, client: IBClient):
    # Send request
    client.nextId()
    c = t.define_contract()
    client.reqMktData(client.order_id, c, "232", False, False, [])

    # Wait for status
    while True:
        try:
            msg = tws_response.get(timeout=5)
            if msg["type"] == "tickPrice":
                logger.info(f"[Algo] {msg['d']} status: {msg['status']}")
                # TODO - exit the trade
                break
        except queue.Empty:
            logger.info(f"[Algo] Waiting for market data for {t.symbol}...")
            continue


def start(trade, client):
    def algo():
        req_price(trade, client)

    thread = threading.Thread(target=algo, daemon=True)
    thread.start()
