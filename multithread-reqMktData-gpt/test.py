# market_data_app.py

import queue
import time
from threading import Event, Thread

from ibapi.client import EClient
from ibapi.contract import Contract
from ibapi.wrapper import EWrapper


# -- App class that handles IB API
class IBApp(EWrapper, EClient):
    def __init__(self, data_queue):
        EClient.__init__(self, self)
        self.data_queue = data_queue

    def tickPrice(self, reqId, tickType, price, attrib):
        self.data_queue.put((reqId, tickType, price))


# -- Contract helper
def create_stock_contract(symbol, exchange="SMART", currency="USD"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = exchange
    contract.currency = currency
    return contract


# -- Worker to send requests from a queue
def start_market_worker(app, request_queue, stop_event):
    def run():
        while not stop_event.is_set():
            try:
                req = request_queue.get(timeout=1)
                if req["type"] == "market_data":
                    app.reqMktData(
                        req["req_id"],
                        req["contract"],
                        "",  # genericTickList
                        False,  # snapshot
                        False,  # regulatorySnapshot
                        [],  # mktDataOptions
                    )
            except queue.Empty:
                continue

    thread = Thread(target=run, daemon=True)
    thread.start()
    return thread


# -- Main
if __name__ == "__main__":
    data_queue = queue.Queue()
    request_queue = queue.Queue()
    stop_event = Event()

    app = IBApp(data_queue)
    app.connect("127.0.0.1", 7500, clientId=123)
    app.reqMarketDataType(3)

    # Start the IB API loop in a thread
    api_thread = Thread(target=app.run, daemon=True)
    api_thread.start()

    # Wait a moment for connection to complete
    time.sleep(1)

    # Start the worker
    start_market_worker(app, request_queue, stop_event)

    # Send a market data request
    contract = create_stock_contract("AAPL")
    request_queue.put({"type": "market_data", "req_id": 1001, "contract": contract})

    # Collect and print a few ticks
    try:
        for _ in range(10):
            reqId, tickType, price = data_queue.get(timeout=5)
            print(f"[Tick] ReqId={reqId}, TickType={tickType}, Price={price}")
    except queue.Empty:
        print("No data received.")

    # Shutdown
    stop_event.set()
    app.disconnect()
