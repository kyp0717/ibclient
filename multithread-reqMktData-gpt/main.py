# main.py
import queue
import threading

from ibapp import IBApp
from ibworker import create_contract, start_market_data_worker

if __name__ == "__main__":
    data_queue = queue.Queue()
    request_queue = queue.Queue()
    stop_event = threading.Event()

    # Instantiate and connect app
    app = IBApp(data_queue)
    app.connect("127.0.0.1", 7500, clientId=1001)
    app.reqMarketDataType(3)

    # Start IB API processing in background
    threading.Thread(target=app.run, daemon=True).start()

    # Start market data worker
    start_market_data_worker(app, request_queue, stop_event)

    # Request market data
    aapl_contract = create_contract("AAPL")
    request_queue.put(
        {"type": "market_data", "req_id": 1001, "contract": aapl_contract}
    )

    # Print 10 market data ticks
    for _ in range(10):
        reqId, tickType, price = data_queue.get()
        print(f"[tick] ReqID={reqId}, Type={tickType}, Price={price}")

    # Optional: shut everything down cleanly
    stop_event.set()
    app.disconnect()
