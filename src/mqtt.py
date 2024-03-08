import threading
import time
from datetime import datetime, timedelta

import paho.mqtt.client as mqtt
import shioaji as sj
import shioaji.constant as sc

from logger import logger
from pb.forwarder import mq_pb2

EXCAHNG_TYPE: str = "direct"

ROUTING_KEY_EVENT: str = "event"
ROUTING_KEY_ORDER_ARR: str = "order_arr"

ROUTING_KEY_STOCK_TICK: str = "stock_tick"
ROUTING_KEY_STOCK_TICK_ODDS: str = "stock_tick_odds"

ROUTING_KEY_FUTURE_TICK: str = "future_tick"
ROUTING_KEY_FUTURE_BID_ASK: str = "future_bid_ask"

ROUTING_KEY_STOCK_BID_ASK: str = "stock_bid_ask"
ROUTING_KEY_STOCK_BID_ASK_ODDS: str = "stock_bid_ask_odds"

DATE_TIME_FORMAT: str = "%Y-%m-%d %H:%M:%S.%f"


class MQTT:
    def __init__(self, host: str, port: int):
        self.order_cb_lock = threading.Lock()
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_disconnect = self.on_disconnect
        self.host = host
        self.port = port

    def connect(self):
        try:
            self.mqttc.connect(self.host, port=self.port, keepalive=10)
        except Exception:
            logger.error("MQTT connect failed, retrying...")
            time.sleep(1)
            self.connect()

        thread = threading.Thread(
            target=self.mqttc.loop_forever,
            daemon=True,
        )
        thread.start()

    def on_connect(self, _____, _, __, ___, ____):
        logger.info("MQTT connected")

    def on_disconnect(self, _, __, ___, ____, _____):
        logger.error("MQTT disconnected, reconnecting...")
        self.mqttc.disconnect()
        self.connect()

    def event_callback(
        self,
        resp_code: int,
        event_code: int,
        info: str,
        event: str,
    ):
        self.mqttc.publish(
            f"{EXCAHNG_TYPE}/{ROUTING_KEY_EVENT}",
            mq_pb2.EventMessage(
                resp_code=resp_code,
                event_code=event_code,
                info=info,
                event=event,
                event_time=datetime.now().strftime(DATE_TIME_FORMAT),
            ).SerializeToString(),
            qos=0,
        )

    def stock_quote_callback_v1(
        self,
        _,
        tick: sj.TickSTKv1,
    ):
        key = f"{EXCAHNG_TYPE}/{ROUTING_KEY_STOCK_TICK}/{tick.code}"
        if bool(tick.intraday_odd):
            key = f"{EXCAHNG_TYPE}/{ROUTING_KEY_STOCK_TICK_ODDS}/{tick.code}"
        self.mqttc.publish(
            key,
            mq_pb2.StockRealTimeTickMessage(
                code=tick.code,
                date_time=datetime.strftime(tick.datetime, DATE_TIME_FORMAT),
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
            qos=0,
        )

    def future_quote_callback_v1(
        self,
        _,
        tick: sj.TickFOPv1,
    ):
        self.mqttc.publish(
            f"{EXCAHNG_TYPE}/{ROUTING_KEY_FUTURE_TICK}/{tick.code}",
            mq_pb2.FutureRealTimeTickMessage(
                code=tick.code,
                date_time=datetime.strftime(tick.datetime, DATE_TIME_FORMAT),
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
            qos=0,
        )

    def stock_bid_ask_callback(
        self,
        _,
        bidask: sj.BidAskSTKv1,
    ):
        key = f"{EXCAHNG_TYPE}/{ROUTING_KEY_STOCK_BID_ASK}/{bidask.code}"
        if bidask.intraday_odd is True:
            key = f"{EXCAHNG_TYPE}/{ROUTING_KEY_STOCK_BID_ASK_ODDS}/{bidask.code}"
        self.mqttc.publish(
            key,
            mq_pb2.StockRealTimeBidAskMessage(
                code=bidask.code,
                date_time=datetime.strftime(bidask.datetime, DATE_TIME_FORMAT),
                suspend=bidask.suspend,
                simtrade=bidask.simtrade,
                bid_price=bidask.bid_price,
                bid_volume=bidask.bid_volume,
                diff_bid_vol=bidask.diff_bid_vol,
                ask_price=bidask.ask_price,
                ask_volume=bidask.ask_volume,
                diff_ask_vol=bidask.diff_ask_vol,
            ).SerializeToString(),
            qos=0,
        )

    def future_bid_ask_callback(
        self,
        _,
        bidask: sj.BidAskFOPv1,
    ):
        self.mqttc.publish(
            f"{EXCAHNG_TYPE}/{ROUTING_KEY_FUTURE_BID_ASK}/{bidask.code}",
            mq_pb2.FutureRealTimeBidAskMessage(
                code=bidask.code,
                date_time=datetime.strftime(bidask.datetime, DATE_TIME_FORMAT),
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
            qos=0,
        )

    def order_status_callback(
        self,
        reply: list[sj.order.Trade],
    ):
        self.send_order_arr(reply)

    def send_order_arr(
        self,
        arr: list[sj.order.Trade],
    ):
        if len(arr) == 0:
            return
        with self.order_cb_lock:
            result = mq_pb2.OrderStatusArr()
            for order in arr:
                if order.status.order_datetime is None:
                    order.status.order_datetime = datetime.now()

                order_price = int()
                if order.status.modified_price != 0:
                    order_price = order.status.modified_price
                else:
                    order_price = order.order.price

                if len(order.status.deals) > 0:
                    order_price = order.status.deals[0].price

                qty = order.order.quantity
                if order.status.deal_quantity not in (0, qty):
                    qty = order.status.deal_quantity

                if order.status.order_datetime.hour < 5 and order.status.order_datetime.hour >= 0:
                    if order.status.order_datetime.day != datetime.now().day:
                        order.status.order_datetime = order.status.order_datetime + timedelta(days=1)

                order_type = mq_pb2.OrderType.TYPE_UNKNOWN
                if order.contract.security_type == sc.SecurityType.Stock:
                    if order.order.order_lot in (sj.order.StockOrderLot.Odd, sj.order.StockOrderLot.IntradayOdd):
                        order_type = mq_pb2.OrderType.TYPE_STOCK_SHARE
                    else:
                        order_type = mq_pb2.OrderType.TYPE_STOCK_LOT
                if order.contract.security_type == sc.SecurityType.Future:
                    order_type = mq_pb2.OrderType.TYPE_FUTURE

                result.data.append(
                    mq_pb2.OrderStatus(
                        type=order_type,
                        code=order.contract.code,
                        action=order.order.action,
                        price=order_price,
                        quantity=qty,
                        order_id=order.status.id,
                        status=order.status.status,
                        order_time=datetime.strftime(
                            order.status.order_datetime,
                            "%Y-%m-%d %H:%M:%S",
                        ),
                    )
                )
            self.mqttc.publish(
                f"{EXCAHNG_TYPE}/{ROUTING_KEY_ORDER_ARR}",
                result.SerializeToString(),
                qos=0,
            )
