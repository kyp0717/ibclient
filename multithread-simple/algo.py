# algo.py
import datetime
import queue
import sys

from ib_client import IBClient, qu_ask, qu_bid, qu_ctx, qu_orderstatus, qu_pnl
from loguru import logger

from trade import Trade

# import logging
logger.remove()  # Remove the default
logger.add(sys.stderr, level="TRACE")


def enter_trade(t: Trade, client: IBClient):
    # check for existing marketdata stream
    # if client.order_id in client.active_streams:
    #     client.cancel_market_data(client.order_id)
    #     logger.info("[Algo] Active Stream, cannot create another stream...")
    #     return None
    # Send request
    client.nextId()
    ctx = t.define_contract()
    # Wait for status
    while True:
        client.reqContractDetails(client.order_id, contract=ctx)
        try:
            msg = qu_ctx.get(timeout=5)
            logger.info(f"[Algo] ReqId {msg['reqId']} - Getting Contract Detail")
            t.conid = msg["conId"]
            logger.info(
                f"[Algo] ReqId {msg['reqId']} - ConId for {t.symbol} - {msg['conId']}"
            )
            break
        except queue.Empty:
            logger.info(f"[Algo] Getting Contract ID for {t.symbol}...")
            continue

    client.nextId()
    ordfn = t.create_order_fn(reqId=client.order_id, action="BUY")
    client.reqMktData(client.order_id, ctx, "", False, False, [])

    # Wait for status
    while True:
        # client.clear_queue(qu_ask)
        try:
            msg = qu_ask.get(timeout=5)
            time_diff = datetime.datetime.now() - msg["time"]
            if time_diff.total_seconds() > 4:
                continue
            logger.info(f"[Algo] ReqId {msg['reqId']} - Ask {msg['price']}")
            buy = input(f"Buy {t.symbol} at {msg['price']} (y/n)")
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
    while True:
        try:
            msg = qu_orderstatus.get(timeout=5)
            logger.info(f"[Algo] OrderId {msg['orderId']} - Order Status ")
            logger.info(f"[Algo] Order Status - {msg['status']} ")
            if msg["status"] == "Filled":
                # logger.info(f"[Algo] Order Status - {msg['status']} ")
                break
            else:
                continue
        except queue.Empty:
            logger.info(f"[Algo] Waiting to fill order for {t.symbol}...")
            continue


def get_pnl(t: Trade, client: IBClient):
    client.reqPnL()
    try:
        msg = qu_pnl.get(timeout=5)
        logger.info(f"[Algo] OrderId {msg['orderId']} - Order Status ")
            break
        else:
            continue
    except queue.Empty:
        logger.info(f"[Algo] Waiting PNL for {t.symbol}...")
        continue


def exit_trade(t: Trade, client: IBClient):
    # Send request
    client.nextId()
    ctx = t.define_contract()
    ordfn = t.create_order_fn(reqId=client.order_id, action="SELL")

    # Wait for status
    while True:
        try:
            msg = qu_bid.get(timeout=5)
            time_diff = datetime.datetime.now() - msg["time"]
            if time_diff.total_seconds() > 4:
                continue
            # TODO - check correct tick type (looking for bid price)
            logger.info(f"[Algo] ReqId {msg['reqId']} - Bid {msg['price']} ")
            buy = input(f"Sell {t.symbol} at {msg['price']} (y/n)")
            if buy == "y":
                ord = ordfn(msg["price"])
                client.placeOrder(client.order_id, ctx, ord)
                break
            else:
                continue
        except queue.Empty:
            logger.info(f"[Algo] Waiting for bid price on {t.symbol}...")
            continue
