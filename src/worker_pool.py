import os
import threading
import time
from datetime import datetime

from shioaji.error import SystemMaintenance

from logger import logger
from rabbitmq import RabbitMQ
from sinopac import Shioaji, ShioajiAuth


class QueryDataLimit:
    def __init__(
        self,
        data: int,
        portfolio: int,
        order: int,
    ):
        self.data = data
        self.portfolio = portfolio
        self.order = order


class WorkerPool:
    def __init__(
        self,
        count: int,
        user: ShioajiAuth,
        rabbit: RabbitMQ,
        request_limt: QueryDataLimit,
    ):
        self.worker_count = count
        self.user = user
        self.rabbit = rabbit

        self.main_worker = Shioaji()
        self.workers: list[Shioaji] = []

        # request count
        self.lock = threading.RLock()
        self.request_count = [int() for _ in range(count - 1)]

        # subscribe list
        self.sub_lock = threading.Lock()
        self.subscribe_count = [int() for _ in range(count - 1)]

        self.stock_tick_sub_dict: dict[str, int] = {}
        self.stock_tick_odds_sub_dict: dict[str, int] = {}

        self.stock_bidask_sub_dict: dict[str, int] = {}
        self.stock_bidask_odds_sub_dict: dict[str, int] = {}

        self.future_tick_sub_dict: dict[str, int] = {}
        self.future_bidask_sub_dict: dict[str, int] = {}

        # request workder limit
        self.request_limit = request_limt
        self.request_worker_times = int()
        self.request_data_timestamp = int()
        self.request_data_times = int()
        self.request_portfolio_timestamp = int()
        self.request_portfolio_times = int()
        self.request_order_timestamp = int()
        self.request_order_times = int()

    def login(self):
        for i in range(self.worker_count):
            logger.info("establish connection %d", i + 1)
            is_main = bool(i == 0)
            try:
                new_connection = Shioaji().login(self.user, is_main)
            except SystemMaintenance:
                time.sleep(75)
                self.logout_and_exit()
            except Exception as error:
                if str(error) != "":
                    logger.error("establish connection %d fail: %s", i + 1, str(error))
                else:
                    logger.error("establish connection %d fail", i + 1)
                self.logout_and_exit()

            if is_main is True:
                self.main_worker = new_connection
            else:
                self.workers.append(new_connection)
            logger.info("login success")

        self.set_event_cb(self.rabbit.event_callback)
        self.set_stock_quote_cb(self.rabbit.stock_quote_callback_v1)
        self.set_future_quote_cb(self.rabbit.future_quote_callback_v1)
        self.set_stock_bid_ask_cb(self.rabbit.stock_bid_ask_callback)
        self.set_future_bid_ask_cb(self.rabbit.future_bid_ask_callback)
        self.set_non_block_order_callback(self.rabbit.order_status_callback)

    def logout_and_exit(self):
        try:
            for worker in self.workers:
                worker.log_out()
            self.get_main().log_out()
        except Exception as error:
            logger.error("logout fail: %s", str(error))
        os._exit(0)

    def get_contract_by_stock_num_arr(self, num_arr: list[str]):
        contract_arr = []
        for num in num_arr:
            contract_arr.append(self.get_main().get_contract_by_stock_num(num))
        return contract_arr

    def get_contract_by_future_code_arr(self, code_arr: list[str]):
        contract_arr = []
        for code in code_arr:
            contract_arr.append(self.get_main().get_contract_by_future_code(code))
        return contract_arr

    def check_usage(self):
        return self.get_main().get_usage()

    def get_sj_version(self):
        return self.get_main().get_sj_version()

    def get_main(self) -> Shioaji:
        return self.main_worker

    def get_data(self) -> Shioaji:
        with self.lock:
            now = round(datetime.now().timestamp() * 1000)
            gap = now - self.request_data_timestamp
            if gap >= 1000:
                self.request_data_timestamp = now
                self.request_data_times = 0
            elif self.request_data_times >= self.request_limit.data:
                rest_time = 1 - (gap / 1000)
                time.sleep(rest_time)
                return self.get_data()
            idx = self.request_count.index(min(self.request_count))
            self.request_count[idx] += 1
            self.request_data_times += 1
            return self.workers[idx]

    def get_portfolio(self) -> Shioaji:
        with self.lock:
            now = round(datetime.now().timestamp() * 1000)
            gap = now - self.request_portfolio_timestamp
            if gap >= 1000:
                self.request_portfolio_timestamp = now
                self.request_portfolio_times = 0
            elif self.request_portfolio_times >= self.request_limit.portfolio:
                rest_time = 1 - (gap / 1000)
                time.sleep(rest_time)
                return self.get_portfolio()
            return self.get_main()

    def get_order_worker(self) -> Shioaji:
        with self.lock:
            now = round(datetime.now().timestamp() * 1000)
            gap = now - self.request_order_timestamp
            if gap >= 1000:
                self.request_order_timestamp = now
                self.request_order_times = 0
            elif self.request_order_times >= self.request_limit.order:
                rest_time = 1 - (gap / 1000)
                time.sleep(rest_time)
                return self.get_order_worker()
            return self.get_main()

    def count(self):
        return len(self.workers)

    def get_all_sub_count(self):
        total = 0
        for count in self.subscribe_count:
            total += count
        return total

    def subscribe_stock_tick(self, stock_num: str, odd: bool):
        with self.sub_lock:
            if odd is True:
                if stock_num in self.stock_tick_odds_sub_dict:
                    return None
            else:
                if stock_num in self.stock_tick_sub_dict:
                    return None
            if self.get_all_sub_count() + 1 > 200 * len(self.workers):
                return None
            idx = self.subscribe_count.index(min(self.subscribe_count))
            result = self.workers[idx].subscribe_stock_tick(stock_num, odd)
            if result is not None:
                return result
            msg = "subscribe stock tick %s %s"
            if odd is True:
                msg = "subscribe stock odd tick %s %s"
            logger.info(
                msg,
                stock_num,
                self.get_main().get_contract_by_stock_num(stock_num).name,
            )
            self.subscribe_count[idx] += 1
            if odd is True:
                self.stock_tick_odds_sub_dict[stock_num] = idx
            else:
                self.stock_tick_sub_dict[stock_num] = idx
        return None

    def unsubscribe_stock_tick(self, stock_num):
        with self.sub_lock:
            if stock_num in self.stock_tick_sub_dict:
                idx = self.stock_tick_sub_dict[stock_num]
                self.subscribe_count[idx] -= 1
                del self.stock_tick_sub_dict[stock_num]
                result = self.workers[idx].unsubscribe_stock_tick(stock_num)
                if result is not None:
                    return result
                logger.info(
                    "unsubscribe stock tick %s %s",
                    stock_num,
                    self.get_main().get_contract_by_stock_num(stock_num).name,
                )
        return None

    def subscribe_future_tick(self, code):
        with self.sub_lock:
            if code in self.future_tick_sub_dict:
                return None
            if self.get_all_sub_count() + 1 > 200 * len(self.workers):
                return None
            idx = self.subscribe_count.index(min(self.subscribe_count))
            result = self.workers[idx].subscribe_future_tick(code)
            if result is not None:
                return result
            logger.info(
                "subscribe future tick %s %s",
                code,
                self.get_main().get_contract_by_future_code(code).name,
            )
            self.subscribe_count[idx] += 1
            self.future_tick_sub_dict[code] = idx
        return None

    def unsubscribe_future_tick(self, code):
        with self.sub_lock:
            if code in self.future_tick_sub_dict:
                idx = self.future_tick_sub_dict[code]
                self.subscribe_count[idx] -= 1
                del self.future_tick_sub_dict[code]
                result = self.workers[idx].unsubscribe_future_tick(code)
                if result is not None:
                    return result
                logger.info(
                    "unsubscribe future tick %s %s",
                    code,
                    self.get_main().get_contract_by_future_code(code).name,
                )
        return None

    def subscribe_stock_bidask(self, stock_num):
        with self.sub_lock:
            if stock_num in self.stock_bidask_sub_dict:
                return None
            if self.get_all_sub_count() + 1 > 200 * len(self.workers):
                return None
            idx = self.subscribe_count.index(min(self.subscribe_count))
            result = self.workers[idx].subscribe_stock_bidask(stock_num)
            if result is not None:
                return result
            logger.info(
                "subscribe stock bidask %s %s",
                stock_num,
                self.get_main().get_contract_by_stock_num(stock_num).name,
            )
            self.subscribe_count[idx] += 1
            self.stock_bidask_sub_dict[stock_num] = idx
        return None

    def unsubscribe_stock_bidask(self, stock_num):
        with self.sub_lock:
            if stock_num in self.stock_bidask_sub_dict:
                idx = self.stock_bidask_sub_dict[stock_num]
                self.subscribe_count[idx] -= 1
                del self.stock_bidask_sub_dict[stock_num]
                result = self.workers[idx].unsubscribe_stock_bidask(stock_num)
                if result is not None:
                    return result
                logger.info(
                    "unsubscribe stock bidask %s %s",
                    stock_num,
                    self.get_main().get_contract_by_stock_num(stock_num).name,
                )
        return None

    def subscribe_future_bidask(self, code):
        with self.sub_lock:
            if code in self.future_bidask_sub_dict:
                return None
            if self.get_all_sub_count() + 1 > 200 * len(self.workers):
                return None
            idx = self.subscribe_count.index(min(self.subscribe_count))
            result = self.workers[idx].subscribe_future_bidask(code)
            if result is not None:
                return result
            logger.info(
                "subscribe future bidask %s %s",
                code,
                self.get_main().get_contract_by_future_code(code).name,
            )
            self.subscribe_count[idx] += 1
            self.future_bidask_sub_dict[code] = idx
        return None

    def unsubscribe_future_bidask(self, code):
        with self.sub_lock:
            if code in self.future_bidask_sub_dict:
                idx = self.future_bidask_sub_dict[code]
                self.subscribe_count[idx] -= 1
                del self.future_bidask_sub_dict[code]
                result = self.workers[idx].unsubscribe_future_bidask(code)
                if result is not None:
                    return result
                logger.info(
                    "unsubscribe future bidask %s %s",
                    code,
                    self.get_main().get_contract_by_future_code(code).name,
                )
        return None

    def unsubscribe_all_tick(self):
        fail_arr: dict[str, list] = {}
        fail_arr["stock"] = []
        fail_arr["future"] = []
        fail_arr["option"] = []

        if len(self.stock_tick_sub_dict) != 0:
            for stock_num in list(self.stock_tick_sub_dict):
                if self.unsubscribe_stock_tick(stock_num) is not None:
                    fail_arr["stock"].append(stock_num)

        if len(self.future_tick_sub_dict) != 0:
            for code in list(self.future_tick_sub_dict):
                if self.unsubscribe_future_tick(code) is not None:
                    fail_arr["future"].append(code)

        return fail_arr

    def unsubscribe_all_bidask(self):
        fail_arr: dict[str, list] = {}
        fail_arr["stock"] = []
        fail_arr["future"] = []
        if len(self.stock_bidask_sub_dict) != 0:
            for stock_num in list(self.stock_bidask_sub_dict):
                if self.unsubscribe_stock_bidask(stock_num) is not None:
                    fail_arr["stock"].append(stock_num)

        if len(self.future_bidask_sub_dict) != 0:
            for code in list(self.future_bidask_sub_dict):
                if self.unsubscribe_future_bidask(code) is not None:
                    fail_arr["future"].append(code)
        return fail_arr

    def set_event_cb(self, func):
        self.get_main().set_event_callback(func)
        for worker in self.workers:
            worker.set_event_callback(func)

    def set_stock_quote_cb(self, func):
        for worker in self.workers:
            worker.set_on_tick_stk_v1_callback(func)

    def set_future_quote_cb(self, func):
        for worker in self.workers:
            worker.set_on_tick_fop_v1_callback(func)

    def set_stock_bid_ask_cb(self, func):
        for worker in self.workers:
            worker.set_on_bidask_stk_v1_callback(func)

    def set_future_bid_ask_cb(self, func):
        for worker in self.workers:
            worker.set_on_bidask_fop_v1_callback(func)

    def set_non_block_order_callback(self, func):
        self.get_main().set_non_block_order_callback(func)

    def buy_stock(self, stock_num, price, quantity):
        return self.get_order_worker().buy_stock(stock_num, price, quantity)

    def sell_stock(self, stock_num, price, quantity):
        return self.get_order_worker().sell_stock(stock_num, price, quantity)

    def buy_odd_stock(self, stock_num, price, share):
        return self.get_order_worker().buy_odd_stock(stock_num, price, share)

    def sell_odd_stock(self, stock_num, price, share):
        return self.get_order_worker().sell_odd_stock(stock_num, price, share)

    def sell_first_stock(self, stock_num, price, quantity):
        return self.get_order_worker().sell_first_stock(stock_num, price, quantity)

    def cancel_stock(self, order_id):
        return self.get_order_worker().cancel_stock(order_id)

    def get_order_status_by_id(self, order_id):
        return self.get_order_worker().get_order_status_from_local_by_order_id(order_id)

    def get_local_order(self):
        return self.get_order_worker().get_local_order()

    def get_non_block_order_status_arr(self):
        return self.get_order_worker().update_order_non_block()

    def buy_future(self, code, price, quantity):
        return self.get_order_worker().buy_future(code, price, quantity)

    def sell_future(self, code, price, quantity):
        return self.get_order_worker().sell_future(code, price, quantity)

    def sell_first_future(self, code, price, quantity):
        return self.get_order_worker().sell_first_future(code, price, quantity)

    def cancel_future(self, order_id):
        return self.get_order_worker().cancel_future(order_id)

    def get_future_position(self):
        return self.get_portfolio().list_future_positions()

    def get_stock_position(self):
        return self.get_portfolio().list_stock_positions()

    def get_position_detail(self, detail_id: int):
        return self.get_portfolio().get_position_detail(detail_id)

    def get_stock_contract_list(self):
        return self.get_main().get_stock_contract_list()

    def get_future_contract_list(self):
        return self.get_main().get_future_contract_list()

    def get_option_contract_list(self):
        return self.get_main().get_option_contract_list()

    def buy_option(self, code, price, quantity):
        return self.get_order_worker().buy_option(code, price, quantity)

    def sell_option(self, code, price, quantity):
        return self.get_order_worker().sell_option(code, price, quantity)

    def sell_first_option(self, code, price, quantity):
        return self.get_order_worker().sell_first_option(code, price, quantity)

    def cancel_option(self, order_id):
        return self.get_order_worker().cancel_option(order_id)

    def account_balance(self):
        return self.get_main().account_balance()

    def margin(self):
        return self.get_portfolio().margin()

    def settlements(self):
        return self.get_portfolio().settlements()

    def get_tse_001_contract(self):
        return self.get_main().get_tse_001_contract()

    def get_otc_101_contract(self):
        return self.get_main().get_otc_101_contract()
