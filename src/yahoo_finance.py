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
                if (
                    t.info["regularMarketPrice"] is None
                    or t.info["previousClose"] is None
                ):
                    return [0.0, 0.0]

                return [
                    float(t.info["regularMarketPrice"]),
                    float(t.info["previousClose"]),
                ]
            return [0.0, 0.0]

        except TypeError:
            return [0.0, 0.0]

    def get_nasdaq_future(self):
        try:
            t = yf.Ticker("NQ=F")
            if (
                t is not None
                and "regularMarketPrice" in t.info
                and "previousClose" in t.info
            ):
                if (
                    t.info["regularMarketPrice"] is None
                    or t.info["previousClose"] is None
                ):
                    return [0.0, 0.0]

                return [
                    float(t.info["regularMarketPrice"]),
                    float(t.info["previousClose"]),
                ]
            return [0.0, 0.0]

        except TypeError:
            return [0.0, 0.0]
