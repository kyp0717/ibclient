# ib_app.py
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

class IBApp(EWrapper, EClient):
    def __init__(self, data_queue):
        EClient.__init__(self, self)
        self.data_queue = data_queue

    def tickPrice(self, reqId, tickType, price, attrib):
        self.data_queue.put((reqId, tickType, price))
