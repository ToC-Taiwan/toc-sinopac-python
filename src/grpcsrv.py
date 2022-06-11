import random
import string
import threading
from concurrent import futures
from datetime import datetime

import grpc
import numpy as np

import sinopac_forwarder_pb2
import sinopac_forwarder_pb2_grpc
from env import RequiredEnv
from logger import logger
from rabbitmq import RabbitMQS
from sinopac import Sinopac
from sinopac_worker import SinopacWorker

SERVER_TOKEN = "".join(random.choice(string.ascii_letters) for _ in range(50))
WORKERS: SinopacWorker


class gRPCSinopacForwarder(sinopac_forwarder_pb2_grpc.SinopacForwarderServicer):
    def GetServerToken(self, request, _):
        """
        HealthCheck _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        return sinopac_forwarder_pb2.TokenResponse(token=SERVER_TOKEN)

    def GetAllStockDetail(self, request, _):
        """
        GetAllStockDetail _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        response = sinopac_forwarder_pb2.StockDetailResponse()
        worker = WORKERS.get()
        tse_001 = worker.get_contract_tse_001()
        response.stock.append(
            sinopac_forwarder_pb2.StockDetailMessage(
                exchange=tse_001.exchange,
                category=tse_001.category,
                code=tse_001.code,
                name=tse_001.name,
                reference=tse_001.reference,
                update_date=tse_001.update_date,
                day_trade=tse_001.day_trade,
            )
        )
        for row in worker.stock_num_list:
            contract = worker.get_contract_by_stock_num(row)
            if contract is None:
                logger.error("%s has no stock data", row)
                continue
            response.stock.append(
                sinopac_forwarder_pb2.StockDetailMessage(
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

    def GetAllStockSnapshot(self, request, _):
        """
        GetAllStockSnapshot _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        contracts = []
        worker = WORKERS.get()
        for stock in worker.stock_num_list:
            contracts.append(worker.get_contract_by_stock_num(stock))
        splits = np.array_split(contracts, WORKERS.count())
        snapshots = []
        threads = []
        for i, split in enumerate(splits):
            threads.append(
                threading.Thread(
                    target=fill_sinopac_snapshot_arr,
                    args=(split, snapshots, WORKERS.get()),
                )
            )
            threads[i].start()
        for t in threads:
            t.join()
        response = sinopac_forwarder_pb2.StockSnapshotResponse()
        for result in snapshots:
            response.data.append(sinopac_snapshot_to_pb(result))
        return response

    def GetStockSnapshotTSE(self, request, _):
        """
        GetStockSnapshotTSE _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        worker = WORKERS.get()
        snapshots = worker.snapshots([worker.get_contract_tse_001()])
        response = sinopac_forwarder_pb2.StockSnapshotResponse()
        for result in snapshots:
            response.data.append(sinopac_snapshot_to_pb(result))
        return response

    def GetStockSnapshotByNumArr(self, request, _):
        """
        GetStockSnapshotByNumArr _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        contracts = []
        worker = WORKERS.get()
        for stock in request.stock_num_arr:
            contracts.append(worker.get_contract_by_stock_num(stock))
        splits = np.array_split(contracts, WORKERS.count())
        snapshots = []
        threads = []
        for i, split in enumerate(splits):
            threads.append(
                threading.Thread(
                    target=fill_sinopac_snapshot_arr,
                    args=(split, snapshots, WORKERS.get()),
                )
            )
            threads[i].start()
        for t in threads:
            t.join()
        response = sinopac_forwarder_pb2.StockSnapshotResponse()
        for result in snapshots:
            response.data.append(sinopac_snapshot_to_pb(result))
        return response

    def GetStockHistoryTick(self, request, _):
        """
        GetStockHistoryTick _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        response = sinopac_forwarder_pb2.StockHistoryTickResponse()
        threads = []
        for num in request.stock_num_arr:
            t = threading.Thread(
                target=fill_history_tick_response,
                args=(
                    WORKERS.get().get_contract_by_stock_num(num),
                    num,
                    request.date,
                    response,
                    WORKERS.get(),
                ),
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return response

    def GetStockTSEHistoryTick(self, request, _):
        """
        GetStockTSEHistoryTick _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        response = sinopac_forwarder_pb2.StockHistoryTickResponse()
        t = threading.Thread(
            target=fill_history_tick_response,
            args=(
                WORKERS.get().get_contract_tse_001(),
                "tse_001",
                request.date,
                response,
                WORKERS.get(),
            ),
        )
        t.start()
        t.join()
        return response

    def GetStockHistoryKbar(self, request, _):
        """
        GetStockHistoryKbar _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        response = sinopac_forwarder_pb2.StockHistoryKbarResponse()
        threads = []
        for num in request.stock_num_arr:
            t = threading.Thread(
                target=fill_history_kbar_response,
                args=(
                    WORKERS.get().get_contract_by_stock_num(num),
                    num,
                    request.date,
                    response,
                    WORKERS.get(),
                ),
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return response

    def GetStockTSEHistoryKbar(self, request, _):
        """
        GetStockHistoryKbar _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        response = sinopac_forwarder_pb2.StockHistoryKbarResponse()
        t = threading.Thread(
            target=fill_history_kbar_response,
            args=(
                WORKERS.get().get_contract_tse_001(),
                "tse_001",
                request.date,
                response,
                WORKERS.get(),
            ),
        )
        t.start()
        t.join()
        return response

    def GetStockHistoryClose(self, request, _):
        """
        GetStockHistoryClose _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        response = sinopac_forwarder_pb2.StockHistoryCloseResponse()
        threads = []
        for num in request.stock_num_arr:
            t = threading.Thread(
                target=fill_history_close_response,
                args=(
                    WORKERS.get().get_contract_by_stock_num(num),
                    num,
                    request.date,
                    response,
                    WORKERS.get(),
                ),
            )
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        return response

    def GetStockHistoryCloseByDateArr(self, request, _):
        """
        GetStockHistoryCloseByDateArr _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        response = sinopac_forwarder_pb2.StockHistoryCloseResponse()
        threads = []
        for date in request.date_arr:
            for num in request.stock_num_arr:
                t = threading.Thread(
                    target=fill_history_close_response,
                    args=(
                        WORKERS.get().get_contract_by_stock_num(num),
                        num,
                        date,
                        response,
                        WORKERS.get(),
                    ),
                )
                threads.append(t)
                t.start()
        for t in threads:
            t.join()
        return response

    def GetStockTSEHistoryClose(self, request, _):
        """
        GetStockTSEHistoryClose _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        response = sinopac_forwarder_pb2.StockHistoryCloseResponse()
        t = threading.Thread(
            target=fill_history_close_response,
            args=(
                WORKERS.get().get_contract_tse_001(),
                "tse_001",
                request.date,
                response,
                WORKERS.get(),
            ),
        )
        t.start()
        t.join()
        return response

    def GetStockVolumeRank(self, request, _):
        response = sinopac_forwarder_pb2.StockVolumeRankResponse()
        worker = WORKERS.get()
        ranks = worker.get_stock_volume_rank_by_date(request.count, request.date)
        for result in ranks:
            response.data.append(
                sinopac_forwarder_pb2.StockVolumeRankMessage(
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
        response = sinopac_forwarder_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = WORKERS.subscribe_stock_tick(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def SubscribeStockBidAsk(self, request, _):
        response = sinopac_forwarder_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = WORKERS.subscribe_stock_bidask(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def UnSubscribeStockTick(self, request, _):
        response = sinopac_forwarder_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = WORKERS.unsubscribe_stock_tick(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def UnSubscribeStockBidAsk(self, request, _):
        response = sinopac_forwarder_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = WORKERS.unsubscribe_stock_bidask(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response


class gRPCTradeMethod(sinopac_forwarder_pb2_grpc.TradeServiceServicer):
    def BuyStock(self, request, _):
        """
        BuyStock _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        result = WORKERS.buy_stock(
            request.stock_num, request.price, request.quantity, request.simulate
        )
        response = sinopac_forwarder_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )
        return response

    def SellStock(self, request, _):
        """
        SellStock _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        result = WORKERS.sell_stock(
            request.stock_num, request.price, request.quantity, request.simulate
        )
        response = sinopac_forwarder_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )
        return response

    def SellFirstStock(self, request, _):
        """
        SellFirstStock _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        result = WORKERS.sell_first_stock(
            request.stock_num, request.price, request.quantity, request.simulate
        )
        response = sinopac_forwarder_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )
        return response

    def CancelStock(self, request, _):
        """
        CancelStock _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        result = WORKERS.cancel_stock(request.order_id, request.simulate)
        response = sinopac_forwarder_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )
        return response

    def GetOrderStatusByID(self, request, _):
        """
        GetOrderStatusByID _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        result = WORKERS.get_order_status_by_id(request.order_id, request.simulate)
        response = sinopac_forwarder_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )
        return response

    def GetOrderStatusArr(self, request, _):
        """
        GetOrderStatusArr _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        arr = WORKERS.get_order_status_arr()
        response = sinopac_forwarder_pb2.StockOrderStatusArr()
        for order in arr:
            if order.status.order_datetime is None:
                order.status.order_datetime = datetime.now()
            order_price = int()
            if order.status.modified_price != 0:
                order_price = order.status.modified_price
            else:
                order_price = order.order.price
            response.data.append(
                sinopac_forwarder_pb2.StockOrderStatus(
                    code=order.contract.code,
                    action=order.order.action,
                    price=order_price,
                    quantity=order.order.quantity,
                    order_id=order.status.id,
                    status=order.status.status,
                    order_time=datetime.strftime(
                        order.status.order_datetime, "%Y-%m-%d %H:%M:%S"
                    ),
                )
            )
        return response

    def GetNonBlockOrderStatusArr(self, request, _):
        """
        GetNonBlockOrderStatusArr _summary_

        Args:
            request (_type_): _description_

        Returns:
            _type_: _description_
        """
        return sinopac_forwarder_pb2.FunctionErr(
            err=WORKERS.get_non_block_order_status_arr()
        )


def sinopac_snapshot_to_pb(result) -> sinopac_forwarder_pb2.StockSnapshotMessage:
    """
    sinopac_snapshot_to_pb _summary_

    Args:
        result (_type_): _description_

    Returns:
        sinopac_forwarder_pb2.StockSnapshotMessage: _description_
    """
    return sinopac_forwarder_pb2.StockSnapshotMessage(
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


def fill_sinopac_snapshot_arr(contracts, snapshots, sinopac: Sinopac):
    """
    fill_sinopac_snapshot_arr _summary_

    Args:
        contracts (_type_): _description_
        snapshots (_type_): _description_
        sinopac (Sinopac): _description_
    """
    snapshots.extend(sinopac.snapshots(contracts))


def fill_history_tick_response(contract, num, date, response, sinopac: Sinopac):
    """
    fill_history_tick_response _summary_

    Args:
        contract (_type_): _description_
        num (_type_): _description_
        date (_type_): _description_
        response (_type_): _description_
        sinopac (Sinopac): _description_
    """
    ticks = sinopac.ticks(contract, date)
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
            sinopac_forwarder_pb2.StockHistoryTickMessage(
                stock_num=num,
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


def fill_history_kbar_response(contract, num, date, response, sinopac: Sinopac):
    """
    fill_history_kbar_response _summary_

    Args:
        contract (_type_): _description_
        num (_type_): _description_
        date (_type_): _description_
        response (_type_): _description_
        sinopac (Sinopac): _description_
    """
    kbar = sinopac.kbars(contract, date)
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
            sinopac_forwarder_pb2.StockHistoryKbarMessage(
                stock_num=num,
                ts=kbar.ts[pos],
                Close=kbar.Close[pos],
                Open=kbar.Open[pos],
                High=kbar.High[pos],
                Low=kbar.Low[pos],
                Volume=kbar.Volume[pos],
            )
        )


def fill_history_close_response(contract, num, date, response, sinopac: Sinopac):
    """
    fill_history_close_response _summary_

    Args:
        contract (_type_): _description_
        num (_type_): _description_
        date (_type_): _description_
        response (_type_): _description_
        sinopac (Sinopac): _description_
    """
    response.data.append(
        sinopac_forwarder_pb2.StockHistoryCloseMessage(
            code=num,
            close=sinopac.get_stock_last_close_by_date(contract, date),
            date=date,
        )
    )


def serve(port: str, main_worker: Sinopac, workers: list[Sinopac], cfg: RequiredEnv):
    """
    serve _summary_

    Args:
        port (str): _description_
        main_worker (Sinopac): _description_
        workers (list[Sinopac]): _description_
        cfg (RequiredEnv): _description_
    """
    global WORKERS  # pylint: disable=global-statement
    WORKERS = SinopacWorker(main_worker, workers)

    # gRPC servicer
    sinopac_forwarder_servicer = gRPCSinopacForwarder()
    trade_servicer = gRPCTradeMethod()

    # set call back
    rq = RabbitMQS(
        cfg.rabbitmq_url,
        cfg.rabbitmq_exchange,
    )
    create_channel = []
    create_channel.append(threading.Thread(target=rq.create_event_channel))
    create_channel.append(threading.Thread(target=rq.create_tick_channel))
    create_channel.append(threading.Thread(target=rq.create_bid_ask_channel))
    create_channel.append(threading.Thread(target=rq.create_order_status_channel))
    for t in create_channel:
        t.start()
        t.join()

    WORKERS.set_event_cb(rq.event_callback)
    WORKERS.set_quote_cb(rq.quote_callback_v1)
    WORKERS.set_bid_ask_cb(rq.bid_ask_callback)
    WORKERS.set_order_status_cb(rq.order_status_callback)

    server = grpc.server(futures.ThreadPoolExecutor())
    sinopac_forwarder_pb2_grpc.add_SinopacForwarderServicer_to_server(
        sinopac_forwarder_servicer, server
    )
    sinopac_forwarder_pb2_grpc.add_TradeServiceServicer_to_server(
        trade_servicer, server
    )

    server.add_insecure_port(f"[::]:{port}")
    server.start()
    logger.info("gRPC Server started at port %s", port)
    server.wait_for_termination()
