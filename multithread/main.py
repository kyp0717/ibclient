# main.py

import time

from ib_worker import IBApp, start_ib_client, start_ib_worker

from algo import run_algo

# Instantiate app
app = IBApp()
app.connect("127.0.0.1", 7497, clientId=1)

# Start IB API client in background
import threading

threading.Thread(target=start_ib_client, args=(app,), daemon=True).start()

# Wait for next valid order ID
while app.order_id is None:
    time.sleep(0.1)

# Start IB worker loop
start_ib_worker(app)

# Start the trading algorithm
run_algo()

# Optionally keep main thread alive
while True:
    time.sleep(1)
