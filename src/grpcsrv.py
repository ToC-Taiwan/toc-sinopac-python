import os
import threading
import time
from concurrent import futures
from datetime import datetime

import google.protobuf.empty_pb2
import grpc
import numpy as np
from shioaji.data import Snapshot
from shioaji.error import TokenError

from logger import logger
from pb import (
    basic_pb2,
    basic_pb2_grpc,
    entity_pb2,
    history_pb2,
    history_pb2_grpc,
    realtime_pb2,
    realtime_pb2_grpc,
    subscribe_pb2,
    subscribe_pb2_grpc,
    trade_pb2,
    trade_pb2_grpc,
)
from rabbitmq import RabbitMQS
from simulator import Simulator
from sinopac import Sinopac
from sinopac_worker import SinopacWorkerPool
from yahoo_finance import Yahoo


class RPCBasic(basic_pb2_grpc.BasicDataInterfaceServicer):
    def __init__(
        self,
        simulator: Simulator,
        workers: SinopacWorkerPool,
    ):
        self.workers = workers
        self.simulator = simulator
        self.heart_beat_client_arr: list[str] = []
        self.heart_beat_client_arr_lock = threading.Lock()

    def Heartbeat(self, request_iterator, context: grpc.ServicerContext):
        for beat in request_iterator:
            with self.heart_beat_client_arr_lock:
                if len(self.heart_beat_client_arr) > 0:
                    yield basic_pb2.BeatMessage(error="sinopac only one client allowed")
                else:
                    self.heart_beat_client_arr.append(beat.message)
                    threading.Thread(target=self.check_context, args=(context,), daemon=True).start()
                    logger.info("new sinopac gRPC client connected: %s", beat.message)
            yield basic_pb2.BeatMessage(message=beat.message)

    def check_context(self, context: grpc.ServicerContext):
        while context.is_active():
            time.sleep(1)

        logger.info("sinopac gRPC client disconnected")
        with self.heart_beat_client_arr_lock:
            if len(self.heart_beat_client_arr) > 0 and self.heart_beat_client_arr[0] == "debug":
                self.workers.unsubscribe_all_tick()
                self.workers.unsubscribe_all_bidask()
                self.simulator.reset_simulator()
                self.heart_beat_client_arr.clear()
            else:
                os._exit(0)

    def Terminate(self, request, _):
        threading.Thread(target=self.wait_and_terminate, daemon=True).start()
        return google.protobuf.empty_pb2.Empty()

    def wait_and_terminate(self):
        time.sleep(3)
        os._exit(0)

    def GetAllStockDetail(self, request, _):
        response = basic_pb2.StockDetailResponse()
        worker = self.workers.get(False)

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
        for row in self.workers.get_stock_num_list():
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
        worker = self.workers.get(False)

        for row in self.workers.get_future_code_list():
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

    def GetAllOptionDetail(self, request, _):
        response = basic_pb2.OptionDetailResponse()
        worker = self.workers.get(False)

        for row in self.workers.get_option_code_list():
            contract = worker.get_contract_by_option_code(row)
            if contract is None:
                logger.error("%s has no option data", row)
                continue
            response.option.append(
                basic_pb2.OptionDetailMessage(
                    code=contract.code,
                    symbol=contract.symbol,
                    name=contract.name,
                    category=contract.category,
                    delivery_month=contract.delivery_month,
                    delivery_date=contract.delivery_date,
                    strike_price=contract.strike_price,
                    option_right=contract.option_right,
                    underlying_kind=contract.underlying_kind,
                    unit=contract.unit,
                    limit_up=contract.limit_up,
                    limit_down=contract.limit_down,
                    reference=contract.reference,
                    update_date=contract.update_date,
                )
            )
        return response


class RPCHistory(history_pb2_grpc.HistoryDataInterfaceServicer):
    def __init__(self, workers: SinopacWorkerPool):
        self.workers = workers

    def fill_stock_history_tick_response(self, num, date, response, worker: Sinopac):
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
                    self.workers.get(True),
                ),
                daemon=True,
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return response

    def fill_stock_history_kbar_response(self, num, date, response, worker: Sinopac):
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
                    self.workers.get(True),
                ),
                daemon=True,
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return response

    def fill_stock_history_close_response(self, num, date, response, sinopac: Sinopac):
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
                    self.workers.get(True),
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
                        self.workers.get(True),
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
                self.workers.get(True),
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
                self.workers.get(True),
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
                self.workers.get(True),
            ),
            daemon=True,
        )
        thread.start()
        thread.join()
        return response

    def fill_future_history_tick_response(self, code, date, response, worker: Sinopac):
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
                    self.workers.get(True),
                ),
                daemon=True,
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return response

    def fill_future_history_kbar_response(self, code, date, response, sinopac: Sinopac):
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
                    self.workers.get(True),
                ),
                daemon=True,
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return response

    def fill_future_history_close_response(self, code, date, response, sinopac: Sinopac):
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
                    self.workers.get(True),
                ),
                daemon=True,
            )
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        return response


class RPCTrade(trade_pb2_grpc.TradeInterfaceServicer):
    def __init__(
        self,
        rabbit: RabbitMQS,
        simulator: Simulator,
        workers: SinopacWorkerPool,
    ):
        self.rabbit = rabbit
        self.simulator = simulator
        self.send_order_lock = threading.Lock()
        self.workers = workers

    def GetFuturePosition(self, request, _):
        response = trade_pb2.FuturePositionArr()
        result = self.workers.get_future_position()
        for pos in result:
            response.position_arr.append(
                trade_pb2.FuturePosition(
                    code=pos.code,
                    direction=pos.direction,
                    quantity=pos.quantity,
                    price=pos.price,
                    last_price=pos.last_price,
                    pnl=pos.pnl,
                )
            )
        return response

    def GetStockPosition(self, request, _):
        response = trade_pb2.StockPositionArr()
        result = self.workers.get_stock_position()
        for pos in result:
            response.position_arr.append(
                trade_pb2.StockPosition(
                    id=pos.id,
                    code=pos.code,
                    direction=pos.direction,
                    quantity=pos.quantity,
                    price=pos.price,
                    last_price=pos.last_price,
                    pnl=pos.pnl,
                    yd_quantity=pos.yd_quantity,
                    cond=pos.cond,
                    margin_purchase_amount=pos.margin_purchase_amount,
                    collateral=pos.collateral,
                    short_sale_margin=pos.short_sale_margin,
                    interest=pos.interest,
                )
            )
        return response

    def BuyStock(self, request, _):
        result = None
        if request.simulate is not True:
            result = self.workers.buy_stock(
                request.stock_num,
                request.price,
                request.quantity,
            )
        else:
            result = self.simulator.buy_stock(
                request.stock_num,
                request.price,
                request.quantity,
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def SellStock(self, request, _):
        result = None
        if request.simulate is not True:
            result = self.workers.sell_stock(
                request.stock_num,
                request.price,
                request.quantity,
            )
        else:
            result = self.simulator.sell_stock(
                request.stock_num,
                request.price,
                request.quantity,
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def BuyOddStock(self, request, _):
        result = None
        result = self.workers.buy_odd_stock(
            request.stock_num,
            request.price,
            request.quantity,
        )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def SellOddStock(self, request, _):
        result = None
        result = self.workers.sell_odd_stock(
            request.stock_num,
            request.price,
            request.quantity,
        )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def SellFirstStock(self, request, _):
        result = None
        if request.simulate is not True:
            result = self.workers.sell_first_stock(
                request.stock_num,
                request.price,
                request.quantity,
            )
        else:
            result = self.simulator.sell_first_stock(
                request.stock_num,
                request.price,
                request.quantity,
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def CancelStock(self, request, _):
        result = None
        if request.simulate is not True:
            result = self.workers.cancel_stock(request.order_id)
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
            result = self.workers.get_order_status_by_id(request.order_id)
        else:
            result = self.simulator.get_local_order_by_id(request.order_id)
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def GetLocalOrderStatusArr(self, request, _):
        with self.send_order_lock:
            self.rabbit.send_order_arr(self.workers.get_local_order())
            return google.protobuf.empty_pb2.Empty()

    def GetSimulateOrderStatusArr(self, request, _):
        with self.send_order_lock:
            self.rabbit.send_order_arr(self.simulator.get_local_order())
            return google.protobuf.empty_pb2.Empty()

    def GetNonBlockOrderStatusArr(self, request, _):
        return entity_pb2.ErrorMessage(err=self.workers.get_non_block_order_status_arr())

    def BuyFuture(self, request, _):
        result = None
        if request.simulate is not True:
            result = self.workers.buy_future(
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
            result = self.workers.sell_future(
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
            result = self.workers.sell_first_future(
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
            result = self.workers.cancel_future(
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

    def BuyOption(self, request, _):
        result = None
        if request.simulate is not True:
            result = self.workers.buy_option(
                request.code,
                request.price,
                request.quantity,
            )
        else:
            result = self.simulator.buy_option(
                request.code,
                request.price,
                request.quantity,
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def SellOption(self, request, _):
        result = None
        if request.simulate is not True:
            result = self.workers.sell_option(
                request.code,
                request.price,
                request.quantity,
            )
        else:
            result = self.simulator.sell_option(
                request.code,
                request.price,
                request.quantity,
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def SellFirstOption(self, request, _):
        result = None
        if request.simulate is not True:
            result = self.workers.sell_first_option(
                request.code,
                request.price,
                request.quantity,
            )
        else:
            result = self.simulator.sell_first_option(
                request.code,
                request.price,
                request.quantity,
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def CancelOption(self, request, _):
        result = None
        if request.simulate is not True:
            result = self.workers.cancel_option(
                request.order_id,
            )
        else:
            result = self.simulator.cancel_option(
                request.order_id,
            )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def GetAccountBalance(self, request, _):
        balance = self.workers.account_balance()
        if balance is None:
            return trade_pb2.AccountBalance(
                date="",
                balance=0,
            )
        return trade_pb2.AccountBalance(
            date=balance.date,
            balance=balance.acc_balance,
        )

    def GetSettlement(self, request, _):
        result = trade_pb2.SettlementList()
        settlements = self.workers.settlements()
        for settle in settlements:
            result.settlement.append(
                trade_pb2.Settlement(
                    date=datetime.strftime(settle.date, "%Y-%m-%d %H:%M:%S"),
                    amount=settle.amount,
                )
            )
        return result

    def GetMargin(self, request, _):
        margin = self.workers.margin()
        if margin is None:
            return trade_pb2.Margin()
        return trade_pb2.Margin(
            status=margin.status,
            yesterday_balance=margin.yesterday_balance,
            today_balance=margin.today_balance,
            deposit_withdrawal=margin.deposit_withdrawal,
            fee=margin.fee,
            tax=margin.tax,
            initial_margin=margin.initial_margin,
            maintenance_margin=margin.maintenance_margin,
            margin_call=margin.margin_call,
            risk_indicator=margin.risk_indicator,
            royalty_revenue_expenditure=margin.royalty_revenue_expenditure,
            equity=margin.equity,
            equity_amount=margin.equity_amount,
            option_openbuy_market_value=margin.option_openbuy_market_value,
            option_opensell_market_value=margin.option_opensell_market_value,
            option_open_position=margin.option_open_position,
            option_settle_profitloss=margin.option_settle_profitloss,
            future_open_position=margin.future_open_position,
            today_future_open_position=margin.today_future_open_position,
            future_settle_profitloss=margin.future_settle_profitloss,
            available_margin=margin.available_margin,
            plus_margin=margin.plus_margin,
            plus_margin_indicator=margin.plus_margin_indicator,
            security_collateral_amount=margin.security_collateral_amount,
            order_margin_premium=margin.order_margin_premium,
            collateral_amount=margin.collateral_amount,
        )


class RPCRealTime(realtime_pb2_grpc.RealTimeDataInterfaceServicer):
    def __init__(self, source: Yahoo, workers: SinopacWorkerPool):
        self.source = source
        self.workers = workers

    def fill_snapshot_arr(self, contracts, snapshots, worker: Sinopac):
        try:
            data = worker.snapshots(contracts)
        except TokenError:
            logger.error("Token Error")
            os._exit(0)

        if data is not None:
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
        worker = self.workers.get(False)

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
                        self.workers.get(True),
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
        contracts = []
        worker = self.workers.get(False)

        for stock in self.workers.get_stock_num_list():
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
                        self.workers.get(True),
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
        worker = self.workers.get(True)
        try:
            snapshots = worker.snapshots([worker.get_contract_tse_001()])
        except TokenError:
            logger.error("token error")
            os._exit(0)
        return self.sinopac_snapshot_to_pb(snapshots[0])

    def GetStockSnapshotOTC(self, request, _):
        worker = self.workers.get(True)
        try:
            snapshots = worker.snapshots([worker.get_contract_otc_101()])
        except TokenError:
            logger.error("token error")
            os._exit(0)
        return self.sinopac_snapshot_to_pb(snapshots[0])

    def GetStockVolumeRank(self, request, _):
        response = realtime_pb2.StockVolumeRankResponse()
        ranks = self.workers.get(True).get_stock_volume_rank_by_date(request.count, request.date)
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
        worker = self.workers.get(False)

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
                        self.workers.get(True),
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


class RPCSubscribe(subscribe_pb2_grpc.SubscribeDataInterfaceServicer):
    def __init__(self, workers: SinopacWorkerPool):
        self.workers = workers

    def SubscribeStockTick(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = self.workers.subscribe_stock_tick(stock_num, request.odd)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def UnSubscribeStockTick(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = self.workers.unsubscribe_stock_tick(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def SubscribeStockBidAsk(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = self.workers.subscribe_stock_bidask(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def UnSubscribeStockBidAsk(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for stock_num in request.stock_num_arr:
            result = self.workers.unsubscribe_stock_bidask(stock_num)
            if result is not None:
                response.fail_arr.append(stock_num)
        return response

    def SubscribeFutureTick(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for code in request.future_code_arr:
            result = self.workers.subscribe_future_tick(code)
            if result is not None:
                response.fail_arr.append(code)
        return response

    def UnSubscribeFutureTick(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for code in request.future_code_arr:
            result = self.workers.unsubscribe_future_tick(code)
            if result is not None:
                response.fail_arr.append(code)
        return response

    def SubscribeFutureBidAsk(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for code in request.future_code_arr:
            result = self.workers.subscribe_future_bidask(code)
            if result is not None:
                response.fail_arr.append(code)
        return response

    def UnSubscribeFutureBidAsk(self, request, _):
        response = subscribe_pb2.SubscribeResponse()
        for code in request.future_code_arr:
            result = self.workers.unsubscribe_future_bidask(code)
            if result is not None:
                response.fail_arr.append(code)
        return response

    def UnSubscribeAllTick(self, request, _):
        result = self.workers.unsubscribe_all_tick()
        if len(result["stock"]) > 0 or len(result["future"]) > 0:
            return entity_pb2.ErrorMessage(err="UnSubscribeAllTick fail")
        return entity_pb2.ErrorMessage(err="")

    def UnSubscribeAllBidAsk(self, request, _):
        result = self.workers.unsubscribe_all_bidask()
        if len(result["stock"]) > 0 or len(result["future"]) > 0:
            return entity_pb2.ErrorMessage(err="UnSubscribeAllBidAsk fail")
        return entity_pb2.ErrorMessage(err="")


class GRPCServer:
    def __init__(self, worker_pool: SinopacWorkerPool, rabbit: RabbitMQS):
        # simulator
        simulator = Simulator(worker_pool.main_worker)

        # gRPC servicer
        basic_servicer = RPCBasic(
            simulator=simulator,
            workers=worker_pool,
        )

        history_servicer = RPCHistory(
            workers=worker_pool,
        )

        realtime_servicer = RPCRealTime(
            source=Yahoo(),
            workers=worker_pool,
        )

        subscribe_servicer = RPCSubscribe(
            workers=worker_pool,
        )

        trade_servicer = RPCTrade(
            rabbit=rabbit,
            simulator=simulator,
            workers=worker_pool,
        )
        self.worker_pool = worker_pool

        server = grpc.server(
            futures.ThreadPoolExecutor(),
            options=[
                (
                    "grpc.max_send_message_length",
                    1024 * 1024 * 1024,
                ),
                (
                    "grpc.max_receive_message_length",
                    1024 * 1024 * 1024,
                ),
            ],
        )
        basic_pb2_grpc.add_BasicDataInterfaceServicer_to_server(basic_servicer, server)
        history_pb2_grpc.add_HistoryDataInterfaceServicer_to_server(history_servicer, server)
        realtime_pb2_grpc.add_RealTimeDataInterfaceServicer_to_server(realtime_servicer, server)
        subscribe_pb2_grpc.add_SubscribeDataInterfaceServicer_to_server(subscribe_servicer, server)
        trade_pb2_grpc.add_TradeInterfaceServicer_to_server(trade_servicer, server)

        self.server = server

    def serve(self, port: str):
        self.server.add_insecure_port(f"[::]:{port}")
        self.server.start()
        logger.info("shioaji version: %s", self.worker_pool.get_sj_version())
        logger.info("gRPC Server started at port %s", port)
        self.server.wait_for_termination()
