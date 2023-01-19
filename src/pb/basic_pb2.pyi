from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FutureDetailMessage(_message.Message):
    __slots__ = ["category", "code", "delivery_date", "delivery_month", "limit_down", "limit_up", "name", "reference", "symbol", "underlying_kind", "unit", "update_date"]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_DATE_FIELD_NUMBER: _ClassVar[int]
    DELIVERY_MONTH_FIELD_NUMBER: _ClassVar[int]
    LIMIT_DOWN_FIELD_NUMBER: _ClassVar[int]
    LIMIT_UP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    UNDERLYING_KIND_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    UPDATE_DATE_FIELD_NUMBER: _ClassVar[int]
    category: str
    code: str
    delivery_date: str
    delivery_month: str
    limit_down: float
    limit_up: float
    name: str
    reference: float
    symbol: str
    underlying_kind: str
    unit: int
    update_date: str
    def __init__(self, code: _Optional[str] = ..., symbol: _Optional[str] = ..., name: _Optional[str] = ..., category: _Optional[str] = ..., delivery_month: _Optional[str] = ..., delivery_date: _Optional[str] = ..., underlying_kind: _Optional[str] = ..., unit: _Optional[int] = ..., limit_up: _Optional[float] = ..., limit_down: _Optional[float] = ..., reference: _Optional[float] = ..., update_date: _Optional[str] = ...) -> None: ...

class FutureDetailResponse(_message.Message):
    __slots__ = ["future"]
    FUTURE_FIELD_NUMBER: _ClassVar[int]
    future: _containers.RepeatedCompositeFieldContainer[FutureDetailMessage]
    def __init__(self, future: _Optional[_Iterable[_Union[FutureDetailMessage, _Mapping]]] = ...) -> None: ...

class StockDetailMessage(_message.Message):
    __slots__ = ["category", "code", "day_trade", "exchange", "name", "reference", "update_date"]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DAY_TRADE_FIELD_NUMBER: _ClassVar[int]
    EXCHANGE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FIELD_NUMBER: _ClassVar[int]
    UPDATE_DATE_FIELD_NUMBER: _ClassVar[int]
    category: str
    code: str
    day_trade: str
    exchange: str
    name: str
    reference: float
    update_date: str
    def __init__(self, exchange: _Optional[str] = ..., category: _Optional[str] = ..., code: _Optional[str] = ..., name: _Optional[str] = ..., reference: _Optional[float] = ..., update_date: _Optional[str] = ..., day_trade: _Optional[str] = ...) -> None: ...

class StockDetailResponse(_message.Message):
    __slots__ = ["stock"]
    STOCK_FIELD_NUMBER: _ClassVar[int]
    stock: _containers.RepeatedCompositeFieldContainer[StockDetailMessage]
    def __init__(self, stock: _Optional[_Iterable[_Union[StockDetailMessage, _Mapping]]] = ...) -> None: ...
