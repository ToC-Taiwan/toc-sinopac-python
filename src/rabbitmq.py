import logging
import threading
from datetime import datetime
from queue import Queue

import pika
import shioaji as sj

import sinopac_forwarder_pb2

logging.getLogger("pika").setLevel(logging.WARNING)


class RabbitMQS:
    def __init__(self, url: str, exchange: str):
        self.exchange = exchange
        self.parameters = pika.URLParameters(url)
        self.event_channel_queue: Queue = Queue()
        self.tick_channel_queue: Queue = Queue()
        self.bid_ask_channel_queue: Queue = Queue()
        self.order_status_channel_queue: Queue = Queue()
        self.order_cb_lock = threading.Lock()

    def create_connection(self):
        return pika.BlockingConnection(self.parameters)

    def create_event_channel(self):
        connection = self.create_connection()
        new = connection.channel()
        new.exchange_declare(
            exchange=self.exchange, exchange_type="direct", durable=True
        )
        self.event_channel_queue.put(new)

    def create_tick_channel(self):
        for _ in range(128):
            connection = self.create_connection()
            new = connection.channel()
            new.exchange_declare(
                exchange=self.exchange, exchange_type="direct", durable=True
            )
            self.tick_channel_queue.put(new)

    def create_bid_ask_channel(self):
        for _ in range(128):
            connection = self.create_connection()
            new = connection.channel()
            new.exchange_declare(
                exchange=self.exchange, exchange_type="direct", durable=True
            )
            self.bid_ask_channel_queue.put(new)

    def create_order_status_channel(self):
        connection = self.create_connection()
        new = connection.channel()
        new.exchange_declare(
            exchange=self.exchange, exchange_type="direct", durable=True
        )
        self.order_status_channel_queue.put(new)

    def event_callback(self, resp_code: int, event_code: int, info: str, event: str):
        """
        event_callback _summary_

        Args:
            resp_code (int): _description_
            event_code (int): _description_
            info (str): _description_
            event (str): _description_
        """
        data = sinopac_forwarder_pb2.EventResponse(
            resp_code=resp_code,
            event_code=event_code,
            info=info,
            event=event,
            event_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
        )
        channel = self.event_channel_queue.get(block=True)
        channel.basic_publish(
            exchange=self.exchange,
            routing_key="event",
            body=data.SerializeToString(),
        )
        self.event_channel_queue.put(channel)

    def quote_callback_v1(self, _, tick: sj.TickSTKv1):
        """
        quote_callback_v1 _summary_

        Args:
            tick (sj.TickSTKv1): _description_
        """
        data = sinopac_forwarder_pb2.StockRealTimeTickResponse(
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
        )
        channel = self.tick_channel_queue.get(block=True)
        channel.basic_publish(
            exchange=self.exchange,
            routing_key="tick",
            body=data.SerializeToString(),
        )
        self.tick_channel_queue.put(channel)

    def bid_ask_callback(self, _, bidask: sj.BidAskSTKv1):
        """
        bid_ask_callback _summary_

        Args:
            bidask (sj.BidAskSTKv1): _description_
        """
        data = sinopac_forwarder_pb2.StockRealTimeBidAskResponse(
            code=bidask.code,
            date_time=datetime.strftime(bidask.datetime, "%Y-%m-%d %H:%M:%S.%f"),
            suspend=bidask.suspend,
            simtrade=bidask.simtrade,
        )
        data.bid_price.extend(bidask.bid_price)
        data.bid_volume.extend(bidask.bid_volume)
        data.diff_bid_vol.extend(bidask.diff_bid_vol)
        data.ask_price.extend(bidask.ask_price)
        data.ask_volume.extend(bidask.ask_volume)
        data.diff_ask_vol.extend(bidask.diff_ask_vol)
        channel = self.bid_ask_channel_queue.get(block=True)
        channel.basic_publish(
            exchange=self.exchange,
            routing_key="bid_ask",
            body=data.SerializeToString(),
        )
        self.bid_ask_channel_queue.put(channel)

    def order_status_callback(self, reply: list[sj.order.Trade]):
        """
        order_status_callback _summary_

        Args:
            reply (list[sj.order.Trade]): _description_
        """
        with self.order_cb_lock:
            if len(reply) != 0:
                for order in reply:
                    if order.status.order_datetime is None:
                        order.status.order_datetime = datetime.now()
                    order_price = int()
                    if order.status.modified_price != 0:
                        order_price = order.status.modified_price
                    else:
                        order_price = order.order.price
                    data = sinopac_forwarder_pb2.StockOrderStatus(
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
                    channel = self.order_status_channel_queue.get(block=True)
                    channel.basic_publish(
                        exchange=self.exchange,
                        routing_key="order_status",
                        body=data.SerializeToString(),
                    )
                    self.order_status_channel_queue.put(channel)
