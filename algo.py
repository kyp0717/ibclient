import time
from threading import Thread

from ibstep import IB
from trade import Trade

port = 7500
clientId = 1001


## main app
def main():
    t = Trade("AAPL")
    ib = IB(t)

    ib.connect("localhost", port, 1001)
    Thread(target=ib.run).start()
    ##
    time.sleep(1)
    # 3 is delay marketdata
    # ib.reqMarketDataType(1)
    ib.reqMarketDataType(3)
    ib.enter_trade(action="BUY")

    try:
        print("Running... Press Ctrl+C to exit")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nDisconnecting from TWS...")
        ib.disconnect()
        print("Disconnected. Exiting.")


if __name__ == "__main__":
    main()
