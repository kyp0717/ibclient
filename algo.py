import time
from threading import Thread

from ibclient import Trade, IB

port = 7500
clientId = 1001


class Algo:
    def __init__(self, ib: IB, trade: Trade):
        self.symbol = symbol
        self.trade = trade
        self.ib = ib 


    def enter_trade():
        if self.trade.complete == False:
            self.ib
            
        

    # def start_ib():
    #     self.ib = IB(self.trade)


## main app
def main():
    t = Trade('AAPL')
    ib = IB(t) 

    algo = 
    Thread(target=ib.run).start()
    ib.connect("localhost", port, 1001)
    ##
    
    ib.enter_trade()
    app.nextId()

    time.sleep(1)
    app.reqCurrentTime()
    app.reqMarketDataType(1)
    ## Start streaming market data
    app.reqMktData()


if __name__ == "__main__":
    main()
