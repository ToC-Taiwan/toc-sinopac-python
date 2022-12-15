import os
import threading
import time
from concurrent import futures
from datetime import datetime
from queue import Queue

import basic_pb2
import basic_pb2_grpc
import common_pb2
import google.protobuf.empty_pb2
import grpc
import health_pb2
import health_pb2_grpc
import history_pb2
import history_pb2_grpc
import numpy as np
import stream_pb2
import stream_pb2_grpc
import trade_pb2
import trade_pb2_grpc
from shioaji.data import Snapshot
from shioaji.error import TokenError

from env import RequiredEnv
from logger import logger
from rabbitmq import RabbitMQS
from simulator import Simulator
from sinopac import Sinopac
from sinopac_worker import SinopacWorkerPool
from yahoo_finance import Yahoo

WORKERS: SinopacWorkerPool


class gRPCHealthCheck(health_pb2_grpc.HealthCheckInterfaceServicer):
    def __init__(self, simulator: Simulator):
        self.beat_time = float()
        self.debug = False
        self.simulator = simulator

    def Heartbeat(self, request_iterator, _):
        logger.info("new grpc client connected")
        self.beat_queue: Queue = Queue()
        threading.Thread(target=self.beat_timer).start()
        for beat in request_iterator:
            self.beat_time = datetime.now().timestamp()
            self.beat_queue.put(beat.message)
            if beat.message == "debug":
                self.debug = True
            else:
                self.debug = False
            yield health_pb2.BeatMessage(message=beat.message)

    def beat_timer(self):
        self.beat_time = datetime.now().timestamp()
        while True:
            if datetime.now().timestamp() > self.beat_time + 10:
                logger.info("grpc client disconnected")
                if self.debug is True:
                    WORKERS.unsubscribe_all_tick()
                    WORKERS.unsubscribe_all_bidask()
                    self.simulator.reset_simulator()
                    return
                os._exit(1)
            if self.beat_queue.empty():
                time.sleep(1)
                continue
            self.beat_queue.get()

    def Terminate(self, request, _):
        threading.Thread(target=self.wait_and_terminate).start()
        return google.protobuf.empty_pb2.Empty()  # pylint: disable=no-member

    def wait_and_terminate(self):
        time.sleep(3)
        os._exit(1)


class gRPCBasic(basic_pb2_grpc.BasicDataInterfaceServicer):
    def GetAllStockDetail(self, request, _):
        response = basic_pb2.StockDetailResponse()
        worker = WORKERS.get(False)

        tse_001 = worker.get_contract_tse_001()
        response.stock.append(
            basic_pb2.StockDetailMessage(
                exchange=tse_001.exchange,
                category=tse_001.category,
                code=tse_001.code,
                name=tse_001.name,
                reference=tse_001.reference,
                update_date=tse_001.update_date,
                day_trade=tse_001.day_trade,
            )
        )
        for row in WORKERS.get_stock_num_list():
            contract = worker.get_contract_by_stock_num(row)
            if contract is None:
                logger.error("%s has no stock data", row)
                continue
            response.stock.append(
                basic_pb2.StockDetailMessage(
                    exchange=contract.exchange,
                    category=contract.category,
                    code=contract.code,
                    name=contract.name,
                    reference=contract.reference,
                    update_date=contract.update_date,
                    day_trade=contract.day_trade,
                )
            )
        return response

    def GetAllFutureDetail(self, request, _):
        response = basic_pb2.FutureDetailResponse()
        worker = WORKERS.get(False)

        for row in WORKERS.get_future_code_list():
            contract = worker.get_contract_by_future_code(row)
            if contract is None:
                logger.error("%s has no future data", row)
                continue
            response.future.append(
                basic_pb2.FutureDetailMessage(
                    code=contract.code,
                    symbol=contract.symbol,
                    name=contract.name,
                    category=contract.category,
                    delivery_month=contract.delivery_month,
                    delivery_date=contract.delivery_date,
                    underlying_kind=contract.underlying_kind,
                    unit=contract.unit,
                    limit_up=contract.limit_up,
                    limit_down=contract.limit_down,
                    reference=contract.reference,
                    update_date=contract.update_date,
                )
            )
        return response


class gRPCHistory(history_pb2_grpc.HistoryDataInterfaceServicer):
    def GetStockHistoryTick(self, request, _):
        response = history_pb2.HistoryTickResponse()
        threads = []
        for num in request.stock_num_arr:
            t = threading.Thread(
                target=fill_stock_history_tick_response,
                args=(
                    num,
                    request.date,
                    response,
                    WORKERS.get(True),
                ),
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return response

    def GetStockHistoryKbar(self, request, _):
        response = history_pb2.HistoryKbarResponse()
        threads = []

        for num in request.stock_num_arr:
            t = threading.Thread(
                target=fill_stock_history_kbar_response,
                args=(
                    num,
                    request.date,
                    response,
                    WORKERS.get(True),
                ),
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return response

    def GetStockHistoryClose(self, request, _):
        response = history_pb2.HistoryCloseResponse()
        threads = []

        for num in request.stock_num_arr:
            t = threading.Thread(
                target=fill_stock_history_close_response,
                args=(
                    num,
                    request.date,
                    response,
                    WORKERS.get(True),
                ),
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return response

    def GetStockHistoryCloseByDateArr(self, request, _):
        response = history_pb2.HistoryCloseResponse()
        threads = []

        for date in request.date_arr:
            for num in request.stock_num_arr:
                t = threading.Thread(
                    target=fill_stock_history_close_response,
                    args=(
                        num,
                        date,
                        response,
                        WORKERS.get(True),
                    ),
                )
                threads.append(t)
                t.start()
        for t in threads:
            t.join()
        return response

    def GetStockTSEHistoryTick(self, request, _):
        response = history_pb2.HistoryTickResponse()

        t = threading.Thread(
            target=fill_stock_history_tick_response,
            args=(
                "tse_001",
                request.date,
                response,
                WORKERS.get(True),
            ),
        )
        t.start()
        t.join()
        return response

    def GetStockTSEHistoryKbar(self, request, _):
        response = history_pb2.HistoryKbarResponse()

        t = threading.Thread(
            target=fill_stock_history_kbar_response,
            args=(
                "tse_001",
                request.date,
                response,
                WORKERS.get(True),
            ),
        )
        t.start()
        t.join()
        return response

    def GetStockTSEHistoryClose(self, request, _):
        response = history_pb2.HistoryCloseResponse()

        t = threading.Thread(
            target=fill_stock_history_close_response,
            args=(
                "tse_001",
                request.date,
                response,
                WORKERS.get(True),
            ),
        )
        t.start()
        t.join()
        return response

    def GetOTCHistoryKbar(self, request, _):
        response = history_pb2.HistoryKbarResponse()

        t = threading.Thread(
            target=fill_stock_history_kbar_response,
            args=(
                "otc_101",
                request.date,
                response,
                WORKERS.get(True),
            ),
        )
        t.start()
        t.join()
        return response

    def GetFutureHistoryTick(self, request, _):
        response = history_pb2.HistoryTickResponse()
        threads = []
        for code in request.future_code_arr:
            t = threading.Thread(
                target=fill_future_history_tick_response,
                args=(
                    code,
                    request.date,
                    response,
                    WORKERS.get(True),
                ),
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return response

    def GetFutureHistoryKbar(self, request, _):
        response = history_pb2.HistoryKbarResponse()
        threads = []

        for code in request.future_code_arr:
            t = threading.Thread(
                target=fill_future_history_kbar_response,
                args=(
                    code,
                    request.date,
                    response,
                    WORKERS.get(True),
                ),
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return response

    def GetFutureHistoryClose(self, request, _):
        response = history_pb2.HistoryCloseResponse()
        threads = []

        for code in request.future_code_arr:
            t = threading.Thread(
                target=fill_future_history_close_response,
                args=(
                    code,
                    request.date,
                    response,
                    WORKERS.get(True),
                ),
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return response


class gRPCTrade(trade_pb2_grpc.TradeInterfaceServicer):
    def __init__(self, rq: RabbitMQS, simulator: Simulator):
        self.rq = rq
        self.simulator = simulator
        self.send_order_lock = threading.Lock()

    def GetFuturePosition(self, request, _):
        response = trade_pb2.FuturePositionArr()
        result = WORKERS.get_future_position()
        if len(result) > 0:
            for x in result:
                response.position_arr.append(
                    trade_pb2.FuturePosition(
                        code=x.code,
                        direction=x.direction,
                        quantity=x.quantity,
                        price=x.price,
                        last_price=x.last_price,
                        pnl=x.pnl,
                    )
                )
        return response

    def BuyStock(self, request, _):
        result = None
        if request.simulate is not True:
            result = WORKERS.buy_stock(
                request.stock_num, request.price, request.quantity
            )
        else:
            result = self.simulator.buy_stock(
                request.stock_num, request.price, request.quantity
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def SellStock(self, request, _):
        result = None
        if request.simulate is not True:
            result = WORKERS.sell_stock(
                request.stock_num, request.price, request.quantity
            )
        else:
            result = self.simulator.sell_stock(
                request.stock_num, request.price, request.quantity
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def SellFirstStock(self, request, _):
        result = None
        if request.simulate is not True:
            result = WORKERS.sell_first_stock(
                request.stock_num, request.price, request.quantity
            )
        else:
            result = self.simulator.sell_first_stock(
                request.stock_num, request.price, request.quantity
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def CancelStock(self, request, _):
        result = None
        if request.simulate is not True:
            result = WORKERS.cancel_stock(request.order_id)
        else:
            result = self.simulator.cancel_stock(request.order_id)
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def GetOrderStatusByID(self, request, _):
        result = None
        if request.simulate is not True:
            result = WORKERS.get_order_status_by_id(request.order_id)
        else:
            result = self.simulator.get_order_status_by_id(request.order_id)
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def GetLocalOrderStatusArr(self, request, _):
        with self.send_order_lock:
            self.rq.send_order_arr(WORKERS.get_order_status_arr())
            return google.protobuf.empty_pb2.Empty()  # pylint: disable=no-member

    def GetSimulateOrderStatusArr(self, request, _):
        with self.send_order_lock:
            self.rq.send_order_arr(self.simulator.get_order_status())
            return google.protobuf.empty_pb2.Empty()  # pylint: disable=no-member

    def GetNonBlockOrderStatusArr(self, request, _):
        return common_pb2.ErrorMessage(err=WORKERS.get_non_block_order_status_arr())

    def BuyFuture(self, request, _):
        result = None
        if request.simulate is not True:
            result = WORKERS.buy_future(
                request.code,
                request.price,
                request.quantity,
            )
        else:
            result = self.simulator.buy_future(
                request.code,
                request.price,
                request.quantity,
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def SellFuture(self, request, _):
        result = None
        if request.simulate is not True:
            result = WORKERS.sell_future(
                request.code,
                request.price,
                request.quantity,
            )
        else:
            result = self.simulator.sell_future(
                request.code,
                request.price,
                request.quantity,
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def SellFirstFuture(self, request, _):
        result = None
        if request.simulate is not True:
            result = WORKERS.sell_first_future(
                request.code,
                request.price,
                request.quantity,
            )
        else:
            result = self.simulator.sell_first_future(
                request.code,
                request.price,
                request.quantity,
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def CancelFuture(self, request, _):
        result = None
        if request.simulate is not True:
            result = WORKERS.cancel_future(
                request.order_id,
            )
        else:
            result = self.simulator.cancel_future(
                request.order_id,
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )


class gRPCStream(stream_pb2_grpc.StreamDataInterfaceServicer):
    def __init__(self, source: Yahoo):
        self.source = source

    def GetNasdaq(self, request, _):
        arr = self.source.get_nasdaq()
        return stream_pb2.YahooFinancePrice(
            price=arr[0],
            last=arr[1],
        )

    def GetNasdaqFuture(self, request, _):
        arr = self.source.get_nasdaq_future()
        return stream_pb2.YahooFinancePrice(
            price=arr[0],
            last=arr[1],
        )

    def GetStockSnapshotByNumArr(self, request, _):
        contracts = []
        worker = WORKERS.get(False)

        for stock in request.stock_num_arr:
            contracts.append(worker.get_contract_by_stock_num(stock))
        splits = np.array_split(contracts, WORKERS.count())
        snapshots: list[Snapshot] = []
        threads = []
        for i, split in enumerate(splits):
            threads.append(
                threading.Thread(
                    target=fill_snapshot_arr,
                    args=(split, snapshots, WORKERS.get(True)),
                )
            )
            threads[i].start()
        for t in threads:
            t.join()
        response = stream_pb2.SnapshotResponse()
        for result in snapshots:
            response.data.append(sinopac_snapshot_to_pb(result))
        return response

    def GetAllStockSnapshot(self, request, _):
        contracts = []
        worker = WORKERS.get(False)

        for stock in WORKERS.get_stock_num_list():
            contracts.append(worker.get_contract_by_stock_num(stock))
        splits = np.array_split(contracts, WORKERS.count())
        snapshots: list[Snapshot] = []
        threads = []
        for i, split in enumerate(splits):
            threads.append(
                threading.Thread(
                    target=fill_snapshot_arr,
                    args=(split, snapshots, WORKERS.get(True)),
                )
            )
            threads[i].start()
        for t in threads:
            t.join()
        response = stream_pb2.SnapshotResponse()
        for result in snapshots:
            response.data.append(sinopac_snapshot_to_pb(result))
        return response

    def GetStockSnapshotTSE(self, request, _):
        worker = WORKERS.get(True)
        try:
            snapshots = worker.snapshots([worker.get_contract_tse_001()])
        except TokenError:
            logger.error("token error")
            os._exit(1)
        return sinopac_snapshot_to_pb(snapshots[0])

    def GetStockSnapshotOTC(self, request, _):
        worker = WORKERS.get(True)
        try:
            snapshots = worker.snapshots([worker.get_contract_otc_101()])
        except TokenError:
            logger.error("token error")
            os._exit(1)
        return sinopac_snapshot_to_pb(snapshots[0])

    def GetStockVolumeRank(self, request, _):
        response = stream_pb2.StockVolumeRankResponse()
        ranks = WORKERS.get(True).get_stock_volume_rank_by_date(
            request.count, request.date
        )
        for result in ranks:
            response.data.append(
                stream_pb2.StockVolumeRankMessage(
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

    def SubscribeStockTick(self, request, _):
        response = stream_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = WORKERS.subscribe_stock_tick(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def UnSubscribeStockTick(self, request, _):
        response = stream_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = WORKERS.unsubscribe_stock_tick(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def SubscribeStockBidAsk(self, request, _):
        response = stream_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = WORKERS.subscribe_stock_bidask(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def UnSubscribeStockBidAsk(self, request, _):
        response = stream_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = WORKERS.unsubscribe_stock_bidask(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def SubscribeFutureTick(self, request, _):
        response = stream_pb2.SubscribeResponse()
        for code in request.future_code_arr:
            result = WORKERS.subscribe_future_tick(code)
            if result is not None:
                response.fail_arr.append(code)
        return response

    def UnSubscribeFutureTick(self, request, _):
        response = stream_pb2.SubscribeResponse()
        for code in request.future_code_arr:
            result = WORKERS.unsubscribe_future_tick(code)
            if result is not None:
                response.fail_arr.append(code)
        return response

    def SubscribeFutureBidAsk(self, request, _):
        response = stream_pb2.SubscribeResponse()
        for code in request.future_code_arr:
            result = WORKERS.subscribe_future_bidask(code)
            if result is not None:
                response.fail_arr.append(code)
        return response

    def UnSubscribeFutureBidAsk(self, request, _):
        response = stream_pb2.SubscribeResponse()
        for code in request.future_code_arr:
            result = WORKERS.unsubscribe_future_bidask(code)
            if result is not None:
                response.fail_arr.append(code)
        return response

    def UnSubscribeStockAllTick(self, request, _):
        return common_pb2.ErrorMessage(err=WORKERS.unsubscribe_all_tick())

    def UnSubscribeStockAllBidAsk(self, request, _):
        return common_pb2.ErrorMessage(err=WORKERS.unsubscribe_all_bidask())

    def GetFutureSnapshotByCodeArr(self, request, _):
        contracts = []
        worker = WORKERS.get(False)

        for code in request.future_code_arr:
            contracts.append(worker.get_contract_by_future_code(code))
        splits = np.array_split(contracts, WORKERS.count())
        snapshots: list[Snapshot] = []
        threads = []
        for i, split in enumerate(splits):
            threads.append(
                threading.Thread(
                    target=fill_snapshot_arr,
                    args=(split, snapshots, WORKERS.get(True)),
                )
            )
            threads[i].start()
        for t in threads:
            t.join()
        response = stream_pb2.SnapshotResponse()
        for result in snapshots:
            response.data.append(sinopac_snapshot_to_pb(result))
        return response


def sinopac_snapshot_to_pb(result) -> stream_pb2.SnapshotMessage:
    return stream_pb2.SnapshotMessage(
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


def fill_snapshot_arr(contracts, snapshots, worker: Sinopac):
    try:
        data = worker.snapshots(contracts)
    except TokenError:
        logger.error("Token Error")
        os._exit(1)

    if data is not None:
        snapshots.extend(data)


def fill_stock_history_tick_response(num, date, response, worker: Sinopac):
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


def fill_future_history_tick_response(code, date, response, worker: Sinopac):
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


def fill_stock_history_kbar_response(num, date, response, worker: Sinopac):
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


def fill_future_history_kbar_response(code, date, response, sinopac: Sinopac):
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


def fill_stock_history_close_response(num, date, response, sinopac: Sinopac):
    response.data.append(
        history_pb2.HistoryCloseMessage(
            code=num,
            close=sinopac.get_stock_last_close_by_date(num, date),
            date=date,
        )
    )


def fill_future_history_close_response(code, date, response, sinopac: Sinopac):
    response.data.append(
        history_pb2.HistoryCloseMessage(
            code=code,
            close=sinopac.get_future_last_close_by_date(code, date),
            date=date,
        )
    )


def serve(port: str, main_worker: Sinopac, workers: list[Sinopac], cfg: RequiredEnv):
    global WORKERS  # pylint: disable=global-statement
    WORKERS = SinopacWorkerPool(main_worker, workers, cfg.request_limit_per_second)

    # set call back
    rq = RabbitMQS(
        str(cfg.rabbitmq_url),
        str(cfg.rabbitmq_exchange),
        128,
    )

    # simulator
    simulator = Simulator(WORKERS.main_worker)

    # gRPC servicer
    health_servicer = gRPCHealthCheck(simulator=simulator)
    basic_servicer = gRPCBasic()
    history_servicer = gRPCHistory()
    trade_servicer = gRPCTrade(rq=rq, simulator=simulator)
    stream_servicer = gRPCStream(source=Yahoo())

    WORKERS.set_event_cb(rq.event_callback)
    WORKERS.set_stock_quote_cb(rq.stock_quote_callback_v1)
    WORKERS.set_future_quote_cb(rq.future_quote_callback_v1)
    WORKERS.set_stock_bid_ask_cb(rq.stock_bid_ask_callback)
    WORKERS.set_future_bid_ask_cb(rq.future_bid_ask_callback)
    WORKERS.set_order_status_cb(rq.order_status_callback)

    server = grpc.server(
        futures.ThreadPoolExecutor(),
        options=[
            ("grpc.max_send_message_length", 1024 * 1024 * 1024),
            ("grpc.max_receive_message_length", 1024 * 1024 * 1024),
        ],
    )
    health_pb2_grpc.add_HealthCheckInterfaceServicer_to_server(health_servicer, server)
    basic_pb2_grpc.add_BasicDataInterfaceServicer_to_server(basic_servicer, server)
    history_pb2_grpc.add_HistoryDataInterfaceServicer_to_server(
        history_servicer, server
    )
    trade_pb2_grpc.add_TradeInterfaceServicer_to_server(trade_servicer, server)
    stream_pb2_grpc.add_StreamDataInterfaceServicer_to_server(stream_servicer, server)

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info("shioaji version: %s", WORKERS.get_sj_version())
    logger.info("gRPC Server started at port %s", port)
    server.wait_for_termination()
