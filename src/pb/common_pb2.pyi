from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Date(_message.Message):
    __slots__ = ["date"]
    DATE_FIELD_NUMBER: _ClassVar[int]
    date: str
    def __init__(self, date: _Optional[str] = ...) -> None: ...

class ErrorMessage(_message.Message):
    __slots__ = ["err"]
    ERR_FIELD_NUMBER: _ClassVar[int]
    err: str
    def __init__(self, err: _Optional[str] = ...) -> None: ...

class EventMessage(_message.Message):
    __slots__ = ["event", "event_code", "event_time", "info", "resp_code"]
    EVENT_CODE_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    EVENT_TIME_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    RESP_CODE_FIELD_NUMBER: _ClassVar[int]
    event: str
    event_code: int
    event_time: str
    info: str
    resp_code: int
    def __init__(self, resp_code: _Optional[int] = ..., event_code: _Optional[int] = ..., info: _Optional[str] = ..., event: _Optional[str] = ..., event_time: _Optional[str] = ...) -> None: ...

class FutureCodeArr(_message.Message):
    __slots__ = ["future_code_arr"]
    FUTURE_CODE_ARR_FIELD_NUMBER: _ClassVar[int]
    future_code_arr: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, future_code_arr: _Optional[_Iterable[str]] = ...) -> None: ...

class FutureCodeArrWithDate(_message.Message):
    __slots__ = ["date", "future_code_arr"]
    DATE_FIELD_NUMBER: _ClassVar[int]
    FUTURE_CODE_ARR_FIELD_NUMBER: _ClassVar[int]
    date: str
    future_code_arr: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, future_code_arr: _Optional[_Iterable[str]] = ..., date: _Optional[str] = ...) -> None: ...

class FutureRealTimeBidAskMessage(_message.Message):
    __slots__ = ["ask_price", "ask_total_vol", "ask_volume", "bid_price", "bid_total_vol", "bid_volume", "code", "date_time", "diff_ask_vol", "diff_bid_vol", "first_derived_ask_price", "first_derived_ask_vol", "first_derived_bid_price", "first_derived_bid_vol", "simtrade", "underlying_price"]
    ASK_PRICE_FIELD_NUMBER: _ClassVar[int]
    ASK_TOTAL_VOL_FIELD_NUMBER: _ClassVar[int]
    ASK_VOLUME_FIELD_NUMBER: _ClassVar[int]
    BID_PRICE_FIELD_NUMBER: _ClassVar[int]
    BID_TOTAL_VOL_FIELD_NUMBER: _ClassVar[int]
    BID_VOLUME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DIFF_ASK_VOL_FIELD_NUMBER: _ClassVar[int]
    DIFF_BID_VOL_FIELD_NUMBER: _ClassVar[int]
    FIRST_DERIVED_ASK_PRICE_FIELD_NUMBER: _ClassVar[int]
    FIRST_DERIVED_ASK_VOL_FIELD_NUMBER: _ClassVar[int]
    FIRST_DERIVED_BID_PRICE_FIELD_NUMBER: _ClassVar[int]
    FIRST_DERIVED_BID_VOL_FIELD_NUMBER: _ClassVar[int]
    SIMTRADE_FIELD_NUMBER: _ClassVar[int]
    UNDERLYING_PRICE_FIELD_NUMBER: _ClassVar[int]
    ask_price: _containers.RepeatedScalarFieldContainer[float]
    ask_total_vol: int
    ask_volume: _containers.RepeatedScalarFieldContainer[int]
    bid_price: _containers.RepeatedScalarFieldContainer[float]
    bid_total_vol: int
    bid_volume: _containers.RepeatedScalarFieldContainer[int]
    code: str
    date_time: str
    diff_ask_vol: _containers.RepeatedScalarFieldContainer[int]
    diff_bid_vol: _containers.RepeatedScalarFieldContainer[int]
    first_derived_ask_price: float
    first_derived_ask_vol: int
    first_derived_bid_price: float
    first_derived_bid_vol: int
    simtrade: bool
    underlying_price: float
    def __init__(self, code: _Optional[str] = ..., date_time: _Optional[str] = ..., bid_total_vol: _Optional[int] = ..., ask_total_vol: _Optional[int] = ..., bid_price: _Optional[_Iterable[float]] = ..., bid_volume: _Optional[_Iterable[int]] = ..., diff_bid_vol: _Optional[_Iterable[int]] = ..., ask_price: _Optional[_Iterable[float]] = ..., ask_volume: _Optional[_Iterable[int]] = ..., diff_ask_vol: _Optional[_Iterable[int]] = ..., first_derived_bid_price: _Optional[float] = ..., first_derived_ask_price: _Optional[float] = ..., first_derived_bid_vol: _Optional[int] = ..., first_derived_ask_vol: _Optional[int] = ..., underlying_price: _Optional[float] = ..., simtrade: bool = ...) -> None: ...

class FutureRealTimeTickMessage(_message.Message):
    __slots__ = ["amount", "ask_side_total_vol", "avg_price", "bid_side_total_vol", "chg_type", "close", "code", "date_time", "high", "low", "open", "pct_chg", "price_chg", "simtrade", "tick_type", "total_amount", "total_volume", "underlying_price", "volume"]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    ASK_SIDE_TOTAL_VOL_FIELD_NUMBER: _ClassVar[int]
    AVG_PRICE_FIELD_NUMBER: _ClassVar[int]
    BID_SIDE_TOTAL_VOL_FIELD_NUMBER: _ClassVar[int]
    CHG_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATE_TIME_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    PCT_CHG_FIELD_NUMBER: _ClassVar[int]
    PRICE_CHG_FIELD_NUMBER: _ClassVar[int]
    SIMTRADE_FIELD_NUMBER: _ClassVar[int]
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
    date_time: str
    high: float
    low: float
    open: float
    pct_chg: float
    price_chg: float
    simtrade: bool
    tick_type: int
    total_amount: float
    total_volume: int
    underlying_price: float
    volume: int
    def __init__(self, code: _Optional[str] = ..., date_time: _Optional[str] = ..., open: _Optional[float] = ..., underlying_price: _Optional[float] = ..., bid_side_total_vol: _Optional[int] = ..., ask_side_total_vol: _Optional[int] = ..., avg_price: _Optional[float] = ..., close: _Optional[float] = ..., high: _Optional[float] = ..., low: _Optional[float] = ..., amount: _Optional[float] = ..., total_amount: _Optional[float] = ..., volume: _Optional[int] = ..., total_volume: _Optional[int] = ..., tick_type: _Optional[int] = ..., chg_type: _Optional[int] = ..., price_chg: _Optional[float] = ..., pct_chg: _Optional[float] = ..., simtrade: bool = ...) -> None: ...

class StockNumArr(_message.Message):
    __slots__ = ["stock_num_arr"]
    STOCK_NUM_ARR_FIELD_NUMBER: _ClassVar[int]
    stock_num_arr: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, stock_num_arr: _Optional[_Iterable[str]] = ...) -> None: ...

class StockNumArrWithDate(_message.Message):
    __slots__ = ["date", "stock_num_arr"]
    DATE_FIELD_NUMBER: _ClassVar[int]
    STOCK_NUM_ARR_FIELD_NUMBER: _ClassVar[int]
    date: str
    stock_num_arr: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, stock_num_arr: _Optional[_Iterable[str]] = ..., date: _Optional[str] = ...) -> None: ...

class StockNumArrWithDateArr(_message.Message):
    __slots__ = ["date_arr", "stock_num_arr"]
    DATE_ARR_FIELD_NUMBER: _ClassVar[int]
    STOCK_NUM_ARR_FIELD_NUMBER: _ClassVar[int]
    date_arr: _containers.RepeatedScalarFieldContainer[str]
    stock_num_arr: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, stock_num_arr: _Optional[_Iterable[str]] = ..., date_arr: _Optional[_Iterable[str]] = ...) -> None: ...

class StockRealTimeBidAskMessage(_message.Message):
    __slots__ = ["ask_price", "ask_volume", "bid_price", "bid_volume", "code", "date_time", "diff_ask_vol", "diff_bid_vol", "simtrade", "suspend"]
    ASK_PRICE_FIELD_NUMBER: _ClassVar[int]
    ASK_VOLUME_FIELD_NUMBER: _ClassVar[int]
    BID_PRICE_FIELD_NUMBER: _ClassVar[int]
    BID_VOLUME_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATE_TIME_FIELD_NUMBER: _ClassVar[int]
    DIFF_ASK_VOL_FIELD_NUMBER: _ClassVar[int]
    DIFF_BID_VOL_FIELD_NUMBER: _ClassVar[int]
    SIMTRADE_FIELD_NUMBER: _ClassVar[int]
    SUSPEND_FIELD_NUMBER: _ClassVar[int]
    ask_price: _containers.RepeatedScalarFieldContainer[float]
    ask_volume: _containers.RepeatedScalarFieldContainer[int]
    bid_price: _containers.RepeatedScalarFieldContainer[float]
    bid_volume: _containers.RepeatedScalarFieldContainer[int]
    code: str
    date_time: str
    diff_ask_vol: _containers.RepeatedScalarFieldContainer[int]
    diff_bid_vol: _containers.RepeatedScalarFieldContainer[int]
    simtrade: bool
    suspend: bool
    def __init__(self, code: _Optional[str] = ..., date_time: _Optional[str] = ..., bid_price: _Optional[_Iterable[float]] = ..., bid_volume: _Optional[_Iterable[int]] = ..., diff_bid_vol: _Optional[_Iterable[int]] = ..., ask_price: _Optional[_Iterable[float]] = ..., ask_volume: _Optional[_Iterable[int]] = ..., diff_ask_vol: _Optional[_Iterable[int]] = ..., suspend: bool = ..., simtrade: bool = ...) -> None: ...

class StockRealTimeTickMessage(_message.Message):
    __slots__ = ["amount", "ask_side_total_cnt", "ask_side_total_vol", "avg_price", "bid_side_total_cnt", "bid_side_total_vol", "chg_type", "close", "code", "date_time", "high", "low", "open", "pct_chg", "price_chg", "simtrade", "suspend", "tick_type", "total_amount", "total_volume", "volume"]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    ASK_SIDE_TOTAL_CNT_FIELD_NUMBER: _ClassVar[int]
    ASK_SIDE_TOTAL_VOL_FIELD_NUMBER: _ClassVar[int]
    AVG_PRICE_FIELD_NUMBER: _ClassVar[int]
    BID_SIDE_TOTAL_CNT_FIELD_NUMBER: _ClassVar[int]
    BID_SIDE_TOTAL_VOL_FIELD_NUMBER: _ClassVar[int]
    CHG_TYPE_FIELD_NUMBER: _ClassVar[int]
    CLOSE_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATE_TIME_FIELD_NUMBER: _ClassVar[int]
    HIGH_FIELD_NUMBER: _ClassVar[int]
    LOW_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    PCT_CHG_FIELD_NUMBER: _ClassVar[int]
    PRICE_CHG_FIELD_NUMBER: _ClassVar[int]
    SIMTRADE_FIELD_NUMBER: _ClassVar[int]
    SUSPEND_FIELD_NUMBER: _ClassVar[int]
    TICK_TYPE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_VOLUME_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    amount: float
    ask_side_total_cnt: int
    ask_side_total_vol: int
    avg_price: float
    bid_side_total_cnt: int
    bid_side_total_vol: int
    chg_type: int
    close: float
    code: str
    date_time: str
    high: float
    low: float
    open: float
    pct_chg: float
    price_chg: float
    simtrade: bool
    suspend: bool
    tick_type: int
    total_amount: float
    total_volume: int
    volume: int
    def __init__(self, code: _Optional[str] = ..., date_time: _Optional[str] = ..., open: _Optional[float] = ..., avg_price: _Optional[float] = ..., close: _Optional[float] = ..., high: _Optional[float] = ..., low: _Optional[float] = ..., amount: _Optional[float] = ..., total_amount: _Optional[float] = ..., volume: _Optional[int] = ..., total_volume: _Optional[int] = ..., tick_type: _Optional[int] = ..., chg_type: _Optional[int] = ..., price_chg: _Optional[float] = ..., pct_chg: _Optional[float] = ..., bid_side_total_vol: _Optional[int] = ..., ask_side_total_vol: _Optional[int] = ..., bid_side_total_cnt: _Optional[int] = ..., ask_side_total_cnt: _Optional[int] = ..., suspend: bool = ..., simtrade: bool = ...) -> None: ...
