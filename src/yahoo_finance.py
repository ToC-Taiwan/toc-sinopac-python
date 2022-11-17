import yfinance as yf


class Yahoo:
    def get_nasdaq(self):
        t = yf.Ticker("^IXIC")
        return float(t.info["regularMarketPrice"])

    def get_nasdaq_future(self):
        t = yf.Ticker("NQ=F")
        return float(t.info["regularMarketPrice"])
