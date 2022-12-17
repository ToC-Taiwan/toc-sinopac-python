import time

import yfinance as yf

from logger import logger


class Yahoo:
    def get_nasdaq(self):
        return self.get_price("^IXIC")

    def get_nasdaq_future(self):
        return self.get_price("NQ=F")

    def get_price(self, code: str):
        try:
            t = yf.Ticker(code)
            if (
                t is not None
                and "regularMarketPrice" in t.info
                and "previousClose" in t.info
            ):
                return [
                    float(t.info["regularMarketPrice"]),
                    float(t.info["previousClose"]),
                ]
            time.sleep(1)
            return self.get_price(code)

        except Exception as e:  # pylint: disable=broad-except
            logger.error("get price error: %s", type(e))
            time.sleep(1)
            return self.get_price(code)
