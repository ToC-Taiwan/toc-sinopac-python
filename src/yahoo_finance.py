import yfinance as yf


class Yahoo:
    def get_nasdaq(self):
        return self.get_price("^IXIC")

    def get_nasdaq_future(self):
        return self.get_price("NQ=F")

    def get_price(self, code: str):
        try:
            data = yf.Ticker(code)
            data_history = data.history(period="5d", interval="1d").loc[:, "Close"].to_dict().values()
            total = len(list(data_history))
            if total < 2:
                return [0.0, 0.0]
            return [list(data_history)[total - 1], list(data_history)[total - 2]]

        except Exception:
            # logger.error("yfinance error: %s", type(e).__name__)
            return [0.0, 0.0]
