import threading
import typing

from sinopac import Sinopac


class SinopacWorker():
    def __init__(self, main_worker: Sinopac, workers: typing.List[Sinopac]):
        self.main_worker = main_worker
        self.workers = workers
        self.request_count = [int() for _ in range(len(workers))]
        self.lock = threading.Lock()

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
