from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
TYPE_ASSIST_STATUS: WSType
TYPE_ERR_MESSAGE: WSType
TYPE_FUTURE_DETAIL: WSType
TYPE_FUTURE_ORDER: WSType
TYPE_FUTURE_POSITION: WSType
TYPE_FUTURE_TICK: WSType
TYPE_KBAR_ARR: WSType
TYPE_TRADE_INDEX: WSType

class Kbar(_message.Message):
    __slots__ = ["close", "high", "kbar_time", "low", "open", "volume"]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    KBAR_TIME_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    close: float
    high: float
    kbar_time: str
    low: float
    open: float
    volume: int
    def __init__(self, kbar_time: _Optional[str] = ..., open: _Optional[float] = ..., high: _Optional[float] = ..., close: _Optional[float] = ..., low: _Optional[float] = ..., volume: _Optional[int] = ...) -> None: ...

class Position(_message.Message):
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

class WSAssitStatus(_message.Message):
    __slots__ = ["running"]
    RUNNING_FIELD_NUMBER: _ClassVar[int]
    running: bool
    def __init__(self, running: bool = ...) -> None: ...

class WSErrMessage(_message.Message):
    __slots__ = ["err_code", "response"]
    ERR_CODE_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    err_code: int
    response: str
    def __init__(self, err_code: _Optional[int] = ..., response: _Optional[str] = ...) -> None: ...

class WSFutureDetail(_message.Message):
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

class WSFutureOrder(_message.Message):
    __slots__ = ["base_order", "code"]
    BASE_ORDER_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    base_order: WSOrder
    code: str
    def __init__(self, code: _Optional[str] = ..., base_order: _Optional[_Union[WSOrder, _Mapping]] = ...) -> None: ...

class WSFuturePosition(_message.Message):
    __slots__ = ["position"]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    position: _containers.RepeatedCompositeFieldContainer[Position]
    def __init__(self, position: _Optional[_Iterable[_Union[Position, _Mapping]]] = ...) -> None: ...

class WSFutureTick(_message.Message):
    __slots__ = ["amount", "ask_side_total_vol", "avg_price", "bid_side_total_vol", "chg_type", "close", "code", "high", "low", "open", "pct_chg", "price_chg", "tick_time", "tick_type", "total_amount", "total_volume", "underlying_price", "volume"]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    ASK_SIDE_TOTAL_VOL_FIELD_NUMBER: _ClassVar[int]
    AVG_PRICE_FIELD_NUMBER: _ClassVar[int]
    BID_SIDE_TOTAL_VOL_FIELD_NUMBER: _ClassVar[int]
    CHG_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    PCT_CHG_FIELD_NUMBER: _ClassVar[int]
    PRICE_CHG_FIELD_NUMBER: _ClassVar[int]
    TICK_TIME_FIELD_NUMBER: _ClassVar[int]
    TICK_TYPE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    UNDERLYING_PRICE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    amount: float
    ask_side_total_vol: int
    avg_price: float
    bid_side_total_vol: int
    chg_type: int
    close: float
    code: str
    high: float
    low: float
    open: float
    pct_chg: float
    price_chg: float
    tick_time: str
    tick_type: int
    total_amount: float
    total_volume: int
    underlying_price: float
    volume: int
    def __init__(self, code: _Optional[str] = ..., tick_time: _Optional[str] = ..., open: _Optional[float] = ..., underlying_price: _Optional[float] = ..., bid_side_total_vol: _Optional[int] = ..., ask_side_total_vol: _Optional[int] = ..., avg_price: _Optional[float] = ..., close: _Optional[float] = ..., high: _Optional[float] = ..., low: _Optional[float] = ..., amount: _Optional[float] = ..., total_amount: _Optional[float] = ..., volume: _Optional[int] = ..., total_volume: _Optional[int] = ..., tick_type: _Optional[int] = ..., chg_type: _Optional[int] = ..., price_chg: _Optional[float] = ..., pct_chg: _Optional[float] = ...) -> None: ...

class WSHistoryKbarMessage(_message.Message):
    __slots__ = ["arr"]
    ARR_FIELD_NUMBER: _ClassVar[int]
    arr: _containers.RepeatedCompositeFieldContainer[Kbar]
    def __init__(self, arr: _Optional[_Iterable[_Union[Kbar, _Mapping]]] = ...) -> None: ...

class WSIndexStatus(_message.Message):
    __slots__ = ["break_count", "price_chg"]
    BREAK_COUNT_FIELD_NUMBER: _ClassVar[int]
    PRICE_CHG_FIELD_NUMBER: _ClassVar[int]
    break_count: int
    price_chg: float
    def __init__(self, break_count: _Optional[int] = ..., price_chg: _Optional[float] = ...) -> None: ...

class WSMessage(_message.Message):
    __slots__ = ["assit_status", "err_message", "future_detail", "future_order", "future_position", "future_tick", "history_kbar", "trade_index", "type"]
    ASSIT_STATUS_FIELD_NUMBER: _ClassVar[int]
    ERR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FUTURE_DETAIL_FIELD_NUMBER: _ClassVar[int]
    FUTURE_ORDER_FIELD_NUMBER: _ClassVar[int]
    FUTURE_POSITION_FIELD_NUMBER: _ClassVar[int]
    FUTURE_TICK_FIELD_NUMBER: _ClassVar[int]
    HISTORY_KBAR_FIELD_NUMBER: _ClassVar[int]
    TRADE_INDEX_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    assit_status: WSAssitStatus
    err_message: WSErrMessage
    future_detail: WSFutureDetail
    future_order: WSFutureOrder
    future_position: WSFuturePosition
    future_tick: WSFutureTick
    history_kbar: WSHistoryKbarMessage
    trade_index: WSTradeIndex
    type: WSType
    def __init__(self, type: _Optional[_Union[WSType, str]] = ..., future_tick: _Optional[_Union[WSFutureTick, _Mapping]] = ..., future_order: _Optional[_Union[WSFutureOrder, _Mapping]] = ..., trade_index: _Optional[_Union[WSTradeIndex, _Mapping]] = ..., future_position: _Optional[_Union[WSFuturePosition, _Mapping]] = ..., assit_status: _Optional[_Union[WSAssitStatus, _Mapping]] = ..., err_message: _Optional[_Union[WSErrMessage, _Mapping]] = ..., history_kbar: _Optional[_Union[WSHistoryKbarMessage, _Mapping]] = ..., future_detail: _Optional[_Union[WSFutureDetail, _Mapping]] = ...) -> None: ...

class WSOrder(_message.Message):
    __slots__ = ["action", "group_id", "order_id", "order_time", "price", "quantity", "status", "tick_time", "trade_time"]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    GROUP_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_TIME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TICK_TIME_FIELD_NUMBER: _ClassVar[int]
    TRADE_TIME_FIELD_NUMBER: _ClassVar[int]
    action: int
    group_id: str
    order_id: str
    order_time: str
    price: float
    quantity: int
    status: int
    tick_time: str
    trade_time: str
    def __init__(self, order_id: _Optional[str] = ..., status: _Optional[int] = ..., order_time: _Optional[str] = ..., action: _Optional[int] = ..., price: _Optional[float] = ..., quantity: _Optional[int] = ..., trade_time: _Optional[str] = ..., tick_time: _Optional[str] = ..., group_id: _Optional[str] = ...) -> None: ...

class WSTradeIndex(_message.Message):
    __slots__ = ["nasdaq", "nf", "otc", "tse"]
    NASDAQ_FIELD_NUMBER: _ClassVar[int]
    NF_FIELD_NUMBER: _ClassVar[int]
    OTC_FIELD_NUMBER: _ClassVar[int]
    TSE_FIELD_NUMBER: _ClassVar[int]
    nasdaq: WSIndexStatus
    nf: WSIndexStatus
    otc: WSIndexStatus
    tse: WSIndexStatus
    def __init__(self, tse: _Optional[_Union[WSIndexStatus, _Mapping]] = ..., otc: _Optional[_Union[WSIndexStatus, _Mapping]] = ..., nasdaq: _Optional[_Union[WSIndexStatus, _Mapping]] = ..., nf: _Optional[_Union[WSIndexStatus, _Mapping]] = ...) -> None: ...

class WSType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
