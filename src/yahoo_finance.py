import yfinance as yf


class Yahoo:
    def get_nasdaq(self):
        try:
            t = yf.Ticker("^IXIC")
            if (
                t is not None
                and "regularMarketPrice" in t.info
                and "previousClose" in t.info
            ):
                return [
                    float(t.info["regularMarketPrice"]),
                    float(t.info["previousClose"]),
                ]
        except KeyError:
            return [0.0, 0.0]

    def get_nasdaq_future(self):
        try:
            t = yf.Ticker("NQ=F")
            if (
                t is not None
                and "regularMarketPrice" in t.info
                and "previousClose" in t.info
            ):
                return [
                    float(t.info["regularMarketPrice"]),
                    float(t.info["previousClose"]),
                ]
        except KeyError:
            return [0.0, 0.0]
