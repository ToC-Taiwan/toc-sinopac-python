from google.protobuf import empty_pb2 as _empty_pb2
import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FutureOrderDetail(_message.Message):
    __slots__ = ["code", "price", "quantity", "simulate"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    SIMULATE_FIELD_NUMBER: _ClassVar[int]
    code: str
    price: float
    quantity: int
    simulate: bool
    def __init__(self, code: _Optional[str] = ..., price: _Optional[float] = ..., quantity: _Optional[int] = ..., simulate: bool = ...) -> None: ...

class FutureOrderID(_message.Message):
    __slots__ = ["order_id", "simulate"]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SIMULATE_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    simulate: bool
    def __init__(self, order_id: _Optional[str] = ..., simulate: bool = ...) -> None: ...

class FuturePosition(_message.Message):
    __slots__ = ["code", "direction", "last_price", "pnl", "price", "quantity"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    LAST_PRICE_FIELD_NUMBER: _ClassVar[int]
    PNL_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    code: str
    direction: str
    last_price: float
    pnl: float
    price: float
    quantity: int
    def __init__(self, code: _Optional[str] = ..., direction: _Optional[str] = ..., quantity: _Optional[int] = ..., price: _Optional[float] = ..., last_price: _Optional[float] = ..., pnl: _Optional[float] = ...) -> None: ...

class FuturePositionArr(_message.Message):
    __slots__ = ["position_arr"]
    POSITION_ARR_FIELD_NUMBER: _ClassVar[int]
    position_arr: _containers.RepeatedCompositeFieldContainer[FuturePosition]
    def __init__(self, position_arr: _Optional[_Iterable[_Union[FuturePosition, _Mapping]]] = ...) -> None: ...

class OrderID(_message.Message):
    __slots__ = ["order_id", "simulate"]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SIMULATE_FIELD_NUMBER: _ClassVar[int]
    order_id: str
    simulate: bool
    def __init__(self, order_id: _Optional[str] = ..., simulate: bool = ...) -> None: ...

class OrderStatus(_message.Message):
    __slots__ = ["action", "code", "order_id", "order_time", "price", "quantity", "status"]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_TIME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    action: str
    code: str
    order_id: str
    order_time: str
    price: float
    quantity: int
    status: str
    def __init__(self, status: _Optional[str] = ..., code: _Optional[str] = ..., action: _Optional[str] = ..., price: _Optional[float] = ..., quantity: _Optional[int] = ..., order_id: _Optional[str] = ..., order_time: _Optional[str] = ...) -> None: ...

class OrderStatusArr(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[OrderStatus]
    def __init__(self, data: _Optional[_Iterable[_Union[OrderStatus, _Mapping]]] = ...) -> None: ...

class StockOrderDetail(_message.Message):
    __slots__ = ["price", "quantity", "simulate", "stock_num"]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    SIMULATE_FIELD_NUMBER: _ClassVar[int]
    STOCK_NUM_FIELD_NUMBER: _ClassVar[int]
    price: float
    quantity: int
    simulate: bool
    stock_num: str
    def __init__(self, stock_num: _Optional[str] = ..., price: _Optional[float] = ..., quantity: _Optional[int] = ..., simulate: bool = ...) -> None: ...

class TradeResult(_message.Message):
    __slots__ = ["error", "order_id", "status"]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    error: str
    order_id: str
    status: str
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...
