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

    Thread(target=ib.run).start()
    ib.connect("localhost", port, 1001)
    ##
    time.sleep(1)
    ib.reqCurrentTime()
    ib.reqMarketDataType(1)
    ## Start streaming market data
    ib.reqMktData()


if __name__ == "__main__":
    main()
