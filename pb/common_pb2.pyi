"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import builtins
import collections.abc
import google.protobuf.descriptor
import google.protobuf.internal.containers
import google.protobuf.message
import sys

if sys.version_info >= (3, 8):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class EventMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    RESP_CODE_FIELD_NUMBER: builtins.int
    EVENT_CODE_FIELD_NUMBER: builtins.int
    INFO_FIELD_NUMBER: builtins.int
    EVENT_FIELD_NUMBER: builtins.int
    EVENT_TIME_FIELD_NUMBER: builtins.int
    resp_code: builtins.int
    event_code: builtins.int
    info: builtins.str
    event: builtins.str
    event_time: builtins.str
    def __init__(
        self,
        *,
        resp_code: builtins.int = ...,
        event_code: builtins.int = ...,
        info: builtins.str = ...,
        event: builtins.str = ...,
        event_time: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["event", b"event", "event_code", b"event_code", "event_time", b"event_time", "info", b"info", "resp_code", b"resp_code"]) -> None: ...

global___EventMessage = EventMessage

class StockRealTimeTickMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CODE_FIELD_NUMBER: builtins.int
    DATE_TIME_FIELD_NUMBER: builtins.int
    OPEN_FIELD_NUMBER: builtins.int
    AVG_PRICE_FIELD_NUMBER: builtins.int
    CLOSE_FIELD_NUMBER: builtins.int
    HIGH_FIELD_NUMBER: builtins.int
    LOW_FIELD_NUMBER: builtins.int
    AMOUNT_FIELD_NUMBER: builtins.int
    TOTAL_AMOUNT_FIELD_NUMBER: builtins.int
    VOLUME_FIELD_NUMBER: builtins.int
    TOTAL_VOLUME_FIELD_NUMBER: builtins.int
    TICK_TYPE_FIELD_NUMBER: builtins.int
    CHG_TYPE_FIELD_NUMBER: builtins.int
    PRICE_CHG_FIELD_NUMBER: builtins.int
    PCT_CHG_FIELD_NUMBER: builtins.int
    BID_SIDE_TOTAL_VOL_FIELD_NUMBER: builtins.int
    ASK_SIDE_TOTAL_VOL_FIELD_NUMBER: builtins.int
    BID_SIDE_TOTAL_CNT_FIELD_NUMBER: builtins.int
    ASK_SIDE_TOTAL_CNT_FIELD_NUMBER: builtins.int
    SUSPEND_FIELD_NUMBER: builtins.int
    SIMTRADE_FIELD_NUMBER: builtins.int
    code: builtins.str
    date_time: builtins.str
    open: builtins.float
    avg_price: builtins.float
    close: builtins.float
    high: builtins.float
    low: builtins.float
    amount: builtins.float
    total_amount: builtins.float
    volume: builtins.int
    total_volume: builtins.int
    tick_type: builtins.int
    chg_type: builtins.int
    price_chg: builtins.float
    pct_chg: builtins.float
    bid_side_total_vol: builtins.int
    ask_side_total_vol: builtins.int
    bid_side_total_cnt: builtins.int
    ask_side_total_cnt: builtins.int
    suspend: builtins.int
    simtrade: builtins.int
    def __init__(
        self,
        *,
        code: builtins.str = ...,
        date_time: builtins.str = ...,
        open: builtins.float = ...,
        avg_price: builtins.float = ...,
        close: builtins.float = ...,
        high: builtins.float = ...,
        low: builtins.float = ...,
        amount: builtins.float = ...,
        total_amount: builtins.float = ...,
        volume: builtins.int = ...,
        total_volume: builtins.int = ...,
        tick_type: builtins.int = ...,
        chg_type: builtins.int = ...,
        price_chg: builtins.float = ...,
        pct_chg: builtins.float = ...,
        bid_side_total_vol: builtins.int = ...,
        ask_side_total_vol: builtins.int = ...,
        bid_side_total_cnt: builtins.int = ...,
        ask_side_total_cnt: builtins.int = ...,
        suspend: builtins.int = ...,
        simtrade: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["amount", b"amount", "ask_side_total_cnt", b"ask_side_total_cnt", "ask_side_total_vol", b"ask_side_total_vol", "avg_price", b"avg_price", "bid_side_total_cnt", b"bid_side_total_cnt", "bid_side_total_vol", b"bid_side_total_vol", "chg_type", b"chg_type", "close", b"close", "code", b"code", "date_time", b"date_time", "high", b"high", "low", b"low", "open", b"open", "pct_chg", b"pct_chg", "price_chg", b"price_chg", "simtrade", b"simtrade", "suspend", b"suspend", "tick_type", b"tick_type", "total_amount", b"total_amount", "total_volume", b"total_volume", "volume", b"volume"]) -> None: ...

global___StockRealTimeTickMessage = StockRealTimeTickMessage

class FutureRealTimeTickMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CODE_FIELD_NUMBER: builtins.int
    DATE_TIME_FIELD_NUMBER: builtins.int
    OPEN_FIELD_NUMBER: builtins.int
    UNDERLYING_PRICE_FIELD_NUMBER: builtins.int
    BID_SIDE_TOTAL_VOL_FIELD_NUMBER: builtins.int
    ASK_SIDE_TOTAL_VOL_FIELD_NUMBER: builtins.int
    AVG_PRICE_FIELD_NUMBER: builtins.int
    CLOSE_FIELD_NUMBER: builtins.int
    HIGH_FIELD_NUMBER: builtins.int
    LOW_FIELD_NUMBER: builtins.int
    AMOUNT_FIELD_NUMBER: builtins.int
    TOTAL_AMOUNT_FIELD_NUMBER: builtins.int
    VOLUME_FIELD_NUMBER: builtins.int
    TOTAL_VOLUME_FIELD_NUMBER: builtins.int
    TICK_TYPE_FIELD_NUMBER: builtins.int
    CHG_TYPE_FIELD_NUMBER: builtins.int
    PRICE_CHG_FIELD_NUMBER: builtins.int
    PCT_CHG_FIELD_NUMBER: builtins.int
    SIMTRADE_FIELD_NUMBER: builtins.int
    code: builtins.str
    date_time: builtins.str
    open: builtins.float
    underlying_price: builtins.float
    bid_side_total_vol: builtins.int
    ask_side_total_vol: builtins.int
    avg_price: builtins.float
    close: builtins.float
    high: builtins.float
    low: builtins.float
    amount: builtins.float
    total_amount: builtins.float
    volume: builtins.int
    total_volume: builtins.int
    tick_type: builtins.int
    chg_type: builtins.int
    price_chg: builtins.float
    pct_chg: builtins.float
    simtrade: builtins.int
    def __init__(
        self,
        *,
        code: builtins.str = ...,
        date_time: builtins.str = ...,
        open: builtins.float = ...,
        underlying_price: builtins.float = ...,
        bid_side_total_vol: builtins.int = ...,
        ask_side_total_vol: builtins.int = ...,
        avg_price: builtins.float = ...,
        close: builtins.float = ...,
        high: builtins.float = ...,
        low: builtins.float = ...,
        amount: builtins.float = ...,
        total_amount: builtins.float = ...,
        volume: builtins.int = ...,
        total_volume: builtins.int = ...,
        tick_type: builtins.int = ...,
        chg_type: builtins.int = ...,
        price_chg: builtins.float = ...,
        pct_chg: builtins.float = ...,
        simtrade: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["amount", b"amount", "ask_side_total_vol", b"ask_side_total_vol", "avg_price", b"avg_price", "bid_side_total_vol", b"bid_side_total_vol", "chg_type", b"chg_type", "close", b"close", "code", b"code", "date_time", b"date_time", "high", b"high", "low", b"low", "open", b"open", "pct_chg", b"pct_chg", "price_chg", b"price_chg", "simtrade", b"simtrade", "tick_type", b"tick_type", "total_amount", b"total_amount", "total_volume", b"total_volume", "underlying_price", b"underlying_price", "volume", b"volume"]) -> None: ...

global___FutureRealTimeTickMessage = FutureRealTimeTickMessage

class StockRealTimeBidAskMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CODE_FIELD_NUMBER: builtins.int
    DATE_TIME_FIELD_NUMBER: builtins.int
    BID_PRICE_FIELD_NUMBER: builtins.int
    BID_VOLUME_FIELD_NUMBER: builtins.int
    DIFF_BID_VOL_FIELD_NUMBER: builtins.int
    ASK_PRICE_FIELD_NUMBER: builtins.int
    ASK_VOLUME_FIELD_NUMBER: builtins.int
    DIFF_ASK_VOL_FIELD_NUMBER: builtins.int
    SUSPEND_FIELD_NUMBER: builtins.int
    SIMTRADE_FIELD_NUMBER: builtins.int
    code: builtins.str
    date_time: builtins.str
    @property
    def bid_price(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    @property
    def bid_volume(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    @property
    def diff_bid_vol(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    @property
    def ask_price(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    @property
    def ask_volume(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    @property
    def diff_ask_vol(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    suspend: builtins.int
    simtrade: builtins.int
    def __init__(
        self,
        *,
        code: builtins.str = ...,
        date_time: builtins.str = ...,
        bid_price: collections.abc.Iterable[builtins.float] | None = ...,
        bid_volume: collections.abc.Iterable[builtins.int] | None = ...,
        diff_bid_vol: collections.abc.Iterable[builtins.int] | None = ...,
        ask_price: collections.abc.Iterable[builtins.float] | None = ...,
        ask_volume: collections.abc.Iterable[builtins.int] | None = ...,
        diff_ask_vol: collections.abc.Iterable[builtins.int] | None = ...,
        suspend: builtins.int = ...,
        simtrade: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["ask_price", b"ask_price", "ask_volume", b"ask_volume", "bid_price", b"bid_price", "bid_volume", b"bid_volume", "code", b"code", "date_time", b"date_time", "diff_ask_vol", b"diff_ask_vol", "diff_bid_vol", b"diff_bid_vol", "simtrade", b"simtrade", "suspend", b"suspend"]) -> None: ...

global___StockRealTimeBidAskMessage = StockRealTimeBidAskMessage

class FutureRealTimeBidAskMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    CODE_FIELD_NUMBER: builtins.int
    DATE_TIME_FIELD_NUMBER: builtins.int
    BID_TOTAL_VOL_FIELD_NUMBER: builtins.int
    ASK_TOTAL_VOL_FIELD_NUMBER: builtins.int
    BID_PRICE_FIELD_NUMBER: builtins.int
    BID_VOLUME_FIELD_NUMBER: builtins.int
    DIFF_BID_VOL_FIELD_NUMBER: builtins.int
    ASK_PRICE_FIELD_NUMBER: builtins.int
    ASK_VOLUME_FIELD_NUMBER: builtins.int
    DIFF_ASK_VOL_FIELD_NUMBER: builtins.int
    FIRST_DERIVED_BID_PRICE_FIELD_NUMBER: builtins.int
    FIRST_DERIVED_ASK_PRICE_FIELD_NUMBER: builtins.int
    FIRST_DERIVED_BID_VOL_FIELD_NUMBER: builtins.int
    FIRST_DERIVED_ASK_VOL_FIELD_NUMBER: builtins.int
    UNDERLYING_PRICE_FIELD_NUMBER: builtins.int
    SIMTRADE_FIELD_NUMBER: builtins.int
    code: builtins.str
    date_time: builtins.str
    bid_total_vol: builtins.int
    ask_total_vol: builtins.int
    @property
    def bid_price(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    @property
    def bid_volume(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    @property
    def diff_bid_vol(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    @property
    def ask_price(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.float]: ...
    @property
    def ask_volume(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    @property
    def diff_ask_vol(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.int]: ...
    first_derived_bid_price: builtins.float
    first_derived_ask_price: builtins.float
    first_derived_bid_vol: builtins.int
    first_derived_ask_vol: builtins.int
    underlying_price: builtins.float
    simtrade: builtins.int
    def __init__(
        self,
        *,
        code: builtins.str = ...,
        date_time: builtins.str = ...,
        bid_total_vol: builtins.int = ...,
        ask_total_vol: builtins.int = ...,
        bid_price: collections.abc.Iterable[builtins.float] | None = ...,
        bid_volume: collections.abc.Iterable[builtins.int] | None = ...,
        diff_bid_vol: collections.abc.Iterable[builtins.int] | None = ...,
        ask_price: collections.abc.Iterable[builtins.float] | None = ...,
        ask_volume: collections.abc.Iterable[builtins.int] | None = ...,
        diff_ask_vol: collections.abc.Iterable[builtins.int] | None = ...,
        first_derived_bid_price: builtins.float = ...,
        first_derived_ask_price: builtins.float = ...,
        first_derived_bid_vol: builtins.int = ...,
        first_derived_ask_vol: builtins.int = ...,
        underlying_price: builtins.float = ...,
        simtrade: builtins.int = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["ask_price", b"ask_price", "ask_total_vol", b"ask_total_vol", "ask_volume", b"ask_volume", "bid_price", b"bid_price", "bid_total_vol", b"bid_total_vol", "bid_volume", b"bid_volume", "code", b"code", "date_time", b"date_time", "diff_ask_vol", b"diff_ask_vol", "diff_bid_vol", b"diff_bid_vol", "first_derived_ask_price", b"first_derived_ask_price", "first_derived_ask_vol", b"first_derived_ask_vol", "first_derived_bid_price", b"first_derived_bid_price", "first_derived_bid_vol", b"first_derived_bid_vol", "simtrade", b"simtrade", "underlying_price", b"underlying_price"]) -> None: ...

global___FutureRealTimeBidAskMessage = FutureRealTimeBidAskMessage

class ErrorMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    ERR_FIELD_NUMBER: builtins.int
    err: builtins.str
    def __init__(
        self,
        *,
        err: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["err", b"err"]) -> None: ...

global___ErrorMessage = ErrorMessage

class Date(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATE_FIELD_NUMBER: builtins.int
    date: builtins.str
    def __init__(
        self,
        *,
        date: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["date", b"date"]) -> None: ...

global___Date = Date

class StockNumArr(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STOCK_NUM_ARR_FIELD_NUMBER: builtins.int
    @property
    def stock_num_arr(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        stock_num_arr: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["stock_num_arr", b"stock_num_arr"]) -> None: ...

global___StockNumArr = StockNumArr

class StockNumArrWithDate(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STOCK_NUM_ARR_FIELD_NUMBER: builtins.int
    DATE_FIELD_NUMBER: builtins.int
    @property
    def stock_num_arr(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    date: builtins.str
    def __init__(
        self,
        *,
        stock_num_arr: collections.abc.Iterable[builtins.str] | None = ...,
        date: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["date", b"date", "stock_num_arr", b"stock_num_arr"]) -> None: ...

global___StockNumArrWithDate = StockNumArrWithDate

class StockNumArrWithDateArr(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    STOCK_NUM_ARR_FIELD_NUMBER: builtins.int
    DATE_ARR_FIELD_NUMBER: builtins.int
    @property
    def stock_num_arr(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    @property
    def date_arr(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        stock_num_arr: collections.abc.Iterable[builtins.str] | None = ...,
        date_arr: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["date_arr", b"date_arr", "stock_num_arr", b"stock_num_arr"]) -> None: ...

global___StockNumArrWithDateArr = StockNumArrWithDateArr

class FutureCodeArr(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FUTURE_CODE_ARR_FIELD_NUMBER: builtins.int
    @property
    def future_code_arr(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    def __init__(
        self,
        *,
        future_code_arr: collections.abc.Iterable[builtins.str] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["future_code_arr", b"future_code_arr"]) -> None: ...

global___FutureCodeArr = FutureCodeArr

class FutureCodeArrWithDate(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    FUTURE_CODE_ARR_FIELD_NUMBER: builtins.int
    DATE_FIELD_NUMBER: builtins.int
    @property
    def future_code_arr(self) -> google.protobuf.internal.containers.RepeatedScalarFieldContainer[builtins.str]: ...
    date: builtins.str
    def __init__(
        self,
        *,
        future_code_arr: collections.abc.Iterable[builtins.str] | None = ...,
        date: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["date", b"date", "future_code_arr", b"future_code_arr"]) -> None: ...

global___FutureCodeArrWithDate = FutureCodeArrWithDate
