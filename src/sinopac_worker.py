import threading

from logger import logger
from sinopac import Sinopac


class SinopacWorker:
    def __init__(self, main_worker: Sinopac, workers: list[Sinopac]):
        self.main_worker = main_worker
        self.workers = workers
        # request count
        self.request_count = [int() for _ in range(len(workers))]
        self.lock = threading.Lock()
        # subscribe list
        self.subscribe_count = [int() for _ in range(len(workers))]
        self.sub_lock = threading.Lock()
        self.stock_tick_sub_dict: dict[str, int] = {}
        self.stock_bidask_sub_dict: dict[str, int] = {}

    def get_main(self):
        """
        get_main _summary_

        Returns:
            Sinopac: _description_
        """
        return self.main_worker

    def get(self):
        """
        get_worker _summary_

        Returns:
            Sinopac: _description_
        """
        with self.lock:
            idx = self.request_count.index(min(self.request_count))
            self.request_count[idx] += 1
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
            logger.info("subscribe_stock_tick: %s", stock_num)
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
                logger.info("unsubscribe_stock_tick: %s", stock_num)
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
            logger.info("subscribe_stock_bidask: %s", stock_num)
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
                logger.info("unsubscribe_stock_bidask: %s", stock_num)
        return None

    def unsubscribe_all_tick(self):
        """
        unsubscribe_all_tick _summary_
        """
        if len(self.stock_tick_sub_dict) != 0:
            logger.info("unsubscribe all tick")
            for stock_num in list(self.stock_tick_sub_dict):
                self.unsubscribe_stock_tick(stock_num)

    def unsubscribe_all_bidask(self):
        """
        unsubscribe_all_bidask _summary_
        """
        if len(self.stock_bidask_sub_dict) != 0:
            logger.info("unsubscribe all bidask")
            for stock_num in list(self.stock_bidask_sub_dict):
                self.unsubscribe_stock_bidask(stock_num)

    def set_event_cb(self, func):
        """
        set_event_cb _summary_

        Args:
            func (_type_): _description_
        """
        for worker in self.workers:
            worker.set_event_callback(func)

    def set_quote_cb(self, func):
        """
        set_quote_cb _summary_

        Args:
            func (_type_): _description_
        """
        for worker in self.workers:
            worker.set_on_tick_stk_v1_callback(func)

    def set_bid_ask_cb(self, func):
        """
        set_bid_ask_cb _summary_

        Args:
            func (_type_): _description_
        """
        for worker in self.workers:
            worker.set_on_bidask_stk_v1_callback(func)

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
        try:
            self.main_worker.update_order_status_instant()
            return ""
        except Exception:  # pylint: disable=broad-except
            return "update_order_status_instant fail"
