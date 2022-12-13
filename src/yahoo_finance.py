from http.client import IncompleteRead, RemoteDisconnected
from json import JSONDecodeError

import yfinance as yf
from requests.exceptions import ChunkedEncodingError as RequestsChunkedEncodingError
from requests.exceptions import ConnectionError as RequestsConnectionError
from urllib3.exceptions import ProtocolError


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
            return self.get_price(code)

        except JSONDecodeError:
            return self.get_price(code)
        except TypeError:
            return self.get_price(code)
        except RemoteDisconnected:
            return self.get_price(code)
        except ConnectionResetError:
            return self.get_price(code)
        except ProtocolError:
            return self.get_price(code)
        except RequestsConnectionError:
            return self.get_price(code)
        except KeyError:
            return self.get_price(code)
        except IncompleteRead:
            return self.get_price(code)
        except RequestsChunkedEncodingError:
            return self.get_price(code)
