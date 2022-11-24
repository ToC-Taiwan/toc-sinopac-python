from http.client import RemoteDisconnected
from json import JSONDecodeError

import yfinance as yf
from requests.exceptions import ConnectionError
from urllib3.exceptions import ProtocolError

from logger import logger


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
            return self.get_nasdaq()

        except JSONDecodeError:
            logger.warning("JSONDecodeError from get_nasdaq")
            return self.get_nasdaq()
        except TypeError:
            logger.warning("TypeError from get_nasdaq")
            return self.get_nasdaq()
        except RemoteDisconnected:
            logger.warning("RemoteDisconnected from get_nasdaq")
            return self.get_nasdaq()
        except ConnectionResetError:
            logger.warning("ConnectionResetError from get_nasdaq")
            return self.get_nasdaq()
        except ProtocolError:
            logger.warning("ProtocolError from get_nasdaq")
            return self.get_nasdaq()
        except ConnectionError:
            logger.warning("ConnectionError from get_nasdaq")
            return self.get_nasdaq()

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
            return self.get_nasdaq_future()

        except JSONDecodeError:
            logger.warning("JSONDecodeError from get_nasdaq_future")
            return self.get_nasdaq_future()
        except TypeError:
            logger.warning("TypeError from get_nasdaq_future")
            return self.get_nasdaq_future()
        except RemoteDisconnected:
            logger.warning("RemoteDisconnected from get_nasdaq_future")
            return self.get_nasdaq_future()
        except ConnectionResetError:
            logger.warning("ConnectionResetError from get_nasdaq_future")
            return self.get_nasdaq_future()
        except ProtocolError:
            logger.warning("ProtocolError from get_nasdaq_future")
            return self.get_nasdaq_future()
        except ConnectionError:
            logger.warning("ConnectionError from get_nasdaq_future")
            return self.get_nasdaq_future()
