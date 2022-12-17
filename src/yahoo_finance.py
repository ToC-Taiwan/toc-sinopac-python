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
            return [0.0, 0.0]
        except JSONDecodeError:
            return [0.0, 0.0]
        except TypeError:
            return [0.0, 0.0]
        except RemoteDisconnected:
            return [0.0, 0.0]
        except ConnectionResetError:
            return [0.0, 0.0]
        except ProtocolError:
            return [0.0, 0.0]
        except RequestsConnectionError:
            return [0.0, 0.0]
        except KeyError:
            return [0.0, 0.0]
        except IncompleteRead:
            return [0.0, 0.0]
        except RequestsChunkedEncodingError:
            return [0.0, 0.0]
        except RecursionError:
            return [0.0, 0.0]
