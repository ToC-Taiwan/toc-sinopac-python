import threading

from pb.forwarder import history_pb2, history_pb2_grpc
from sinopac import Shioaji
from worker_pool import WorkerPool


class RPCHistory(history_pb2_grpc.HistoryDataInterfaceServicer):
    def __init__(self, workers: WorkerPool):
        self.workers = workers

    def fill_stock_history_tick_response(self, num, date, response, worker: Shioaji):
        ticks = worker.stock_ticks(num, date)
        total_count = len(ticks.ts)
        tmp_length = [
            len(ticks.close),
            len(ticks.tick_type),
            len(ticks.volume),
            len(ticks.bid_price),
            len(ticks.bid_volume),
            len(ticks.ask_price),
            len(ticks.ask_volume),
        ]

        for length in tmp_length:
            if length - total_count != 0:
                return

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
        total_count = len(kbar.ts)
        tmp_length = [
            len(kbar.Close),
            len(kbar.Open),
            len(kbar.High),
            len(kbar.Low),
            len(kbar.Volume),
        ]

        for length in tmp_length:
            if length - total_count != 0:
                return

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

    def GetStockHistoryCloseByDateArr(self, request, _):
        response = history_pb2.HistoryCloseResponse()
        threads = []

        for date in request.date_arr:
            for num in request.stock_num_arr:
                thread = threading.Thread(
                    target=self.fill_stock_history_close_response,
                    args=(
                        num,
                        date,
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

    def GetStockTSEHistoryTick(self, request, _):
        response = history_pb2.HistoryTickResponse()

        thread = threading.Thread(
            target=self.fill_stock_history_tick_response,
            args=(
                "tse_001",
                request.date,
                response,
                self.workers.get_data(),
            ),
            daemon=True,
        )
        thread.start()
        thread.join()
        return response

    def GetStockTSEHistoryKbar(self, request, _):
        response = history_pb2.HistoryKbarResponse()

        thread = threading.Thread(
            target=self.fill_stock_history_kbar_response,
            args=(
                "tse_001",
                request.date,
                response,
                self.workers.get_data(),
            ),
            daemon=True,
        )
        thread.start()
        thread.join()
        return response

    def GetStockTSEHistoryClose(self, request, _):
        response = history_pb2.HistoryCloseResponse()

        thread = threading.Thread(
            target=self.fill_stock_history_close_response,
            args=(
                "tse_001",
                request.date,
                response,
                self.workers.get_data(),
            ),
            daemon=True,
        )
        thread.start()
        thread.join()
        return response

    def fill_future_history_tick_response(self, code, date, response, worker: Shioaji):
        ticks = worker.future_ticks(code, date)
        total_count = len(ticks.ts)
        tmp_length = [
            len(ticks.close),
            len(ticks.tick_type),
            len(ticks.volume),
            len(ticks.bid_price),
            len(ticks.bid_volume),
            len(ticks.ask_price),
            len(ticks.ask_volume),
        ]

        for length in tmp_length:
            if length - total_count != 0:
                return

        for pos in range(total_count):
            response.data.append(
                history_pb2.HistoryTickMessage(
                    code=code,
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

    def GetFutureHistoryTick(self, request, _):
        response = history_pb2.HistoryTickResponse()
        threads = []
        for code in request.future_code_arr:
            thread = threading.Thread(
                target=self.fill_future_history_tick_response,
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

    def fill_future_history_kbar_response(self, code, date, response, sinopac: Shioaji):
        kbar = sinopac.future_kbars(code, date)
        total_count = len(kbar.ts)
        tmp_length = [
            len(kbar.Close),
            len(kbar.Open),
            len(kbar.High),
            len(kbar.Low),
            len(kbar.Volume),
        ]

        for length in tmp_length:
            if length - total_count != 0:
                return

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

    def fill_future_history_close_response(self, code, date, response, sinopac: Shioaji):
        response.data.append(
            history_pb2.HistoryCloseMessage(
                code=code,
                close=sinopac.get_future_last_close_by_date(code, date),
                date=date,
            )
        )

    def GetFutureHistoryClose(self, request, _):
        response = history_pb2.HistoryCloseResponse()
        threads = []

        for code in request.future_code_arr:
            thread = threading.Thread(
                target=self.fill_future_history_close_response,
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
