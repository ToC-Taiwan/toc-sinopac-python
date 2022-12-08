import os
import threading
import time

import shioaji as sj
from shioaji.constant import DayTrade, OrderState, SecurityType

from logger import logger


class OrderStatus:
    def __init__(self, order_id: str, status: str, error: str):
        self.order_id = order_id
        self.status = status
        self.error = error


class SinopacUser:
    def __init__(self, person_id: str, password: str, ca_password: str):
        self.person_id = person_id
        self.password = password
        self.ca_password = ca_password


class Sinopac:  # pylint: disable=too-many-public-methods
    def __init__(self):
        self.__api = sj.Shioaji()
        self.__login_lock = threading.Lock()
        self.__login_status = int()

        self.stock_num_list: list[str] = []
        self.future_code_list: list[str] = []

        self.__order_status_lock = threading.Lock()
        self.order_status_list: list[sj.order.Trade] = []

    def get_sj_version(self):
        return str(sj.__version__)

    def get_sj_api(self) -> sj.Shioaji:
        return self.__api

    def event_logger_cb(self, resp_code: int, event_code: int, info: str, event: str):
        if event_code != 0:
            logger.info("resp_code: %d", resp_code)
            logger.info("event_code: %d", event_code)
            logger.info("info: %s", info)
            logger.info("event: %s", event)

        if event_code == 12:
            os._exit(1)

    def login_cb(self, security_type):
        with self.__login_lock:
            if security_type.value in [item.value for item in SecurityType]:
                self.__login_status += 1
                # logger.info("%s: %d/4", security_type, self.__login_status)

    def login(self, user: SinopacUser, is_main: bool):
        # before gRPC set cb, using logger to save event
        self.set_event_callback(self.event_logger_cb)

        try:
            self.__api.login(
                person_id=user.person_id,
                passwd=user.password,
                contracts_cb=self.login_cb,
                subscribe_trade=is_main,
            )

        except sj.error.SystemMaintenance:
            logger.error("login 503 system maintenance, terminate after 75 sec")
            wait = 75
            while True:
                time.sleep(1)
                wait -= 1
                if wait == 0:
                    os._exit(1)

        except TimeoutError:
            logger.error("login timeout error, terminate after 60 sec")
            time.sleep(60)
            os._exit(1)

        except ValueError:
            logger.error("login value error, terminate after 15 sec")
            time.sleep(15)
            os._exit(1)

        while True:
            if self.__login_status == 4:
                break

        self.__api.activate_ca(
            ca_path=f"./data/{user.person_id}.pfx",
            ca_passwd=user.ca_password,
            person_id=user.person_id,
        )

        if is_main is True:
            self.fill_stock_num_list()
            self.fill_future_code_list()
            self.set_order_callback(self.place_order_callback)
            logger.info(
                "stock account sign status: %s", self.__api.stock_account.signed
            )
            logger.info(
                "future account sign status: %s", self.__api.futopt_account.signed
            )
            self.update_local_order_status()

        return self

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

    def set_order_status_callback(self, func):
        self.order_status_callback = func

    def fill_stock_num_list(self):
        for contract_arr in self.__api.Contracts.Stocks:
            for contract in contract_arr:
                if (
                    contract.day_trade == DayTrade.Yes.value
                    and contract.category != "00"
                ):
                    self.stock_num_list.append(contract.code)
        if len(self.stock_num_list) != 0:
            logger.info("total stock: %d", len(self.stock_num_list))
        else:
            raise Exception("stock_num_list is empty")

    def get_stock_num_list(self):
        return self.stock_num_list

    def fill_future_code_list(self):
        for future_arr in self.__api.Contracts.Futures:
            for future in future_arr:
                self.future_code_list.append(future.code)
        if len(self.future_code_list) != 0:
            logger.info("total future: %d", len(self.future_code_list))
        else:
            raise Exception("future_code_list is empty")

    def get_future_code_list(self):
        return self.future_code_list

    def list_positions(self):
        try:
            return self.__api.list_positions(self.__api.futopt_account)
        except TimeoutError:
            return None

    def update_order_status_instant(self):
        if self.order_status_callback is None:
            raise Exception("order_status_callback is None")

        with self.__order_status_lock:
            self.__api.update_status(timeout=0, cb=self.order_status_callback)
            return None

    def update_local_order_status(self):
        with self.__order_status_lock:
            self.__api.update_status()
            self.order_status_list = self.__api.list_trades()

    def clear_local_order_status(self):
        with self.__order_status_lock:
            self.order_status_list = []

    def snapshots(self, contracts):
        try:
            return self.__api.snapshots(contracts)
        except TimeoutError:
            logger.error("snapshots timeout error")
            return None

    def get_contract_tse_001(self):
        return self.__api.Contracts.Indexs.TSE.TSE001

    def get_contract_otc_101(self):
        return self.__api.Contracts.Indexs.OTC.OTC101

    def get_contract_by_stock_num(self, num):
        return self.__api.Contracts.Stocks[num]

    def get_contract_by_future_code(self, code):
        return self.__api.Contracts.Futures[code]

    def get_contract_name_by_stock_num(self, num) -> str:
        return str(self.__api.Contracts.Stocks[num].name)

    def get_contract_name_by_future_code(self, code) -> str:
        return str(self.__api.Contracts.Futures[code].name)

    def stock_ticks(self, num, date):
        contract = self.get_contract_by_stock_num(num)
        if num == "tse_001":
            contract = self.get_contract_tse_001()
        elif num == "otc_101":
            contract = self.get_contract_otc_101()

        try:
            return self.__api.ticks(contract, date)
        except TimeoutError:
            return self.stock_ticks(num, date)

    def future_ticks(self, code, date):
        try:
            return self.__api.ticks(self.get_contract_by_future_code(code), date)
        except TimeoutError:
            return self.future_ticks(code, date)

    def stock_kbars(self, num, date):
        contract = self.get_contract_by_stock_num(num)
        if num == "tse_001":
            contract = self.get_contract_tse_001()
        elif num == "otc_101":
            contract = self.get_contract_otc_101()

        try:
            return self.__api.kbars(
                contract=contract,
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
        contract = self.get_contract_by_stock_num(num)
        if num == "tse_001":
            contract = self.get_contract_tse_001()
        elif num == "otc_101":
            contract = self.get_contract_otc_101()

        try:
            ticks = self.__api.quote.ticks(
                contract=contract,
                date=date,
                query_type=sj.constant.TicksQueryType.LastCount,
                last_cnt=1,
            )
            if len(ticks.close) > 0:
                return ticks.close[0]
            return 0
        except TimeoutError:
            return self.get_stock_last_close_by_date(num, date)

    def get_future_last_close_by_date(self, code, date):
        contract = self.get_contract_by_future_code(code)
        try:
            ticks = self.__api.quote.ticks(
                contract=contract,
                date=date,
                query_type=sj.constant.TicksQueryType.LastCount,
                last_cnt=1,
            )
            if len(ticks.close) > 0:
                return ticks.close[0]
            return 0
        except TimeoutError:
            return self.get_future_last_close_by_date(code, date)

    def get_stock_volume_rank_by_date(self, count, date):
        return self.__api.scanners(
            scanner_type=sj.constant.ScannerType.VolumeRank,
            count=count,
            date=date,
        )

    def subscribe_stock_tick(self, stock_num):
        try:
            self.__api.quote.subscribe(
                self.__api.Contracts.Stocks[stock_num],
                quote_type=sj.constant.QuoteType.Tick,
                version=sj.constant.QuoteVersion.v1,
            )
            return None
        except Exception:  # pylint: disable=broad-except
            return stock_num

    def unsubscribe_stock_tick(self, stock_num):
        try:
            self.__api.quote.unsubscribe(
                self.__api.Contracts.Stocks[stock_num],
                quote_type=sj.constant.QuoteType.Tick,
                version=sj.constant.QuoteVersion.v1,
            )
            return None
        except Exception:  # pylint: disable=broad-except
            return stock_num

    def subscribe_future_tick(self, code):
        try:
            self.__api.quote.subscribe(
                self.get_contract_by_future_code(code),
                quote_type=sj.constant.QuoteType.Tick,
                version=sj.constant.QuoteVersion.v1,
            )
            return None
        except Exception:  # pylint: disable=broad-except
            return code

    def unsubscribe_future_tick(self, code):
        try:
            self.__api.quote.unsubscribe(
                self.get_contract_by_future_code(code),
                quote_type=sj.constant.QuoteType.Tick,
                version=sj.constant.QuoteVersion.v1,
            )
            return None
        except Exception:  # pylint: disable=broad-except
            return code

    def subscribe_stock_bidask(self, stock_num):
        try:
            self.__api.quote.subscribe(
                self.__api.Contracts.Stocks[stock_num],
                quote_type=sj.constant.QuoteType.BidAsk,
                version=sj.constant.QuoteVersion.v1,
            )
            return None
        except Exception:  # pylint: disable=broad-except
            return stock_num

    def unsubscribe_stock_bidask(self, stock_num):
        try:
            self.__api.quote.unsubscribe(
                self.__api.Contracts.Stocks[stock_num],
                quote_type=sj.constant.QuoteType.BidAsk,
                version=sj.constant.QuoteVersion.v1,
            )
            return None
        except Exception:  # pylint: disable=broad-except
            return stock_num

    def subscribe_future_bidask(self, code):
        try:
            self.__api.quote.subscribe(
                self.get_contract_by_future_code(code),
                quote_type=sj.constant.QuoteType.BidAsk,
                version=sj.constant.QuoteVersion.v1,
            )
            return None
        except Exception:  # pylint: disable=broad-except
            return code

    def unsubscribe_future_bidask(self, code):
        try:
            self.__api.quote.unsubscribe(
                self.get_contract_by_future_code(code),
                quote_type=sj.constant.QuoteType.BidAsk,
                version=sj.constant.QuoteVersion.v1,
            )
            return None
        except Exception:  # pylint: disable=broad-except
            return code

    def buy_stock(self, stock_num: str, price: float, quantity: int):
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Buy,
            price_type=sj.constant.StockPriceType.LMT,
            order_type=sj.constant.TFTOrderType.ROD,
            order_lot=sj.constant.TFTStockOrderLot.Common,
            account=self.__api.stock_account,
        )
        contract = self.get_contract_by_stock_num(stock_num)
        trade = self.__api.place_order(contract, order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "buy stock fail")

    def sell_stock(self, stock_num: str, price: float, quantity: int):
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Sell,
            price_type=sj.constant.StockPriceType.LMT,
            order_type=sj.constant.TFTOrderType.ROD,
            order_lot=sj.constant.TFTStockOrderLot.Common,
            account=self.__api.stock_account,
        )
        contract = self.get_contract_by_stock_num(stock_num)
        trade = self.__api.place_order(contract, order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "sell stock fail")

    def sell_first_stock(self, stock_num: str, price: float, quantity: int):
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Sell,
            price_type=sj.constant.StockPriceType.LMT,
            order_type=sj.constant.TFTOrderType.ROD,
            order_lot=sj.constant.TFTStockOrderLot.Common,
            first_sell=sj.constant.StockFirstSell.Yes,
            account=self.__api.stock_account,
        )
        contract = self.get_contract_by_stock_num(stock_num)
        trade = self.__api.place_order(contract, order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "sell first stock fail")

    def cancel_stock(self, order_id: str):
        cancel_order = None
        times = int()
        while True:
            self.update_local_order_status()
            for order in self.order_status_list:
                if order.status.id == order_id:
                    cancel_order = order
            if cancel_order is not None or times >= 10:
                break
            times += 1
            time.sleep(1)
        if cancel_order is None:
            return OrderStatus(order_id, "", "id not found")
        if cancel_order.status.status == sj.constant.Status.Cancelled:
            return OrderStatus(order_id, "", "id already cancelled")

        times = 0
        self.__api.cancel_order(cancel_order)
        while True:
            if times >= 10:
                break
            self.update_local_order_status()
            for order in self.order_status_list:
                if (
                    order.status.id == order_id
                    and order.status.status == sj.constant.Status.Cancelled
                ):
                    return OrderStatus(order_id, order.status.status, "")
            times += 1
            time.sleep(1)
        return OrderStatus("", "", "cancel stock fail")

    def get_order_status_from_local_by_order_id(self, order_id: str):
        self.update_local_order_status()
        if len(self.order_status_list) == 0:
            return OrderStatus("", "", "order list is empty")

        for order in self.order_status_list:
            if order.status.id == order_id:
                return OrderStatus(order_id, order.status.status, "")
        return OrderStatus("", "", "order not found")

    def get_order_status(self):
        return self.order_status_list

    def place_order_callback(self, order_state: OrderState, res: dict):
        self.update_local_order_status()
        if order_state in (OrderState.FOrder, OrderState.TFTOrder):
            if res["contract"]["code"] is None:
                logger.error("place order code is none")
                return
            logger.info(
                "%s order: %s %s %.2f %d %s",
                res["operation"]["op_type"],
                res["contract"]["code"],
                res["order"]["action"],
                res["order"]["price"],
                res["order"]["quantity"],
                res["order"]["id"],
            )

        elif order_state in (OrderState.FDeal, OrderState.TFTDeal):
            if res["code"] is None:
                logger.error("deal order code is none")
                return
            logger.info(
                "Deal future order: %s %s %.2f %d %s",
                res["code"],
                res["action"],
                res["price"],
                res["quantity"],
                res["trade_id"],
            )

    def buy_future(self, code: str, price: float, quantity: int):
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Buy,
            price_type=sj.constant.FuturesPriceType.LMT,
            order_type=sj.constant.FuturesOrderType.ROD,
            octype=sj.constant.FuturesOCType.Auto,
            account=self.__api.futopt_account,
        )
        contract = self.get_contract_by_future_code(code)
        trade = self.__api.place_order(contract=contract, order=order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "buy future fail")

    def sell_future(self, code: str, price: float, quantity: int):
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Sell,
            price_type=sj.constant.FuturesPriceType.LMT,
            order_type=sj.constant.FuturesOrderType.ROD,
            octype=sj.constant.FuturesOCType.Auto,
            account=self.__api.futopt_account,
        )
        contract = self.get_contract_by_future_code(code)
        trade = self.__api.place_order(contract=contract, order=order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "sell future fail")

    def sell_first_future(self, code: str, price: float, quantity: int):
        order = self.__api.Order(
            price=price,
            quantity=quantity,
            action=sj.constant.Action.Sell,
            price_type=sj.constant.FuturesPriceType.LMT,
            order_type=sj.constant.FuturesOrderType.ROD,
            octype=sj.constant.FuturesOCType.Auto,
            account=self.__api.futopt_account,
        )
        contract = self.get_contract_by_future_code(code)
        trade = self.__api.place_order(contract=contract, order=order)
        if trade is not None and trade.order.id != "":
            return OrderStatus(trade.order.id, trade.status.status, "")
        return OrderStatus("", "", "sell first future fail")

    def cancel_future(self, order_id: str):
        cancel_order = None
        times = int()
        while True:
            self.update_local_order_status()
            for order in self.order_status_list:
                if order.status.id == order_id:
                    cancel_order = order
            if cancel_order is not None or times >= 10:
                break
            times += 1
            time.sleep(1)
        if cancel_order is None:
            return OrderStatus(order_id, "", "id not found")
        if cancel_order.status.status == sj.constant.Status.Cancelled:
            return OrderStatus(order_id, "", "id already cancelled")

        times = 0
        self.__api.cancel_order(cancel_order)
        while True:
            if times >= 10:
                break
            self.update_local_order_status()
            for order in self.order_status_list:
                if (
                    order.status.id == order_id
                    and order.status.status == sj.constant.Status.Cancelled
                ):
                    return OrderStatus(order_id, order.status.status, "")
            times += 1
            time.sleep(1)
        return OrderStatus("", "", "cancel future fail")
