import logging
import threading
import time
from typing import List

import shioaji as sj
import shioaji.constant as sc
from shioaji.contracts import Contract
from shioaji.error import SystemMaintenance, TokenError
from shioaji.order import Order, Trade
from shioaji.position import AccountBalance, FuturePosition, Margin, StockPosition

from logger import logger

logging.getLogger("shioaji").propagate = False


class OrderStatus:
    def __init__(self, order_id: str, status: str, error: str):
        self.order_id = order_id
        self.status = status
        self.error = error


class ShioajiAuth:
    def __init__(self, api_key: str, api_key_secret: str, person_id: str, ca_password: str):
        self.api_key = api_key
        self.api_key_secret = api_key_secret
        self.person_id = person_id
        self.ca_password = ca_password


class Shioaji:
    def __init__(self):
        self.__api = sj.Shioaji()
        self.__login_status_lock = threading.Lock()
        self.__login_progess = int()

        # callback initialization avoid NoneType error
        self.non_block_order_callback = None

        # order map with lock
        self.__order_map: dict[str, Trade] = {}  # order_id: Trade
        self.__order_map_lock = threading.Lock()

        # stock, future, option code map
        self.stock_map: dict[str, Contract] = {}
        self.stock_map_lock = threading.Lock()

        self.future_map: dict[str, Contract] = {}
        self.future_map_lock = threading.Lock()

        self.option_map: dict[str, Contract] = {}
        self.option_map_lock = threading.Lock()

    def login(self, user: ShioajiAuth, is_main: bool):
        # before gRPC set cb, using logger to save event
        def event_logger_cb(resp_code: int, event_code: int, info: str, event: str):
            if event_code != 0:
                logger.warning("resp_code: %d", resp_code)
                logger.warning("event_code: %d", event_code)
                logger.warning("info: %s", info)
                logger.warning("event: %s", event)

            if event_code == 12:
                time.sleep(30)
                raise RuntimeError("reconnecting in initial login")

        def login_cb(security_type: sc.SecurityType):
            with self.__login_status_lock:
                if security_type.value in [item.value for item in sc.SecurityType]:
                    self.__login_progess += 1
                    logger.info("login progress: %d/4, %s", self.__login_progess, security_type)

        try:
            self.set_event_callback(event_logger_cb)
            self.__api.login(
                api_key=user.api_key,
                secret_key=user.api_key_secret,
                contracts_cb=login_cb,
                subscribe_trade=is_main,
            )

        except SystemMaintenance as exc:
            time.sleep(75)
            raise RuntimeError("login 503 system maintenance") from exc

        except Exception as error:
            time.sleep(30)
            raise RuntimeError("login error") from error

        while True:
            with self.__login_status_lock:
                if self.__login_progess == 4:
                    break

        self.__api.activate_ca(
            ca_path=f"./data/{user.person_id}.pfx",
            ca_passwd=user.ca_password,
            person_id=user.person_id,
        )

        self.fill_stock_map()
        self.fill_future_map()
        self.fill_option_map()

        if is_main is True:
            if self.__api.stock_account.signed is False or self.__api.futopt_account.signed is False:
                raise RuntimeError("account not sign")

            self.set_order_callback(self.order_callback)
            self.update_local_order()

        return self

    def log_out(self):
        try:
            self.__api.logout()
            logger.info("logout shioaji")
        except Exception:
            logger.error("logout shioaji fail")

    def get_usage(self):
        return self.__api.usage()

    def get_sj_version(self):
        return str(sj.__version__)

    def set_event_callback(self, func):
        self.__api.quote.set_event_callback(func)

    def set_on_tick_stk_v1_callback(self, func):
        self.__api.quote.set_on_tick_stk_v1_callback(func)

    def set_on_tick_fop_v1_callback(self, func):
        self.__api.quote.set_on_tick_fop_v1_callback(func)

    def set_on_bidask_stk_v1_callback(self, func):
        self.__api.quote.set_on_bidask_stk_v1_callback(func)

    def set_on_bidask_fop_v1_callback(self, func):
        self.__api.quote.set_on_bidask_fop_v1_callback(func)

    def set_order_callback(self, func):
        self.__api.set_order_callback(func)

    def set_non_block_order_callback(self, func):
        self.non_block_order_callback = func

    def fill_stock_map(self):
        for contract_arr in self.__api.Contracts.Stocks:
            for contract in contract_arr:
                if contract.day_trade == sc.DayTrade.Yes.value and contract.category != "00":
                    with self.stock_map_lock:
                        self.stock_map[contract.code] = contract
        with self.stock_map_lock:
            if len(self.stock_map) != 0:
                logger.info("total stock: %d", len(self.stock_map))
            else:
                raise RuntimeError("stock_map is empty")

    def get_stock_contract_list(self):
        with self.stock_map_lock:
            return list(self.stock_map.values())

    def get_contract_by_stock_num(self, num):
        if num == "tse_001":
            return self.__api.Contracts.Indexs.TSE.TSE001

        if num == "otc_101":
            return self.__api.Contracts.Indexs.OTC.OTC101

        with self.stock_map_lock:
            return self.stock_map[num]

    def fill_future_map(self):
        for future_arr in self.__api.Contracts.Futures:
            for future in future_arr:
                with self.future_map_lock:
                    self.future_map[future.code] = future
        with self.future_map_lock:
            if len(self.future_map) != 0:
                logger.info("total future: %d", len(self.future_map))
            else:
                raise RuntimeError("future_map is empty")

    def get_future_contract_list(self):
        with self.future_map_lock:
            return list(self.future_map.values())

    def get_contract_by_future_code(self, code):
        with self.future_map_lock:
            return self.future_map[code]

    def fill_option_map(self):
        for option_arr in self.__api.Contracts.Options:
            for option in option_arr:
                with self.option_map_lock:
                    self.option_map[option.code] = option
        with self.option_map_lock:
            if len(self.option_map) != 0:
                logger.info("total option: %d", len(self.option_map))
            else:
                raise RuntimeError("option_map is empty")

    def get_option_contract_list(self):
        with self.option_map_lock:
            return list(self.option_map.values())

    def get_contract_by_option_code(self, code):
        with self.option_map_lock:
            return self.option_map[code]

    def get_local_order(self) -> list[Trade]:
        with self.__order_map_lock:
            return list(self.__order_map.values())

    def get_local_order_by_order_id(self, order_id: str):
        with self.__order_map_lock:
            return self.__order_map.get(order_id, None)

    def get_order_status_from_local_by_order_id(self, order_id: str):
        order = self.get_local_order_by_order_id(order_id)
        if order is None:
            return OrderStatus("", "", "order not found")
        return OrderStatus(order_id, order.status.status, "")

    def update_local_order(self):
        with self.__order_map_lock:
            cache = self.__order_map.copy()
            self.__order_map = {}
            try:
                self.__api.update_status()
                for order in self.__api.list_trades():
                    self.__order_map[order.order.id] = order
            except Exception:
                self.__order_map = cache

    def order_callback(self, order_state: sc.OrderState, res: dict):
        # every time order callback, update local order
        self.update_local_order()
        if order_state in (sc.OrderState.FuturesOrder, sc.OrderState.StockOrder):
            if res["contract"]["code"] is None:
                logger.error("place order code is none")
                return
            logger.info(
                "%s order: %s %s %.2f %d %s",
                str(res["operation"]["op_type"]).lower(),
                res["contract"]["code"],
                res["order"]["action"],
                res["order"]["price"],
                res["order"]["quantity"],
                res["order"]["id"],
            )

        elif order_state in (sc.OrderState.FuturesDeal, sc.OrderState.StockDeal):
            if res["code"] is None:
                logger.error("deal order code is none")
                return
            logger.info(
                "deal order: %s %s %.2f %d %s",
                res["code"],
                res["action"],
                res["price"],
                res["quantity"],
                res["trade_id"],
            )

    def update_order_non_block(self):
        if self.non_block_order_callback is None:
            return "non_block_order_callback is None"

        with self.__order_map_lock:
            try:
                self.__api.update_status(timeout=0, cb=self.non_block_order_callback)
                return ""
            except Exception:
                return "update_order_non_block fail"

    def snapshots(self, contracts):
        try:
            return self.__api.snapshots(contracts)
        except TokenError as error:
            raise error
        except Exception as error:
            logger.error(str(error))
            return None

    def stock_ticks(self, num, date):
        try:
            return self.__api.ticks(self.get_contract_by_stock_num(num), date)
        except TimeoutError:
            return self.stock_ticks(num, date)

    def future_ticks(self, code, date):
        try:
            return self.__api.ticks(self.get_contract_by_future_code(code), date)
        except TimeoutError:
            return self.future_ticks(code, date)

    def stock_kbars(self, num, date):
        try:
            return self.__api.kbars(
                contract=self.get_contract_by_stock_num(num),
                start=date,
                end=date,
            )
        except TimeoutError:
            return self.stock_kbars(num, date)

    def future_kbars(self, code, date):
        try:
            return self.__api.kbars(
                contract=self.get_contract_by_future_code(code),
                start=date,
                end=date,
            )
        except TimeoutError:
            return self.future_kbars(code, date)

    def get_stock_last_close_by_date(self, num, date):
        try:
            ticks = self.__api.quote.ticks(
                contract=self.get_contract_by_stock_num(num),
                date=date,
                query_type=sc.TicksQueryType.LastCount,
                last_cnt=1,
            )
            if len(ticks.close) > 0:
                return ticks.close[0]
            return 0
        except TimeoutError:
            return self.get_stock_last_close_by_date(num, date)

    def get_future_last_close_by_date(self, code, date):
        try:
            ticks = self.__api.quote.ticks(
                contract=self.get_contract_by_future_code(code),
                date=date,
                query_type=sc.TicksQueryType.LastCount,
                last_cnt=1,
            )
            if len(ticks.close) > 0:
                return ticks.close[0]
            return 0
        except TimeoutError:
            return self.get_future_last_close_by_date(code, date)

    def get_stock_volume_rank_by_date(self, count, date):
        return self.__api.scanners(
            scanner_type=sc.ScannerType.VolumeRank,
            count=count,
            date=date,
        )

    def subscribe_stock_tick(self, stock_num: str, odd: bool):
        try:
            self.__api.quote.subscribe(
                self.get_contract_by_stock_num(stock_num),
                quote_type=sc.QuoteType.Tick,
                version=sc.QuoteVersion.v1,
                intraday_odd=odd,
            )
            return None
        except Exception:
            return stock_num

    def unsubscribe_stock_tick(self, stock_num):
        try:
            self.__api.quote.unsubscribe(
                self.get_contract_by_stock_num(stock_num),
                quote_type=sc.QuoteType.Tick,
                version=sc.QuoteVersion.v1,
            )
            return None
        except Exception:
            return stock_num

    def subscribe_future_tick(self, code):
        try:
            self.__api.quote.subscribe(
                self.get_contract_by_future_code(code),
                quote_type=sc.QuoteType.Tick,
                version=sc.QuoteVersion.v1,
            )
            return None
        except Exception:
            return code

    def unsubscribe_future_tick(self, code):
        try:
            self.__api.quote.unsubscribe(
                self.get_contract_by_future_code(code),
                quote_type=sc.QuoteType.Tick,
                version=sc.QuoteVersion.v1,
            )
            return None
        except Exception:
            return code

    def subscribe_option_tick(self, code):
        try:
            self.__api.quote.subscribe(
                self.get_contract_by_option_code(code),
                quote_type=sc.QuoteType.Tick,
                version=sc.QuoteVersion.v1,
            )
            return None
        except Exception:
            return code

    def unsubscribe_option_tick(self, code):
        try:
            self.__api.quote.unsubscribe(
                self.get_contract_by_option_code(code),
                quote_type=sc.QuoteType.Tick,
                version=sc.QuoteVersion.v1,
            )
            return None
        except Exception:
            return code

    def subscribe_stock_bidask(self, stock_num):
        try:
            self.__api.quote.subscribe(
                self.get_contract_by_stock_num(stock_num),
                quote_type=sc.QuoteType.BidAsk,
                version=sc.QuoteVersion.v1,
            )
            return None
        except Exception:
            return stock_num

    def unsubscribe_stock_bidask(self, stock_num):
        try:
            self.__api.quote.unsubscribe(
                self.get_contract_by_stock_num(stock_num),
                quote_type=sc.QuoteType.BidAsk,
                version=sc.QuoteVersion.v1,
            )
            return None
        except Exception:
            return stock_num

    def subscribe_future_bidask(self, code):
        try:
            self.__api.quote.subscribe(
                self.get_contract_by_future_code(code),
                quote_type=sc.QuoteType.BidAsk,
                version=sc.QuoteVersion.v1,
            )
            return None
        except Exception:
            return code

    def unsubscribe_future_bidask(self, code):
        try:
            self.__api.quote.unsubscribe(
                self.get_contract_by_future_code(code),
                quote_type=sc.QuoteType.BidAsk,
                version=sc.QuoteVersion.v1,
            )
            return None
        except Exception:
            return code

    def buy_stock(self, stock_num: str, price: float, quantity: int):
        order: Order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sc.Action.Buy,
            price_type=sc.StockPriceType.LMT,
            order_type=sc.OrderType.ROD,
            order_lot=sc.StockOrderLot.Common,
            account=self.__api.stock_account,
        )
        trade = self.__api.place_order(self.get_contract_by_stock_num(stock_num), order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "buy stock fail")

    def sell_stock(self, stock_num: str, price: float, quantity: int):
        order: Order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sc.Action.Sell,
            price_type=sc.StockPriceType.LMT,
            order_type=sc.OrderType.ROD,
            order_lot=sc.StockOrderLot.Common,
            account=self.__api.stock_account,
        )
        trade = self.__api.place_order(self.get_contract_by_stock_num(stock_num), order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "sell stock fail")

    def sell_first_stock(self, stock_num: str, price: float, quantity: int):
        order: Order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sc.Action.Sell,
            price_type=sc.StockPriceType.LMT,
            order_type=sc.OrderType.ROD,
            order_lot=sc.StockOrderLot.Common,
            daytrade_short=True,
            account=self.__api.stock_account,
        )
        trade = self.__api.place_order(self.get_contract_by_stock_num(stock_num), order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "sell first stock fail")

    def cancel_stock(self, order_id: str):
        cancel_order = self.get_local_order_by_order_id(order_id)
        if cancel_order is None:
            return OrderStatus(order_id, "", "id not found")
        if cancel_order.status.status == sc.Status.Cancelled:
            return OrderStatus(order_id, sc.Status.Cancelled.value, "")

        self.__api.cancel_order(cancel_order)
        self.update_local_order()
        return OrderStatus(order_id, self.get_local_order_by_order_id(order_id).status.status, "")

    def buy_future(self, code: str, price: float, quantity: int):
        order: Order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sc.Action.Buy,
            price_type=sc.FuturesPriceType.LMT,
            order_type=sc.OrderType.ROD,
            octype=sc.FuturesOCType.Auto,
            account=self.__api.futopt_account,
        )
        trade = self.__api.place_order(contract=self.get_contract_by_future_code(code), order=order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "buy future fail")

    def sell_future(self, code: str, price: float, quantity: int):
        order: Order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sc.Action.Sell,
            price_type=sc.FuturesPriceType.LMT,
            order_type=sc.OrderType.ROD,
            octype=sc.FuturesOCType.Auto,
            account=self.__api.futopt_account,
        )
        trade = self.__api.place_order(contract=self.get_contract_by_future_code(code), order=order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "sell future fail")

    def sell_first_future(self, code: str, price: float, quantity: int):
        order: Order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sc.Action.Sell,
            price_type=sc.FuturesPriceType.LMT,
            order_type=sc.OrderType.ROD,
            octype=sc.FuturesOCType.Auto,
            account=self.__api.futopt_account,
        )
        trade = self.__api.place_order(contract=self.get_contract_by_future_code(code), order=order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "sell first future fail")

    def cancel_future(self, order_id: str):
        cancel_order = self.get_local_order_by_order_id(order_id)
        if cancel_order is None:
            return OrderStatus(order_id, "", "id not found")
        if cancel_order.status.status == sc.Status.Cancelled:
            return OrderStatus(order_id, sc.Status.Cancelled.value, "")

        self.__api.cancel_order(cancel_order)
        self.update_local_order()
        return OrderStatus(order_id, self.get_local_order_by_order_id(order_id).status.status, "")

    def buy_option(self, code: str, price: float, quantity: int):
        order: Order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sc.Action.Buy,
            price_type=sc.FuturesPriceType.LMT,
            order_type=sc.OrderType.ROD,
            account=self.__api.futopt_account,
        )
        trade = self.__api.place_order(contract=self.get_contract_by_option_code(code), order=order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "buy option fail")

    def sell_option(self, code: str, price: float, quantity: int):
        order: Order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sc.Action.Sell,
            price_type=sc.FuturesPriceType.LMT,
            order_type=sc.OrderType.ROD,
            account=self.__api.futopt_account,
        )
        trade = self.__api.place_order(contract=self.get_contract_by_option_code(code), order=order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "sell option fail")

    def sell_first_option(self, code: str, price: float, quantity: int):
        order: Order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sc.Action.Sell,
            price_type=sc.FuturesPriceType.LMT,
            order_type=sc.OrderType.ROD,
            account=self.__api.futopt_account,
        )
        trade = self.__api.place_order(contract=self.get_contract_by_option_code(code), order=order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "sell first option fail")

    def cancel_option(self, order_id: str):
        cancel_order = self.get_local_order_by_order_id(order_id)
        if cancel_order is None:
            return OrderStatus(order_id, "", "id not found")
        if cancel_order.status.status == sc.Status.Cancelled:
            return OrderStatus(order_id, sc.Status.Cancelled.value, "")

        self.__api.cancel_order(cancel_order)
        self.update_local_order()
        return OrderStatus(order_id, self.get_local_order_by_order_id(order_id).status.status, "")

    def account_balance(self) -> AccountBalance | None:
        try:
            return self.__api.account_balance()
        except Exception:
            return None

    def margin(self) -> Margin | None:
        try:
            return self.__api.margin(self.__api.futopt_account)
        except Exception:
            return None

    def list_future_positions(self) -> List[FuturePosition]:
        try:
            result: List[FuturePosition] = []
            result = self.__api.list_positions(self.__api.futopt_account)
            return result
        except Exception:
            return []

    def list_stock_positions(self) -> List[StockPosition]:
        try:
            result: List[StockPosition] = []
            result = self.__api.list_positions(self.__api.stock_account)
            return result
        except Exception:
            return []

    def settlements(self):
        try:
            return self.__api.settlements(self.__api.stock_account)
        except Exception:
            return []

    def buy_odd_stock(self, stock_num: str, price: float, share: int):
        if share >= 1000:
            return OrderStatus("", "", "share must be less than 1000")

        order: Order = self.__api.Order(
            price=price,
            quantity=share,
            action=sc.Action.Buy,
            price_type=sc.StockPriceType.LMT,
            order_type=sc.OrderType.ROD,
            order_lot=sc.StockOrderLot.IntradayOdd,
            account=self.__api.stock_account,
        )
        trade = self.__api.place_order(self.get_contract_by_stock_num(stock_num), order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "buy odd stock fail")

    def sell_odd_stock(self, stock_num: str, price: float, share: int):
        if share >= 1000:
            return OrderStatus("", "", "share must be less than 1000")

        order: Order = self.__api.Order(
            price=price,
            quantity=share,
            action=sc.Action.Sell,
            price_type=sc.StockPriceType.LMT,
            order_type=sc.OrderType.ROD,
            order_lot=sc.StockOrderLot.IntradayOdd,
            account=self.__api.stock_account,
        )
        trade = self.__api.place_order(self.get_contract_by_stock_num(stock_num), order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "sell odd stock fail")
