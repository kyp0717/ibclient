import time
from threading import Thread

from ib import IB
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
    ib.nextId()

    # ib.reqMarketDataType(1)
    ## 3 is delay marketdata
    ib.reqMarketDataType(3)
    ## Start streaming market data
    ib.reqMktData()


if __name__ == "__main__":
    main()
