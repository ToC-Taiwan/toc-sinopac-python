import threading
import time
from datetime import datetime

from logger import logger
from sinopac import Sinopac


class SinopacWorkerPool:  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    def __init__(self, main_worker: Sinopac, workers: list[Sinopac], request_limt: int):
        self.main_worker = main_worker
        self.workers = workers

        # request count
        self.request_count = [int() for _ in range(len(workers))]
        self.lock = threading.RLock()

        # subscribe list
        self.subscribe_count = [int() for _ in range(len(workers))]
        self.sub_lock = threading.Lock()
        self.stock_tick_sub_dict: dict[str, int] = {}
        self.stock_bidask_sub_dict: dict[str, int] = {}
        self.future_tick_sub_dict: dict[str, int] = {}
        self.future_bidask_sub_dict: dict[str, int] = {}

        # request workder limit
        self.request_limit = request_limt
        self.request_worker_timestamp = int()
        self.request_worker_times = int()

    def get_sj_version(self):
        return self.main_worker.get_sj_version()

    def get(self, fetch: bool) -> Sinopac:
        with self.lock:
            now = round(datetime.now().timestamp() * 1000)
            gap = now - self.request_worker_timestamp

            if gap >= 1000:
                self.request_worker_timestamp = now
                self.request_worker_times = 0

            elif fetch is True and self.request_worker_times >= self.request_limit:
                rest_time = 1 - (gap / 1000)
                time.sleep(rest_time)
                return self.get(fetch)

            idx = self.request_count.index(min(self.request_count))
            self.request_count[idx] += 1
            if fetch is True:
                self.request_worker_times += 1

            return self.workers[idx]

    def count(self):
        return len(self.workers)

    def subscribe_stock_tick(self, stock_num):
        with self.sub_lock:
            if stock_num in self.stock_tick_sub_dict:
                return None
            idx = self.subscribe_count.index(min(self.subscribe_count))
            result = self.workers[idx].subscribe_stock_tick(stock_num)
            if result is not None:
                return result
            logger.info(
                "subscribe stock tick %s %s",
                stock_num,
                self.workers[idx].get_contract_name_by_stock_num(stock_num),
            )
            self.subscribe_count[idx] += 1
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
                    self.workers[idx].get_contract_name_by_stock_num(stock_num),
                )
        return None

    def subscribe_future_tick(self, code):
        with self.sub_lock:
            if code in self.future_tick_sub_dict:
                return None
            idx = self.subscribe_count.index(min(self.subscribe_count))
            result = self.workers[idx].subscribe_future_tick(code)
            if result is not None:
                return result
            logger.info(
                "subscribe future tick %s %s",
                code,
                self.workers[idx].get_contract_name_by_future_code(code),
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
                    self.workers[idx].get_contract_name_by_future_code(code),
                )
        return None

    def subscribe_stock_bidask(self, stock_num):
        with self.sub_lock:
            if stock_num in self.stock_bidask_sub_dict:
                return None
            idx = self.subscribe_count.index(min(self.subscribe_count))
            result = self.workers[idx].subscribe_stock_bidask(stock_num)
            if result is not None:
                return result
            logger.info(
                "subscribe stock bidask %s %s",
                stock_num,
                self.workers[idx].get_contract_name_by_stock_num(stock_num),
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
                    self.workers[idx].get_contract_name_by_stock_num(stock_num),
                )
        return None

    def subscribe_future_bidask(self, code):
        with self.sub_lock:
            if code in self.future_bidask_sub_dict:
                return None
            idx = self.subscribe_count.index(min(self.subscribe_count))
            result = self.workers[idx].subscribe_future_bidask(code)
            if result is not None:
                return result
            logger.info(
                "subscribe future bidask %s %s",
                code,
                self.workers[idx].get_contract_name_by_future_code(code),
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
                    self.workers[idx].get_contract_name_by_future_code(code),
                )
        return None

    def unsubscribe_all_tick(self):
        fail_arr: dict[str, list] = {}
        fail_arr["stock"] = []
        fail_arr["future"] = []

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

    def set_order_status_cb(self, func):
        self.main_worker.set_order_status_callback(func)

    def buy_stock(self, stock_num, price, quantity):
        return self.main_worker.buy_stock(stock_num, price, quantity)

    def sell_stock(self, stock_num, price, quantity):
        return self.main_worker.sell_stock(stock_num, price, quantity)

    def sell_first_stock(self, stock_num, price, quantity):
        return self.main_worker.sell_first_stock(stock_num, price, quantity)

    def cancel_stock(self, order_id):
        return self.main_worker.cancel_stock(order_id)

    def get_order_status_by_id(self, order_id):
        return self.main_worker.get_order_status_from_local_by_order_id(order_id)

    def get_order_status_arr(self):
        return self.main_worker.get_order_status()

    def get_non_block_order_status_arr(self):
        return self.main_worker.update_order_status_instant()

    def buy_future(self, code, price, quantity):
        return self.main_worker.buy_future(code, price, quantity)

    def sell_future(self, code, price, quantity):
        return self.main_worker.sell_future(code, price, quantity)

    def sell_first_future(self, code, price, quantity):
        return self.main_worker.sell_first_future(code, price, quantity)

    def cancel_future(self, order_id):
        return self.main_worker.cancel_future(order_id)

    def get_future_position(self):
        return self.main_worker.list_positions()

    def get_stock_num_list(self):
        return self.main_worker.get_stock_num_list()

    def get_future_code_list(self):
        return self.main_worker.get_future_code_list()
