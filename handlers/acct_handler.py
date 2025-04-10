from loguru import logger


class AcctHandler:
    def __init__(self, app):
        self.app = app

    def updateAccountValue(self, key: str, val: str, currency: str, accountName: str):
        logger.info(f" --- UpdateAccountValue Callback {accountName} ---")
        logger.info(f" {key} : {val}, currency: {currency}")
