from google.protobuf import empty_pb2 as _empty_pb2
import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SnapshotMessage(_message.Message):
    __slots__ = ["amount", "average_price", "buy_price", "buy_volume", "change_price", "change_rate", "change_type", "close", "code", "exchange", "high", "low", "open", "sell_price", "sell_volume", "tick_type", "total_amount", "total_volume", "ts", "volume", "volume_ratio", "yesterday_volume"]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_PRICE_FIELD_NUMBER: _ClassVar[int]
    BUY_PRICE_FIELD_NUMBER: _ClassVar[int]
    BUY_VOLUME_FIELD_NUMBER: _ClassVar[int]
    CHANGE_PRICE_FIELD_NUMBER: _ClassVar[int]
    CHANGE_RATE_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    EXCHANGE_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    SELL_PRICE_FIELD_NUMBER: _ClassVar[int]
    SELL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    TICK_TYPE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    VOLUME_RATIO_FIELD_NUMBER: _ClassVar[int]
    YESTERDAY_VOLUME_FIELD_NUMBER: _ClassVar[int]
    amount: int
    average_price: float
    buy_price: float
    buy_volume: float
    change_price: float
    change_rate: float
    change_type: str
    close: float
    code: str
    exchange: str
    high: float
    low: float
    open: float
    sell_price: float
    sell_volume: int
    tick_type: str
    total_amount: int
    total_volume: int
    ts: int
    volume: int
    volume_ratio: float
    yesterday_volume: float
    def __init__(self, ts: _Optional[int] = ..., code: _Optional[str] = ..., exchange: _Optional[str] = ..., open: _Optional[float] = ..., high: _Optional[float] = ..., low: _Optional[float] = ..., close: _Optional[float] = ..., tick_type: _Optional[str] = ..., change_price: _Optional[float] = ..., change_rate: _Optional[float] = ..., change_type: _Optional[str] = ..., average_price: _Optional[float] = ..., volume: _Optional[int] = ..., total_volume: _Optional[int] = ..., amount: _Optional[int] = ..., total_amount: _Optional[int] = ..., yesterday_volume: _Optional[float] = ..., buy_price: _Optional[float] = ..., buy_volume: _Optional[float] = ..., sell_price: _Optional[float] = ..., sell_volume: _Optional[int] = ..., volume_ratio: _Optional[float] = ...) -> None: ...

class SnapshotResponse(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[SnapshotMessage]
    def __init__(self, data: _Optional[_Iterable[_Union[SnapshotMessage, _Mapping]]] = ...) -> None: ...

class StockVolumeRankMessage(_message.Message):
    __slots__ = ["amount", "ask_orders", "ask_volumes", "average_price", "bid_orders", "bid_volumes", "buy_price", "buy_volume", "change_price", "change_type", "close", "code", "date", "high", "low", "name", "open", "price_range", "sell_price", "sell_volume", "tick_type", "total_amount", "total_volume", "ts", "volume", "volume_ratio", "yesterday_volume"]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    ASK_ORDERS_FIELD_NUMBER: _ClassVar[int]
    ASK_VOLUMES_FIELD_NUMBER: _ClassVar[int]
    AVERAGE_PRICE_FIELD_NUMBER: _ClassVar[int]
    BID_ORDERS_FIELD_NUMBER: _ClassVar[int]
    BID_VOLUMES_FIELD_NUMBER: _ClassVar[int]
    BUY_PRICE_FIELD_NUMBER: _ClassVar[int]
    BUY_VOLUME_FIELD_NUMBER: _ClassVar[int]
    CHANGE_PRICE_FIELD_NUMBER: _ClassVar[int]
    CHANGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    PRICE_RANGE_FIELD_NUMBER: _ClassVar[int]
    SELL_PRICE_FIELD_NUMBER: _ClassVar[int]
    SELL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    TICK_TYPE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    VOLUME_RATIO_FIELD_NUMBER: _ClassVar[int]
    YESTERDAY_VOLUME_FIELD_NUMBER: _ClassVar[int]
    amount: int
    ask_orders: int
    ask_volumes: int
    average_price: float
    bid_orders: int
    bid_volumes: int
    buy_price: float
    buy_volume: int
    change_price: float
    change_type: int
    close: float
    code: str
    date: str
    high: float
    low: float
    name: str
    open: float
    price_range: float
    sell_price: float
    sell_volume: int
    tick_type: int
    total_amount: int
    total_volume: int
    ts: int
    volume: int
    volume_ratio: float
    yesterday_volume: int
    def __init__(self, date: _Optional[str] = ..., code: _Optional[str] = ..., name: _Optional[str] = ..., ts: _Optional[int] = ..., open: _Optional[float] = ..., high: _Optional[float] = ..., low: _Optional[float] = ..., close: _Optional[float] = ..., price_range: _Optional[float] = ..., tick_type: _Optional[int] = ..., change_price: _Optional[float] = ..., change_type: _Optional[int] = ..., average_price: _Optional[float] = ..., volume: _Optional[int] = ..., total_volume: _Optional[int] = ..., amount: _Optional[int] = ..., total_amount: _Optional[int] = ..., yesterday_volume: _Optional[int] = ..., volume_ratio: _Optional[float] = ..., buy_price: _Optional[float] = ..., buy_volume: _Optional[int] = ..., sell_price: _Optional[float] = ..., sell_volume: _Optional[int] = ..., bid_orders: _Optional[int] = ..., bid_volumes: _Optional[int] = ..., ask_orders: _Optional[int] = ..., ask_volumes: _Optional[int] = ...) -> None: ...

class StockVolumeRankResponse(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[StockVolumeRankMessage]
    def __init__(self, data: _Optional[_Iterable[_Union[StockVolumeRankMessage, _Mapping]]] = ...) -> None: ...

class SubscribeResponse(_message.Message):
    __slots__ = ["fail_arr"]
    FAIL_ARR_FIELD_NUMBER: _ClassVar[int]
    fail_arr: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, fail_arr: _Optional[_Iterable[str]] = ...) -> None: ...

class VolumeRankRequest(_message.Message):
    __slots__ = ["count", "date"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    count: int
    date: str
    def __init__(self, count: _Optional[int] = ..., date: _Optional[str] = ...) -> None: ...

class YahooFinancePrice(_message.Message):
    __slots__ = ["last", "price"]
    LAST_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    last: float
    price: float
    def __init__(self, price: _Optional[float] = ..., last: _Optional[float] = ...) -> None: ...
