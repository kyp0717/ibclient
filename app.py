import time
from threading import Thread

from ibclient import Algo, IBApp

port = 7500
clientId = 1001


## main app
def main():
    app = IBApp()
    algo = Algo(app)
    app.algo = algo

    app.connect("localhost", port, 1001)
    Thread(target=app.run).start()
    time.sleep(1)
    app.reqCurrentTime()
    app.reqMarketDataType(1)
    ## Start streaming market data
    app.reqMktData()


if __name__ == "__main__":
    main()
