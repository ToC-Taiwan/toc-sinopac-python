import common_pb2 as _common_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HistoryCloseMessage(_message.Message):
    __slots__ = ["close", "code", "date"]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATE_FIELD_NUMBER: _ClassVar[int]
    close: float
    code: str
    date: str
    def __init__(self, date: _Optional[str] = ..., code: _Optional[str] = ..., close: _Optional[float] = ...) -> None: ...

class HistoryCloseResponse(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[HistoryCloseMessage]
    def __init__(self, data: _Optional[_Iterable[_Union[HistoryCloseMessage, _Mapping]]] = ...) -> None: ...

class HistoryKbarMessage(_message.Message):
    __slots__ = ["close", "code", "high", "low", "open", "ts", "volume"]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    close: float
    code: str
    high: float
    low: float
    open: float
    ts: int
    volume: int
    def __init__(self, ts: _Optional[int] = ..., close: _Optional[float] = ..., open: _Optional[float] = ..., high: _Optional[float] = ..., low: _Optional[float] = ..., volume: _Optional[int] = ..., code: _Optional[str] = ...) -> None: ...

class HistoryKbarResponse(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[HistoryKbarMessage]
    def __init__(self, data: _Optional[_Iterable[_Union[HistoryKbarMessage, _Mapping]]] = ...) -> None: ...

class HistoryTickMessage(_message.Message):
    __slots__ = ["ask_price", "ask_volume", "bid_price", "bid_volume", "close", "code", "tick_type", "ts", "volume"]
    ASK_PRICE_FIELD_NUMBER: _ClassVar[int]
    ASK_VOLUME_FIELD_NUMBER: _ClassVar[int]
    BID_PRICE_FIELD_NUMBER: _ClassVar[int]
    BID_VOLUME_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    TICK_TYPE_FIELD_NUMBER: _ClassVar[int]
    TS_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    ask_price: float
    ask_volume: int
    bid_price: float
    bid_volume: int
    close: float
    code: str
    tick_type: int
    ts: int
    volume: int
    def __init__(self, ts: _Optional[int] = ..., close: _Optional[float] = ..., volume: _Optional[int] = ..., bid_price: _Optional[float] = ..., bid_volume: _Optional[int] = ..., ask_price: _Optional[float] = ..., ask_volume: _Optional[int] = ..., tick_type: _Optional[int] = ..., code: _Optional[str] = ...) -> None: ...

class HistoryTickResponse(_message.Message):
    __slots__ = ["data"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    data: _containers.RepeatedCompositeFieldContainer[HistoryTickMessage]
    def __init__(self, data: _Optional[_Iterable[_Union[HistoryTickMessage, _Mapping]]] = ...) -> None: ...
