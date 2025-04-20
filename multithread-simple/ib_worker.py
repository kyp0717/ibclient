# ib_worker.py

import queue
import threading

from ib_client import algo_request
from loguru import logger


def start_ib_worker(app):
    def ib_worker_loop():
        while True:
            try:
                command = algo_request.get(timeout=1)
                if command["type"] == "place_order":
                    contract = command["contract"]
                    order = command["order"]
                    app.placeOrder(app.order_id, contract, order)
                    logger.info(f"[Worker] Placed order ID: {app.order_id}")
                    app.order_id += 1
            except queue.Empty:
                continue

    thread = threading.Thread(target=ib_worker_loop, daemon=True)
    thread.start()
