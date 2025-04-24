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


def enter_trade(t: Trade, client: IBClient):
    # check for existing marketdata stream
    if client.order_id in client.active_streams:
        client.cancel_market_data(client.order_id)
        logger.info("[Algo] Active Stream, cannot create another stream...")
        return None
    # Send request
    client.nextId()
    ctx = t.define_contract()
    ordfn = t.create_order_fn(reqId=client.order_id, action="BUY")

    client.reqMktData(client.order_id, ctx, "", False, False, [])

    # Wait for status
    while True:
        try:
            msg = tws_response.get(timeout=5)
            if msg["type"] == "tickPrice":
                logger.info(f"[Algo] ReqId - {msg['reqId']} ")
                logger.info(f"[Algo] {msg['price']} ")
                buy = input("Buy {t.symbol} at {msg['price'] (y/n)")
                if buy == "y":
                    ord = ordfn(msg["price"])
                    client.placeOrder(client.order_id, ctx, ord)
                    break
                else:
                    continue
        except queue.Empty:
            logger.info(f"[Algo] Waiting for market data for {t.symbol}...")
            continue


def check_order(t: Trade, client: IBClient):
    pass


def exit_trade(t: Trade, client: IBClient):
    pass
    # TODO - monitor price


def run(trade: Trade, client: IBClient):
    def algo():
        enter_trade(trade, client)

    thread = threading.Thread(target=algo, daemon=True)
    thread.start()
