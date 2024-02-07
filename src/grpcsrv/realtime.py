import threading

import numpy as np

from pb.forwarder import realtime_pb2, realtime_pb2_grpc
from realtime_us import RealTimeUS
from sinopac import Shioaji
from worker_pool import WorkerPool


class RPCRealTime(realtime_pb2_grpc.RealTimeDataInterfaceServicer):
    def __init__(self, source: RealTimeUS, workers: WorkerPool):
        self.source = source
        self.workers = workers

    def fill_snapshot_arr(
        self,
        contracts,
        response: realtime_pb2.SnapshotResponse,
        worker: Shioaji,
    ):
        data = worker.snapshots(contracts)
        if data is None or len(data) == 0:
            return

        for result in data:
            response.data.append(
                realtime_pb2.SnapshotMessage(
                    ts=result.ts,
                    code=result.code,
                    exchange=result.exchange,
                    open=result.open,
                    high=result.high,
                    low=result.low,
                    close=result.close,
                    tick_type=result.tick_type,
                    change_price=result.change_price,
                    change_rate=result.change_rate,
                    change_type=result.change_type,
                    average_price=result.average_price,
                    volume=result.volume,
                    total_volume=result.total_volume,
                    amount=result.amount,
                    total_amount=result.total_amount,
                    yesterday_volume=result.yesterday_volume,
                    buy_price=result.buy_price,
                    buy_volume=result.buy_volume,
                    sell_price=result.sell_price,
                    sell_volume=result.sell_volume,
                    volume_ratio=result.volume_ratio,
                )
            )

    def GetNasdaq(self, request, _):
        arr = self.source.get_nasdaq()
        return realtime_pb2.YahooFinancePrice(
            price=arr[0],
            last=arr[1],
        )

    def GetNasdaqFuture(self, request, _):
        arr = self.source.get_nasdaq_future()
        return realtime_pb2.YahooFinancePrice(
            price=arr[0],
            last=arr[1],
        )

    def GetStockSnapshotByNumArr(self, request, _):
        contracts = self.workers.get_contract_by_stock_num_arr(request.stock_num_arr)
        splits = np.array_split(contracts, self.workers.count())
        response = realtime_pb2.SnapshotResponse()
        threads = []
        for i, split in enumerate(splits):
            threads.append(
                threading.Thread(
                    target=self.fill_snapshot_arr,
                    args=(
                        split,
                        response,
                        self.workers.get_data(),
                    ),
                    daemon=True,
                )
            )
            threads[i].start()
        for thread in threads:
            thread.join()
        return response

    def GetAllStockSnapshot(self, request, _):
        splits = np.array_split(self.workers.get_stock_contract_list(), self.workers.count())
        response = realtime_pb2.SnapshotResponse()
        threads = []
        for i, split in enumerate(splits):
            threads.append(
                threading.Thread(
                    target=self.fill_snapshot_arr,
                    args=(
                        split,
                        response,
                        self.workers.get_data(),
                    ),
                    daemon=True,
                )
            )
            threads[i].start()
        for thread in threads:
            thread.join()
        return response

    def GetStockSnapshotTSE(self, request, _):
        response = realtime_pb2.SnapshotResponse()
        self.fill_snapshot_arr([self.workers.get_tse_001_contract()], response, self.workers.get_data())
        return response

    def GetStockSnapshotOTC(self, request, _):
        response = realtime_pb2.SnapshotResponse()
        self.fill_snapshot_arr([self.workers.get_otc_101_contract()], response, self.workers.get_data())
        return response

    def GetStockVolumeRank(self, request, _):
        response = realtime_pb2.StockVolumeRankResponse()
        ranks = self.workers.get_data().get_stock_volume_rank_by_date(request.count, request.date)
        for result in ranks:
            response.data.append(
                realtime_pb2.StockVolumeRankMessage(
                    date=result.date,
                    code=result.code,
                    name=result.name,
                    ts=result.ts,
                    open=result.open,
                    high=result.high,
                    low=result.low,
                    close=result.close,
                    price_range=result.price_range,
                    tick_type=result.tick_type,
                    change_price=result.change_price,
                    change_type=result.change_type,
                    average_price=result.average_price,
                    volume=result.volume,
                    total_volume=result.total_volume,
                    amount=result.amount,
                    total_amount=result.total_amount,
                    yesterday_volume=result.yesterday_volume,
                    volume_ratio=result.volume_ratio,
                    buy_price=result.buy_price,
                    buy_volume=result.buy_volume,
                    sell_price=result.sell_price,
                    sell_volume=result.sell_volume,
                    bid_orders=result.bid_orders,
                    bid_volumes=result.bid_volumes,
                    ask_orders=result.ask_orders,
                    ask_volumes=result.ask_volumes,
                )
            )
        return response

    def GetFutureSnapshotByCodeArr(self, request, _):
        contracts = self.workers.get_contract_by_future_code_arr(request.future_code_arr)
        splits = np.array_split(contracts, self.workers.count())
        response = realtime_pb2.SnapshotResponse()
        threads = []
        for i, split in enumerate(splits):
            threads.append(
                threading.Thread(
                    target=self.fill_snapshot_arr,
                    args=(
                        split,
                        response,
                        self.workers.get_data(),
                    ),
                    daemon=True,
                )
            )
            threads[i].start()
        for thread in threads:
            thread.join()
        return response
