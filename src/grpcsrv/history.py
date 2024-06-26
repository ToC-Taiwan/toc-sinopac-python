import threading

from toc_trade_pb.forwarder import history_pb2, history_pb2_grpc

from sinopac import Shioaji
from worker_pool import WorkerPool


class RPCHistory(history_pb2_grpc.HistoryDataInterfaceServicer):
    def __init__(self, workers: WorkerPool):
        self.workers = workers

    def fill_stock_history_tick_response(self, num, date, response, worker: Shioaji):
        ticks = worker.stock_ticks(num, date)
        if ticks is None or len(ticks.ts) == 0:
            return

        total_count = len(ticks.ts)
        for pos in range(total_count):
            response.data.append(
                history_pb2.HistoryTickMessage(
                    code=num,
                    ts=ticks.ts[pos],
                    close=ticks.close[pos],
                    volume=ticks.volume[pos],
                    bid_price=ticks.bid_price[pos],
                    bid_volume=ticks.bid_volume[pos],
                    ask_price=ticks.ask_price[pos],
                    ask_volume=ticks.ask_volume[pos],
                    tick_type=ticks.tick_type[pos],
                )
            )

    def GetStockHistoryTick(self, request, _):
        response = history_pb2.HistoryTickResponse()
        threads = []
        for num in request.stock_num_arr:
            thread = threading.Thread(
                target=self.fill_stock_history_tick_response,
                args=(
                    num,
                    request.date,
                    response,
                    self.workers.get_data(),
                ),
                daemon=True,
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return response

    def fill_stock_history_kbar_response(self, num, date, response, worker: Shioaji):
        kbar = worker.stock_kbars(num, date)
        if kbar is None or len(kbar.ts) == 0:
            return

        total_count = len(kbar.ts)
        for pos in range(total_count):
            response.data.append(
                history_pb2.HistoryKbarMessage(
                    code=num,
                    ts=kbar.ts[pos],
                    close=kbar.Close[pos],
                    open=kbar.Open[pos],
                    high=kbar.High[pos],
                    low=kbar.Low[pos],
                    volume=kbar.Volume[pos],
                )
            )

    def GetStockHistoryKbar(self, request, _):
        response = history_pb2.HistoryKbarResponse()
        threads = []

        for num in request.stock_num_arr:
            thread = threading.Thread(
                target=self.fill_stock_history_kbar_response,
                args=(
                    num,
                    request.date,
                    response,
                    self.workers.get_data(),
                ),
                daemon=True,
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return response

    def fill_stock_history_close_response(self, num, date, response, sinopac: Shioaji):
        response.data.append(
            history_pb2.HistoryCloseMessage(
                code=num,
                close=sinopac.get_stock_last_close_by_date(num, date),
                date=date,
            )
        )

    def GetStockHistoryClose(self, request, _):
        response = history_pb2.HistoryCloseResponse()
        threads = []

        for num in request.stock_num_arr:
            thread = threading.Thread(
                target=self.fill_stock_history_close_response,
                args=(
                    num,
                    request.date,
                    response,
                    self.workers.get_data(),
                ),
                daemon=True,
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return response

    def fill_future_history_kbar_response(
        self,
        code: str,
        date,
        response: history_pb2.HistoryKbarResponse,
        sinopac: Shioaji,
    ):
        kbar = sinopac.future_kbars(code, date)
        if kbar is None or len(kbar.ts) == 0:
            return

        total_count = len(kbar.ts)
        for pos in range(total_count):
            response.data.append(
                history_pb2.HistoryKbarMessage(
                    code=code,
                    ts=kbar.ts[pos],
                    close=kbar.Close[pos],
                    open=kbar.Open[pos],
                    high=kbar.High[pos],
                    low=kbar.Low[pos],
                    volume=kbar.Volume[pos],
                )
            )

    def GetFutureHistoryKbar(self, request, _):
        response = history_pb2.HistoryKbarResponse()
        threads = []

        for code in request.future_code_arr:
            thread = threading.Thread(
                target=self.fill_future_history_kbar_response,
                args=(
                    code,
                    request.date,
                    response,
                    self.workers.get_data(),
                ),
                daemon=True,
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return response
