# main.py

import sys
import threading
import time

from ib_client import IBClient, start_ib_client

# from ib_worker import start_ib_worker
from loguru import logger

import algo
from trade import Trade

# import logging
logger.remove()  # Remove the default
# logger.add(sys.stderr, level="TRACE", format="{time} | {level} | {message}")
logger.add(sys.stderr, level="TRACE")

# define the asset to trade
t = Trade("AAPL")


# Instantiate app
# this must be done first to create queue to be imported
logger.info("IB client instantiated")
client = IBClient()
client.connect("127.0.0.1", 7500, clientId=1001)

## delay market data
client.reqMarketDataType(3)
# Start IB API client in background

logger.info("Starting ib client thread")
threading.Thread(target=start_ib_client, args=(client,), daemon=True).start()

# Wait for next valid order ID
while client.order_id is None:
    time.sleep(0.1)

# Start IB worker loop in a thread
# logger.info("Starting ib worker thread")
# start_ib_worker(client)

# Start the trading algorithm in a thread
logger.info("Starting algo thread")
algo.start(t, client)

# Optionally keep main thread alive
while True:
    try:
        print("Running... Press Ctrl+C to exit")
        time.sleep(1)
        continue

    except KeyboardInterrupt:
        print("\nDisconnecting from TWS...")
        client.disconnect()
        print("IB Client has disconnected. Exiting.")
        break

s = input("Shutdown Algo? (y/n)")
if s == "y":
    sys.exit(0)
