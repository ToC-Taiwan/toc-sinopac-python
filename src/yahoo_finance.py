import yfinance as yf


class Yahoo:
    def get_nasdaq(self):
        try:
            t = yf.Ticker("^IXIC")
            return [float(t.info["regularMarketPrice"]), float(t.info["previousClose"])]
        except KeyError:
            return [0, 0]

    def get_nasdaq_future(self):
        try:
            t = yf.Ticker("NQ=F")
            return [float(t.info["regularMarketPrice"]), float(t.info["previousClose"])]
        except KeyError:
            return [0, 0]
