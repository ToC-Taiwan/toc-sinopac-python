import os
import random
import string
import threading
import time
from datetime import datetime

import shioaji as sj

from constant import DayTrade, OrderState, SecurityType
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
        self.__login_status = int()

        self.stock_num_list = []
        self.future_code_list = []
        self.order_status_list = []

        self.__login_lock = threading.Lock()
        self.__order_status_lock = threading.Lock()
        self.__simulation_lock = threading.Lock()

        # simulate trade
        self.__simulation_count_map = {}  # key: stock_num or code, value: count

    def get_sj_version(self):
        return sj.__version__

    def login(self, user: SinopacUser, is_main: bool):
        # before gRPC set cb, using logger to save event
        self.set_event_callback(event_logger_cb)
        try:
            self.__api.login(
                person_id=user.person_id,
                passwd=user.password,
                contracts_cb=self.login_cb,
                subscribe_trade=is_main,
            )

        except sj.error.SystemMaintenance:
            logger.error("503 system maintenance, terminate after 75 sec")
            wait = 75
            while True:
                time.sleep(1)
                wait -= 1
                if wait == 0:
                    os._exit(1)
                elif wait % 5 == 0:
                    logger.info("system maintenance, wait %d sec", wait)

        except TimeoutError:
            logger.error("timeout error, retry after 60 sec")
            time.sleep(60)
            os._exit(1)

        except ValueError:
            logger.error("value error, retry after 15 sec")
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

        self.fill_stock_num_list()
        self.fill_future_code_list()
        if is_main is True:
            self.set_order_callback(self.place_order_callback)
            logger.info(self.__api.stock_account)
            logger.info(self.__api.futopt_account)

        return self

    def login_cb(self, security_type):
        with self.__login_lock:
            if security_type.value in [item.value for item in SecurityType]:
                self.__login_status += 1
                logger.info(
                    "login progress: %d/4, %s", self.__login_status, security_type
                )

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

    def list_accounts(self):
        return self.__api.list_accounts()

    def fill_stock_num_list(self):
        for contract_arr in self.__api.Contracts.Stocks:
            for contract in contract_arr:
                if (
                    contract.day_trade == DayTrade.Yes.value
                    and contract.category != "00"
                ):
                    self.stock_num_list.append(contract.code)
                    self.__simulation_count_map[contract.code] = 0
        if len(self.stock_num_list) != 0:
            logger.info("filling stock_num_list, total: %d", len(self.stock_num_list))
        else:
            raise Exception("stock_num_list is empty")

    def fill_future_code_list(self):
        for future_arr in self.__api.Contracts.Futures:
            for future in future_arr:
                self.future_code_list.append(future.code)
                self.__simulation_count_map[future.code] = 0
        if len(self.future_code_list) != 0:
            logger.info(
                "filling future_code_list, total: %d", len(self.future_code_list)
            )
        else:
            raise Exception("future_code_list is empty")

    def update_order_status_instant(self):
        if self.order_status_callback is None:
            return "order_status_callback is None"

        with self.__order_status_lock:
            self.__api.update_status(timeout=0, cb=self.order_status_callback)
            return None

    def list_positions(self):
        try:
            return self.__api.list_positions(self.__api.futopt_account)
        except TimeoutError:
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

    def finish_simulation_order(self, order: sj.order.Trade, wait: int):
        self.order_status_list.append(order)
        with self.__simulation_lock:
            buy_later = False
            if (
                order.order.action == sj.constant.Action.Buy
                and self.__simulation_count_map[order.contract.code] < 0
            ):
                buy_later = True
                self.__simulation_count_map[order.contract.code] += order.order.quantity
            if order.order.action == sj.constant.Action.Sell:
                self.__simulation_count_map[order.contract.code] -= order.order.quantity

        time.sleep(wait)
        with self.__simulation_lock:
            for sim in self.order_status_list:
                if sim.status.id == order.status.id:
                    sim.status.status = sj.constant.Status.Filled
                    if (
                        sim.order.action == sj.constant.Action.Buy
                        and buy_later is False
                    ):
                        self.__simulation_count_map[
                            sim.contract.code
                        ] += sim.order.quantity

    def buy_stock(self, stock_num: str, price: float, quantity: int, sim: bool):
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

        if sim is False:
            trade = self.__api.place_order(contract, order)
            if trade is not None and trade.order.id != "":
                return OrderStatus(trade.order.id, trade.status.status, "")
        else:
            with self.__simulation_lock:
                if self.__simulation_count_map[stock_num] < 0:
                    if quantity + self.__simulation_count_map[stock_num] > 0:
                        return OrderStatus("", "", "buy later quantity is too big")
            sim_order = sj.order.Trade(
                contract=contract,
                order=order,
                status=sj.order.OrderStatus(
                    id="".join(
                        random.choice(string.ascii_lowercase + string.octdigits)
                        for _ in range(8)
                    ),
                    status=sj.constant.Status.Submitted,
                    status_code="",
                    order_datetime=datetime.now(),
                    deals=[],
                ),
            )
            threading.Thread(
                target=self.finish_simulation_order,
                args=(sim_order, random.randrange(5) + 1),
            ).start()
            return OrderStatus(sim_order.status.id, sim_order.status.status, "")

        return OrderStatus("", "", "unknown error")

    def sell_stock(self, stock_num: str, price: float, quantity: int, sim: bool):
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

        if sim is False:
            trade = self.__api.place_order(contract, order)
            if trade is not None and trade.order.id != "":
                return OrderStatus(trade.order.id, trade.status.status, "")
        else:
            with self.__simulation_lock:
                if quantity > self.__simulation_count_map[stock_num]:
                    return OrderStatus("", "", "quantity is too big")
                sim_order = sj.order.Trade(
                    contract=contract,
                    order=order,
                    status=sj.order.OrderStatus(
                        id="".join(
                            random.choice(string.ascii_lowercase + string.octdigits)
                            for _ in range(8)
                        ),
                        status=sj.constant.Status.Submitted,
                        status_code="",
                        order_datetime=datetime.now(),
                        deals=[],
                    ),
                )
            threading.Thread(
                target=self.finish_simulation_order,
                args=(sim_order, random.randrange(5) + 1),
            ).start()
            return OrderStatus(sim_order.status.id, sim_order.status.status, "")

        return OrderStatus("", "", "unknown error")

    def sell_first_stock(self, stock_num: str, price: float, quantity: int, sim: bool):
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

        if sim is False:
            trade = self.__api.place_order(contract, order)
            if trade is not None and trade.order.id != "":
                return OrderStatus(trade.order.id, trade.status.status, "")
        else:
            with self.__simulation_lock:
                if self.__simulation_count_map[stock_num] > 0:
                    return OrderStatus("", "", "can not sell first")
                sim_order = sj.order.Trade(
                    contract=contract,
                    order=order,
                    status=sj.order.OrderStatus(
                        id="".join(
                            random.choice(string.ascii_lowercase + string.octdigits)
                            for _ in range(8)
                        ),
                        status=sj.constant.Status.Submitted,
                        status_code="",
                        order_datetime=datetime.now(),
                        deals=[],
                    ),
                )
            threading.Thread(
                target=self.finish_simulation_order,
                args=(sim_order, random.randrange(5) + 1),
            ).start()
            return OrderStatus(sim_order.status.id, sim_order.status.status, "")

        return OrderStatus("", "", "unknown error")

    def cancel_stock(self, order_id: str, sim: bool):
        if sim is False:
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
        else:
            for order in self.order_status_list:
                if (
                    order.status.id == order_id
                    and order.status.status != sj.constant.Status.Cancelled
                ):
                    order.status.status = sj.constant.Status.Cancelled
                    return OrderStatus(order_id, order.status.status, "")

        return OrderStatus("", "", "cancel order fail, unknown error")

    def get_order_status_from_local_by_order_id(self, order_id: str, sim: bool):
        if sim is False:
            self.update_local_order_status()

        if len(self.order_status_list) == 0:
            return OrderStatus("", "", "order list is empty")

        for order in self.order_status_list:
            if order.status.id == order_id:
                return OrderStatus(order_id, order.status.status, "")

        return OrderStatus("", "", "unknown error")

    def get_order_status(self):
        return self.order_status_list

    def place_order_callback(self, order_state: OrderState, order: dict):
        if order_state == OrderState.TFTOrder:
            if order["contract"]["code"] is None:
                logger.error("place stock contract code is None")
                return

            logger.info(
                "%s stock order: %s %s %s %.2f %d %s",
                order["operation"]["op_type"],
                order["contract"]["code"],
                self.get_contract_name_by_stock_num(order["contract"]["code"]),
                order["order"]["action"],
                order["order"]["price"],
                order["order"]["quantity"],
                order["order"]["id"],
            )

        elif order_state == OrderState.TFTDeal:
            if order["code"] is None:
                logger.error("deal contract code is None")
                return

            logger.info(
                "Deal stock order: %s %s %s %.2f %d %s",
                order["code"],
                self.get_contract_name_by_stock_num(order["contract"]["code"]),
                order["action"],
                order["price"],
                order["quantity"],
                order["trade_id"],
            )

        elif order_state == OrderState.FOrder:
            if order["contract"]["code"] is None:
                logger.error("place future contract code is None")
                return

            logger.info(
                "%s future order: %s %s %s %.2f %d %s",
                order["operation"]["op_type"],
                order["contract"]["code"],
                self.get_contract_name_by_future_code(order["contract"]["code"]),
                order["order"]["action"],
                order["order"]["price"],
                order["order"]["quantity"],
                order["order"]["id"],
            )

        elif order_state == OrderState.FDeal:
            if order["code"] is None:
                logger.error("deal contract code is None")
                return

            logger.info(
                "Deal future order: %s %s %s %.2f %d %s",
                order["code"],
                self.get_contract_name_by_future_code(order["code"]),
                order["action"],
                order["price"],
                order["quantity"],
                order["trade_id"],
            )

    def buy_future(self, code: str, price: float, quantity: int, sim: bool):
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
        if sim is False:
            trade = self.__api.place_order(contract=contract, order=order)
            if trade is not None and trade.order.id != "":
                return OrderStatus(trade.order.id, trade.status.status, "")
        else:
            with self.__simulation_lock:
                if self.__simulation_count_map[code] < 0:
                    if quantity + self.__simulation_count_map[code] > 0:
                        return OrderStatus("", "", "buy later quantity is too big")
            sim_order = sj.order.Trade(
                contract=contract,
                order=order,
                status=sj.order.OrderStatus(
                    id="".join(
                        random.choice(string.ascii_lowercase + string.octdigits)
                        for _ in range(8)
                    ),
                    status=sj.constant.Status.Submitted,
                    status_code="",
                    order_datetime=datetime.now(),
                    deals=[],
                ),
            )
            threading.Thread(
                target=self.finish_simulation_order,
                args=(sim_order, 1),
            ).start()
            return OrderStatus(sim_order.status.id, sim_order.status.status, "")
        return OrderStatus("", "", "unknown error")

    def sell_future(self, code: str, price: float, quantity: int, sim: bool):
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
        if sim is False:
            trade = self.__api.place_order(contract=contract, order=order)
            if trade is not None and trade.order.id != "":
                return OrderStatus(trade.order.id, trade.status.status, "")
        else:
            with self.__simulation_lock:
                if quantity > self.__simulation_count_map[code]:
                    return OrderStatus("", "", "quantity is too big")
                sim_order = sj.order.Trade(
                    contract=contract,
                    order=order,
                    status=sj.order.OrderStatus(
                        id="".join(
                            random.choice(string.ascii_lowercase + string.octdigits)
                            for _ in range(8)
                        ),
                        status=sj.constant.Status.Submitted,
                        status_code="",
                        order_datetime=datetime.now(),
                        deals=[],
                    ),
                )
            threading.Thread(
                target=self.finish_simulation_order,
                args=(sim_order, 1),
            ).start()
            return OrderStatus(sim_order.status.id, sim_order.status.status, "")
        return OrderStatus("", "", "unknown error")

    def sell_first_future(self, code: str, price: float, quantity: int, sim: bool):
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
        if sim is False:
            trade = self.__api.place_order(contract=contract, order=order)
            if trade is not None and trade.order.id != "":
                return OrderStatus(trade.order.id, trade.status.status, "")
        else:
            with self.__simulation_lock:
                if self.__simulation_count_map[code] > 0:
                    return OrderStatus("", "", "can not sell first")
                sim_order = sj.order.Trade(
                    contract=contract,
                    order=order,
                    status=sj.order.OrderStatus(
                        id="".join(
                            random.choice(string.ascii_lowercase + string.octdigits)
                            for _ in range(8)
                        ),
                        status=sj.constant.Status.Submitted,
                        status_code="",
                        order_datetime=datetime.now(),
                        deals=[],
                    ),
                )
            threading.Thread(
                target=self.finish_simulation_order,
                args=(sim_order, 1),
            ).start()
            return OrderStatus(sim_order.status.id, sim_order.status.status, "")
        return OrderStatus("", "", "unknown error")

    def cancel_future(self, order_id: str, sim: bool):
        if sim is False:
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
        else:
            for order in self.order_status_list:
                if (
                    order.status.id == order_id
                    and order.status.status != sj.constant.Status.Cancelled
                ):
                    order.status.status = sj.constant.Status.Cancelled
                    return OrderStatus(order_id, order.status.status, "")
        return OrderStatus("", "", "cancel future order fail, unknown error")

    def clear_simulation_order(self):
        clear_count = int()
        for stock in self.stock_num_list:
            s = self.__simulation_count_map[stock]
            if s != 0:
                self.__simulation_count_map[stock] = 0
                clear_count += 1
        for future in self.future_code_list:
            f = self.__simulation_count_map[future]
            if f != 0:
                self.__simulation_count_map[future] = 0
                clear_count += 1
        if clear_count > 0:
            logger.info("clear %d simulation order", clear_count)


def event_logger_cb(resp_code: int, event_code: int, info: str, event: str):
    if event_code != 0:
        logger.info("resp_code: %d", resp_code)
        logger.info("event_code: %d", event_code)
        logger.info("info: %s", info)
        logger.info("event: %s", event)

    if event_code == 12:
        os._exit(1)
