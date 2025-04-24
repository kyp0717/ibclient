# market_worker.py
import threading
from ibapi.contract import Contract
import time

def create_contract(symbol="AAPL", secType="STK", exchange="SMART", currency="USD"):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = secType
    contract.exchange = exchange
    contract.currency = currency
    return contract

def start_market_data_worker(app, request_queue, stop_event):
    def worker_loop():
        while not stop_event.is_set():
            try:
                req = request_queue.get(timeout=1)
                if req["type"] == "market_data":
                    contract = req["contract"]
                    req_id = req["req_id"]
                    app.reqMktData(req_id, contract, "", False, False, [])
            except Exception:
                continue
    thread = threading.Thread(target=worker_loop)
    thread.start()
    return thread
