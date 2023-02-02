import yfinance as yf


class Yahoo:
    def get_nasdaq(self):
        return self.get_price("^IXIC")

    def get_nasdaq_future(self):
        return self.get_price("NQ=F")

    def get_price(self, code: str):
        try:
            tick = yf.Ticker(code)
            if tick is not None and "regularMarketPrice" in tick.info and "previousClose" in tick.info:
                return [
                    float(tick.info["regularMarketPrice"]),
                    float(tick.info["previousClose"]),
                ]
            return [0.0, 0.0]

        except Exception:
            # logger.error("yfinance error: %s", type(e).__name__)
            return [0.0, 0.0]
