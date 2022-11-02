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

    def get(self, fetch: bool):
        """
        get_worker _summary_

        Returns:
            Sinopac: _description_
        """
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
        """
        count _summary_

        Returns:
            int: _description_
        """
        return len(self.workers)

    def subscribe_stock_tick(self, stock_num):
        """
        subscribe_stock_tick _summary_

        Args:
            stock_num (_type_): _description_

        Returns:
            _type_: _description_
        """
        with self.sub_lock:
            if stock_num in self.stock_tick_sub_dict:
                return None
            idx = self.subscribe_count.index(min(self.subscribe_count))
            result = self.workers[idx].subscribe_stock_tick(stock_num)
            if result is not None:
                return result
            self.subscribe_count[idx] += 1
            self.stock_tick_sub_dict[stock_num] = idx
        return None

    def unsubscribe_stock_tick(self, stock_num):
        """
        unsubscribe_stock_tick _summary_

        Args:
            stock_num (_type_): _description_

        Returns:
            _type_: _description_
        """
        with self.sub_lock:
            if stock_num in self.stock_tick_sub_dict:
                idx = self.stock_tick_sub_dict[stock_num]
                self.subscribe_count[idx] -= 1
                del self.stock_tick_sub_dict[stock_num]
                result = self.workers[idx].unsubscribe_stock_tick(stock_num)
                if result is not None:
                    return result
        return None

    def subscribe_future_tick(self, code):
        """
        subscribe_future_tick _summary_

        Args:
            code (_type_): _description_

        Returns:
            _type_: _description_
        """
        with self.sub_lock:
            if code in self.future_tick_sub_dict:
                return None
            idx = self.subscribe_count.index(min(self.subscribe_count))
            result = self.workers[idx].subscribe_future_tick(code)
            if result is not None:
                return result
            self.subscribe_count[idx] += 1
            self.future_tick_sub_dict[code] = idx
        return None

    def unsubscribe_future_tick(self, code):
        """
        unsubscribe_future_tick _summary_

        Args:
            code (_type_): _description_

        Returns:
            _type_: _description_
        """
        with self.sub_lock:
            if code in self.future_tick_sub_dict:
                idx = self.future_tick_sub_dict[code]
                self.subscribe_count[idx] -= 1
                del self.future_tick_sub_dict[code]
                result = self.workers[idx].unsubscribe_future_tick(code)
                if result is not None:
                    return result
        return None

    def subscribe_stock_bidask(self, stock_num):
        """
        subscribe_stock_bidask _summary_

        Args:
            stock_num (_type_): _description_

        Returns:
            _type_: _description_
        """
        with self.sub_lock:
            if stock_num in self.stock_bidask_sub_dict:
                return None
            idx = self.subscribe_count.index(min(self.subscribe_count))
            result = self.workers[idx].subscribe_stock_bidask(stock_num)
            if result is not None:
                return result
            self.subscribe_count[idx] += 1
            self.stock_bidask_sub_dict[stock_num] = idx
        return None

    def unsubscribe_stock_bidask(self, stock_num):
        """
        unsubscribe_stock_bidask _summary_

        Args:
            stock_num (_type_): _description_

        Returns:
            _type_: _description_
        """
        with self.sub_lock:
            if stock_num in self.stock_bidask_sub_dict:
                idx = self.stock_bidask_sub_dict[stock_num]
                self.subscribe_count[idx] -= 1
                del self.stock_bidask_sub_dict[stock_num]
                result = self.workers[idx].unsubscribe_stock_bidask(stock_num)
                if result is not None:
                    return result
        return None

    def subscribe_future_bidask(self, code):
        with self.sub_lock:
            if code in self.future_bidask_sub_dict:
                return None
            idx = self.subscribe_count.index(min(self.subscribe_count))
            result = self.workers[idx].subscribe_future_bidask(code)
            if result is not None:
                return result
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
        return None

    def unsubscribe_all_tick(self):
        """
        unsubscribe_all_tick _summary_
        """
        fail_arr = []
        if len(self.stock_tick_sub_dict) != 0:
            logger.info("unsubscribe all stock tick")
            for stock_num in list(self.stock_tick_sub_dict):
                if self.unsubscribe_stock_tick(stock_num) is not None:
                    fail_arr.append(stock_num)
        if len(fail_arr) != 0:
            return f"unsubscribe_all_stock_tick fail: {fail_arr}"

        fail_arr = []
        if len(self.future_tick_sub_dict) != 0:
            logger.info("unsubscribe all future tick")
            for code in list(self.future_tick_sub_dict):
                if self.unsubscribe_future_tick(code) is not None:
                    fail_arr.append(code)
        if len(fail_arr) != 0:
            return f"unsubscribe_all_future_tick fail: {fail_arr}"
        return ""

    def unsubscribe_all_bidask(self):
        """
        unsubscribe_all_bidask _summary_
        """
        fail_arr = []
        if len(self.stock_bidask_sub_dict) != 0:
            logger.info("unsubscribe all stock bidask")
            for stock_num in list(self.stock_bidask_sub_dict):
                if self.unsubscribe_stock_bidask(stock_num) is not None:
                    fail_arr.append(stock_num)
        if len(fail_arr) != 0:
            return f"unsubscribe_all_bidask fail: {fail_arr}"

        fail_arr = []
        if len(self.future_bidask_sub_dict) != 0:
            logger.info("unsubscribe all future bidask")
            for code in list(self.future_bidask_sub_dict):
                if self.unsubscribe_future_bidask(code) is not None:
                    fail_arr.append(code)
        if len(fail_arr) != 0:
            return f"unsubscribe_all_future_bidask fail: {fail_arr}"
        return ""

    def set_event_cb(self, func):
        """
        set_event_cb _summary_

        Args:
            func (_type_): _description_
        """
        for worker in self.workers:
            worker.set_event_callback(func)

    def set_stock_quote_cb(self, func):
        """
        set_stock_quote_cb _summary_

        Args:
            func (_type_): _description_
        """
        for worker in self.workers:
            worker.set_on_tick_stk_v1_callback(func)

    def set_future_quote_cb(self, func):
        """
        set_future_quote_cb _summary_

        Args:
            func (_type_): _description_
        """
        for worker in self.workers:
            worker.set_on_tick_fop_v1_callback(func)

    def set_stock_bid_ask_cb(self, func):
        for worker in self.workers:
            worker.set_on_bidask_stk_v1_callback(func)

    def set_future_bid_ask_cb(self, func):
        for worker in self.workers:
            worker.set_on_bidask_fop_v1_callback(func)

    def set_order_status_cb(self, func):
        """
        set_order_status_cb _summary_

        Args:
            func (_type_): _description_
        """
        self.main_worker.set_order_status_callback(func)

    def buy_stock(self, stock_num, price, quantity, sim):
        """
        buy_stock _summary_

        Args:
            stock_num (_type_): _description_
            price (_type_): _description_
            quantity (_type_): _description_
            sim (_type_): _description_
        """
        return self.main_worker.buy_stock(stock_num, price, quantity, sim)

    def sell_stock(self, stock_num, price, quantity, sim):
        """
        sell_stock _summary_

        Args:
            stock_num (_type_): _description_
            price (_type_): _description_
            quantity (_type_): _description_
            sim (_type_): _description_
        """
        return self.main_worker.sell_stock(stock_num, price, quantity, sim)

    def sell_first_stock(self, stock_num, price, quantity, sim):
        """
        sell_first_stock _summary_

        Args:
            stock_num (_type_): _description_
            price (_type_): _description_
            quantity (_type_): _description_
            sim (_type_): _description_
        """
        return self.main_worker.sell_first_stock(stock_num, price, quantity, sim)

    def cancel_stock(self, order_id, sim):
        """
        cancel_stock _summary_

        Args:
            order_id (_type_): _description_
            sim (_type_): _description_
        """
        return self.main_worker.cancel_stock(order_id, sim)

    def get_order_status_by_id(self, order_id, sim):
        """
        get_order_status_by_id _summary_

        Args:
            order_id (_type_): _description_
            sim (_type_): _description_
        """
        return self.main_worker.get_order_status_from_local_by_order_id(order_id, sim)

    def get_order_status_arr(self):
        """
        get_order_status_arr _summary_

        Returns:
            _type_: _description_
        """
        return self.main_worker.get_order_status()

    def get_non_block_order_status_arr(self):
        return self.main_worker.update_order_status_instant()

    def buy_future(self, code, price, quantity, sim):
        return self.main_worker.buy_future(code, price, quantity, sim)

    def sell_future(self, code, price, quantity, sim):
        return self.main_worker.sell_future(code, price, quantity, sim)

    def sell_first_future(self, code, price, quantity, sim):
        return self.main_worker.sell_first_future(code, price, quantity, sim)

    def cancel_future(self, order_id, sim):
        return self.main_worker.cancel_future(order_id, sim)

    def clear_simulation_order(self):
        logger.info("clear all simulation order")
        return self.main_worker.clear_simulation_order()
