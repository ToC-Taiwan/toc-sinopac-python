import logging
import threading
import time
from datetime import datetime
from queue import Queue

import common_pb2
import pika
import shioaji as sj
import trade_pb2

logging.getLogger("pika").setLevel(logging.WARNING)


class PikaCC:
    def __init__(self, conn: pika.BlockingConnection, ch):
        self.conn = conn
        self.ch = ch

    def heartbeat(self):
        self.conn.process_data_events()


class RabbitMQS:
    def __init__(self, url: str, exchange: str, pool_size: int):
        # pika
        self.exchange = exchange
        self.parameters = pika.URLParameters(url)
        self.pool_size = pool_size
        # queue
        self.pika_queue: Queue = Queue()
        # lock
        self.order_cb_lock = threading.Lock()
        # initial connections
        self.fill_pika_queue()

    def send_heartbeat(self):
        while True:
            time.sleep(20)
            count = 0
            while True:
                if count >= self.pool_size:
                    break
                p = self.pika_queue.get(block=True)
                p.heartbeat()
                count += 1
                self.pika_queue.put(p)

    def create_pika(self):
        conn = pika.BlockingConnection(self.parameters)
        ch = conn.channel()
        ch.exchange_declare(
            exchange=self.exchange, exchange_type="direct", durable=True
        )
        return PikaCC(conn, ch)

    def fill_pika_queue(self):
        for _ in range(self.pool_size):
            self.pika_queue.put(self.create_pika())
        threading.Thread(target=self.send_heartbeat).start()

    def event_callback(self, resp_code: int, event_code: int, info: str, event: str):
        p = self.pika_queue.get(block=True)
        p.ch.basic_publish(
            exchange=self.exchange,
            routing_key="event",
            body=common_pb2.EventMessage(
                resp_code=resp_code,
                event_code=event_code,
                info=info,
                event=event,
                event_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
            ).SerializeToString(),
        )
        self.pika_queue.put(p)

    def order_status_callback(self, reply: list[sj.order.Trade]):
        with self.order_cb_lock:
            for order in reply:
                if order.status.order_datetime is None:
                    order.status.order_datetime = datetime.now()
                order_price = int()
                if order.status.modified_price != 0:
                    order_price = order.status.modified_price
                else:
                    order_price = order.order.price
                qty = order.order.quantity
                if order.status.deal_quantity not in (0, qty):
                    qty = order.status.deal_quantity

                p = self.pika_queue.get(block=True)
                p.ch.basic_publish(
                    exchange=self.exchange,
                    routing_key="order",
                    body=trade_pb2.StockOrderStatus(
                        code=order.contract.code,
                        action=order.order.action,
                        price=order_price,
                        quantity=qty,
                        order_id=order.status.id,
                        status=order.status.status,
                        order_time=datetime.strftime(
                            order.status.order_datetime, "%Y-%m-%d %H:%M:%S"
                        ),
                    ).SerializeToString(),
                )
                self.pika_queue.put(p)

    def stock_quote_callback_v1(self, _, tick: sj.TickSTKv1):
        p = self.pika_queue.get(block=True)
        p.ch.basic_publish(
            exchange=self.exchange,
            routing_key=f"tick:{tick.code}",
            body=common_pb2.StockRealTimeTickMessage(
                code=tick.code,
                date_time=datetime.strftime(tick.datetime, "%Y-%m-%d %H:%M:%S.%f"),
                open=tick.open,
                avg_price=tick.avg_price,
                close=tick.close,
                high=tick.high,
                low=tick.low,
                amount=tick.amount,
                total_amount=tick.total_amount,
                volume=tick.volume,
                total_volume=tick.total_volume,
                tick_type=tick.tick_type,
                chg_type=tick.chg_type,
                price_chg=tick.price_chg,
                pct_chg=tick.pct_chg,
                bid_side_total_vol=tick.bid_side_total_vol,
                ask_side_total_vol=tick.ask_side_total_vol,
                bid_side_total_cnt=tick.bid_side_total_cnt,
                ask_side_total_cnt=tick.ask_side_total_cnt,
                suspend=tick.suspend,
                simtrade=tick.simtrade,
            ).SerializeToString(),
        )
        self.pika_queue.put(p)

    def future_quote_callback_v1(self, _, tick: sj.TickFOPv1):
        p = self.pika_queue.get(block=True)
        p.ch.basic_publish(
            exchange=self.exchange,
            routing_key=f"future_tick:{tick.code}",
            body=common_pb2.FutureRealTimeTickMessage(
                code=tick.code,
                date_time=datetime.strftime(tick.datetime, "%Y-%m-%d %H:%M:%S.%f"),
                open=tick.open,
                underlying_price=tick.underlying_price,
                bid_side_total_vol=tick.bid_side_total_vol,
                ask_side_total_vol=tick.ask_side_total_vol,
                avg_price=tick.avg_price,
                close=tick.close,
                high=tick.high,
                low=tick.low,
                amount=tick.amount,
                total_amount=tick.total_amount,
                volume=tick.volume,
                total_volume=tick.total_volume,
                tick_type=tick.tick_type,
                chg_type=tick.chg_type,
                price_chg=tick.price_chg,
                pct_chg=tick.pct_chg,
                simtrade=tick.simtrade,
            ).SerializeToString(),
        )
        self.pika_queue.put(p)

    def stock_bid_ask_callback(self, _, bidask: sj.BidAskSTKv1):
        p = self.pika_queue.get(block=True)
        p.ch.basic_publish(
            exchange=self.exchange,
            routing_key=f"bid_ask:{bidask.code}",
            body=common_pb2.StockRealTimeBidAskMessage(
                code=bidask.code,
                date_time=datetime.strftime(bidask.datetime, "%Y-%m-%d %H:%M:%S.%f"),
                suspend=bidask.suspend,
                simtrade=bidask.simtrade,
                bid_price=bidask.bid_price,
                bid_volume=bidask.bid_volume,
                diff_bid_vol=bidask.diff_bid_vol,
                ask_price=bidask.ask_price,
                ask_volume=bidask.ask_volume,
                diff_ask_vol=bidask.diff_ask_vol,
            ).SerializeToString(),
        )
        self.pika_queue.put(p)

    def future_bid_ask_callback(self, _, bidask: sj.BidAskFOPv1):
        p = self.pika_queue.get(block=True)
        p.ch.basic_publish(
            exchange=self.exchange,
            routing_key=f"future_bid_ask:{bidask.code}",
            body=common_pb2.FutureRealTimeBidAskMessage(
                code=bidask.code,
                date_time=datetime.strftime(bidask.datetime, "%Y-%m-%d %H:%M:%S.%f"),
                bid_total_vol=bidask.bid_total_vol,
                ask_total_vol=bidask.ask_total_vol,
                simtrade=bidask.simtrade,
                bid_price=bidask.bid_price,
                bid_volume=bidask.bid_volume,
                diff_bid_vol=bidask.diff_bid_vol,
                ask_price=bidask.ask_price,
                ask_volume=bidask.ask_volume,
                diff_ask_vol=bidask.diff_ask_vol,
                first_derived_bid_price=bidask.first_derived_bid_price,
                first_derived_ask_price=bidask.first_derived_ask_price,
                first_derived_bid_vol=bidask.first_derived_bid_vol,
                first_derived_ask_vol=bidask.first_derived_ask_vol,
                underlying_price=bidask.underlying_price,
            ).SerializeToString(),
        )
        self.pika_queue.put(p)

    def send_order(self, order: sj.order.Trade):
        with self.order_cb_lock:
            p = self.pika_queue.get(block=True)
            p.ch.basic_publish(
                exchange=self.exchange,
                routing_key="order",
                body=trade_pb2.StockOrderStatus(
                    code=order.contract.code,
                    action=order.order.action,
                    price=order.order.price,
                    quantity=order.order.quantity,
                    order_id=order.status.id,
                    status=order.status.status,
                    order_time=datetime.strftime(
                        order.status.order_datetime, "%Y-%m-%d %H:%M:%S"
                    ),
                ).SerializeToString(),
            )
            self.pika_queue.put(p)
