import threading
import typing

from sinopac import Sinopac


class SinopacWorker():
    def __init__(self, main_worker: Sinopac, workers: typing.List[Sinopac]):
        self.main_worker = main_worker
        self.workers = workers
        # request count
        self.request_count = [int() for _ in range(len(workers))]
        self.lock = threading.Lock()
        # subscribe list
        self.subscribe_count = [int() for _ in range(len(workers))]
        self.sub_lock = threading.Lock()
        self.stock_tick_sub_dict: typing.Dict[str, int] = {}
        self.stock_bidask_sub_dict: typing.Dict[str, int] = {}

    def get_main(self):
        '''
        get_main _summary_

        Returns:
            Sinopac: _description_
        '''
        return self.main_worker

    def get(self):
        '''
        get_worker _summary_

        Returns:
            Sinopac: _description_
        '''
        with self.lock:
            idx = self.request_count.index(min(self.request_count))
            self.request_count[idx] += 1
            return self.workers[idx]

    def count(self):
        '''
        count _summary_

        Returns:
            int: _description_
        '''
        return len(self.workers)

    def subscribe_stock_tick(self, stock_num):
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
        with self.sub_lock:
            if stock_num in self.stock_tick_sub_dict:
                idx = self.stock_tick_sub_dict[stock_num]
                self.subscribe_count[idx] -= 1
                del self.stock_tick_sub_dict[stock_num]
                result = self.workers[idx].unsubscribe_stock_tick(stock_num)
                if result is not None:
                    return result
        return None

    def subscribe_stock_bidask(self, stock_num):
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
        with self.sub_lock:
            if stock_num in self.stock_bidask_sub_dict:
                idx = self.stock_bidask_sub_dict[stock_num]
                self.subscribe_count[idx] -= 1
                del self.stock_bidask_sub_dict[stock_num]
                result = self.workers[idx].unsubscribe_stock_bidask(stock_num)
                if result is not None:
                    return result
        return None

    def unsubscribe_all(self):
        for stock_num in self.stock_tick_sub_dict:
            self.unsubscribe_stock_tick(stock_num)
        for stock_num in self.stock_bidask_sub_dict:
            self.unsubscribe_stock_bidask(stock_num)
