import threading

import numpy as np
from shioaji.data import Snapshot
from shioaji.error import TokenError

from logger import logger
from pb.forwarder import realtime_pb2, realtime_pb2_grpc
from realtime_us import RealTimeUS
from sinopac import Shioaji
from worker_pool import WorkerPool


class RPCRealTime(realtime_pb2_grpc.RealTimeDataInterfaceServicer):
    def __init__(self, source: RealTimeUS, workers: WorkerPool):
        self.source = source
        self.workers = workers

    def fill_snapshot_arr(self, contracts, snapshots, worker: Shioaji):
        try:
            data = worker.snapshots(contracts)
        except TokenError:
            logger.error("Token Error")
            self.workers.logout_and_exit()

        if data is not None and len(data) > 0:
            snapshots.extend(data)

    def sinopac_snapshot_to_pb(
        self,
        result,
    ) -> realtime_pb2.SnapshotMessage:
        return realtime_pb2.SnapshotMessage(
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
        contracts = []
        worker = self.workers.get()

        for stock in request.stock_num_arr:
            contracts.append(worker.get_contract_by_stock_num(stock))
        splits = np.array_split(contracts, self.workers.count())
        snapshots: list[Snapshot] = []
        threads = []
        for i, split in enumerate(splits):
            threads.append(
                threading.Thread(
                    target=self.fill_snapshot_arr,
                    args=(
                        split,
                        snapshots,
                        self.workers.get_data(),
                    ),
                    daemon=True,
                )
            )
            threads[i].start()
        for thread in threads:
            thread.join()
        response = realtime_pb2.SnapshotResponse()
        for result in snapshots:
            response.data.append(self.sinopac_snapshot_to_pb(result))
        return response

    def GetAllStockSnapshot(self, request, _):
        splits = np.array_split(self.workers.get_stock_contract_list(), self.workers.count())
        snapshots: list[Snapshot] = []
        threads = []
        for i, split in enumerate(splits):
            threads.append(
                threading.Thread(
                    target=self.fill_snapshot_arr,
                    args=(
                        split,
                        snapshots,
                        self.workers.get_data(),
                    ),
                    daemon=True,
                )
            )
            threads[i].start()
        for thread in threads:
            thread.join()
        response = realtime_pb2.SnapshotResponse()
        for result in snapshots:
            response.data.append(self.sinopac_snapshot_to_pb(result))
        return response

    def GetStockSnapshotTSE(self, request, _):
        worker = self.workers.get_data()
        try:
            snapshots = worker.snapshots([worker.get_contract_by_stock_num("tse_001")])
        except TokenError:
            logger.error("token error")
            self.workers.logout_and_exit()
        if snapshots is not None and len(snapshots) > 0:
            return self.sinopac_snapshot_to_pb(snapshots[0])
        return realtime_pb2.SnapshotMessage()

    def GetStockSnapshotOTC(self, request, _):
        worker = self.workers.get_data()
        try:
            snapshots = worker.snapshots([worker.get_contract_by_stock_num("otc_101")])
        except TokenError:
            logger.error("token error")
            self.workers.logout_and_exit()
        if snapshots is not None and len(snapshots) > 0:
            return self.sinopac_snapshot_to_pb(snapshots[0])
        return realtime_pb2.SnapshotMessage()

    def GetStockVolumeRank(self, request, _):
        response = realtime_pb2.StockVolumeRankResponse()
        ranks = self.workers.get().get_stock_volume_rank_by_date(request.count, request.date)
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
        contracts = []
        worker = self.workers.get()

        for code in request.future_code_arr:
            contracts.append(worker.get_contract_by_future_code(code))
        splits = np.array_split(contracts, self.workers.count())
        snapshots: list[Snapshot] = []
        threads = []
        for i, split in enumerate(splits):
            threads.append(
                threading.Thread(
                    target=self.fill_snapshot_arr,
                    args=(
                        split,
                        snapshots,
                        self.workers.get_data(),
                    ),
                    daemon=True,
                )
            )
            threads[i].start()
        for thread in threads:
            thread.join()
        response = realtime_pb2.SnapshotResponse()
        for result in snapshots:
            response.data.append(self.sinopac_snapshot_to_pb(result))
        return response
