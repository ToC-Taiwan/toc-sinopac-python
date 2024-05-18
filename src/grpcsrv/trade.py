import threading
from datetime import datetime

from google.protobuf import empty_pb2
from toc_trade_pb.forwarder import trade_pb2, trade_pb2_grpc

from simulator import Simulator
from worker_pool import WorkerPool


class RPCTrade(trade_pb2_grpc.TradeInterfaceServicer):
    def __init__(
        self,
        simulator: Simulator,
        workers: WorkerPool,
    ):
        self.simulator = simulator
        self.workers = workers
        self.send_order_lock = threading.Lock()

    def GetFuturePosition(self, request: empty_pb2.Empty, _):
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

    def GetStockPosition(self, request: empty_pb2.Empty, _):
        response = trade_pb2.StockPositionArr()
        result = self.workers.get_stock_position()
        for pos in result:
            data_arr: list[trade_pb2.StockPositionDetail] = []
            detail = self.workers.get_position_detail(pos.id)
            if detail is not None and len(detail) > 0:
                for d in detail:
                    data_arr.append(
                        trade_pb2.StockPositionDetail(
                            date=d.date,
                            code=d.code,
                            quantity=d.quantity,
                            price=d.price,
                            last_price=d.last_price,
                            dseq=d.dseq,
                            direction=d.direction,
                            pnl=d.pnl,
                            currency=d.currency,
                            fee=d.fee,
                        )
                    )

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
                    detail_arr=data_arr,
                )
            )
        return response

    def CancelOrder(self, request: trade_pb2.OrderID, _):
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

    def BuyStock(self, request: trade_pb2.StockOrderDetail, _):
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

    def SellStock(self, request: trade_pb2.StockOrderDetail, _):
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

    def BuyOddStock(self, request: trade_pb2.OddStockOrderDetail, _):
        result = None
        result = self.workers.buy_odd_stock(
            request.stock_num,
            request.price,
            request.share,
        )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def SellOddStock(self, request: trade_pb2.OddStockOrderDetail, _):
        result = None
        result = self.workers.sell_odd_stock(
            request.stock_num,
            request.price,
            request.share,
        )
        return trade_pb2.TradeResult(
            order_id=result.order_id,
            status=result.status,
            error=result.error,
        )

    def SellFirstStock(self, request: trade_pb2.StockOrderDetail, _):
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

    def GetLocalOrderStatusArr(self, request: empty_pb2.Empty, _):
        self.workers.send_local_order_status_arr()
        return empty_pb2.Empty()

    def GetSimulateOrderStatusArr(self, request: empty_pb2.Empty, _):
        self.workers.send_simulate_local_order_status_arr(self.simulator.get_local_order())
        return empty_pb2.Empty()

    def BuyFuture(self, request: trade_pb2.FutureOrderDetail, _):
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

    def SellFuture(self, request: trade_pb2.FutureOrderDetail, _):
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

    def SellFirstFuture(self, request: trade_pb2.FutureOrderDetail, _):
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

    def BuyOption(self, request: trade_pb2.OptionOrderDetail, _):
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

    def SellOption(self, request: trade_pb2.OptionOrderDetail, _):
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

    def SellFirstOption(self, request: trade_pb2.OptionOrderDetail, _):
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

    def GetAccountBalance(self, request: empty_pb2.Empty, _):
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

    def GetSettlement(self, request: empty_pb2.Empty, _):
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

    def GetMargin(self, request: empty_pb2.Empty, _):
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
