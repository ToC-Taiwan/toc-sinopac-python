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

@typing_extensions.final
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

@typing_extensions.final
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

@typing_extensions.final
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

@typing_extensions.final
class HistoryTickResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATA_FIELD_NUMBER: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___HistoryTickMessage]: ...
    def __init__(
        self,
        *,
        data: collections.abc.Iterable[global___HistoryTickMessage] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data", b"data"]) -> None: ...

global___HistoryTickResponse = HistoryTickResponse

@typing_extensions.final
class HistoryKbarResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATA_FIELD_NUMBER: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___HistoryKbarMessage]: ...
    def __init__(
        self,
        *,
        data: collections.abc.Iterable[global___HistoryKbarMessage] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data", b"data"]) -> None: ...

global___HistoryKbarResponse = HistoryKbarResponse

@typing_extensions.final
class HistoryCloseResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATA_FIELD_NUMBER: builtins.int
    @property
    def data(self) -> google.protobuf.internal.containers.RepeatedCompositeFieldContainer[global___HistoryCloseMessage]: ...
    def __init__(
        self,
        *,
        data: collections.abc.Iterable[global___HistoryCloseMessage] | None = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["data", b"data"]) -> None: ...

global___HistoryCloseResponse = HistoryCloseResponse

@typing_extensions.final
class HistoryTickMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TS_FIELD_NUMBER: builtins.int
    CLOSE_FIELD_NUMBER: builtins.int
    VOLUME_FIELD_NUMBER: builtins.int
    BID_PRICE_FIELD_NUMBER: builtins.int
    BID_VOLUME_FIELD_NUMBER: builtins.int
    ASK_PRICE_FIELD_NUMBER: builtins.int
    ASK_VOLUME_FIELD_NUMBER: builtins.int
    TICK_TYPE_FIELD_NUMBER: builtins.int
    CODE_FIELD_NUMBER: builtins.int
    ts: builtins.int
    close: builtins.float
    volume: builtins.int
    bid_price: builtins.float
    bid_volume: builtins.int
    ask_price: builtins.float
    ask_volume: builtins.int
    tick_type: builtins.int
    code: builtins.str
    def __init__(
        self,
        *,
        ts: builtins.int = ...,
        close: builtins.float = ...,
        volume: builtins.int = ...,
        bid_price: builtins.float = ...,
        bid_volume: builtins.int = ...,
        ask_price: builtins.float = ...,
        ask_volume: builtins.int = ...,
        tick_type: builtins.int = ...,
        code: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["ask_price", b"ask_price", "ask_volume", b"ask_volume", "bid_price", b"bid_price", "bid_volume", b"bid_volume", "close", b"close", "code", b"code", "tick_type", b"tick_type", "ts", b"ts", "volume", b"volume"]) -> None: ...

global___HistoryTickMessage = HistoryTickMessage

@typing_extensions.final
class HistoryKbarMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    TS_FIELD_NUMBER: builtins.int
    CLOSE_FIELD_NUMBER: builtins.int
    OPEN_FIELD_NUMBER: builtins.int
    HIGH_FIELD_NUMBER: builtins.int
    LOW_FIELD_NUMBER: builtins.int
    VOLUME_FIELD_NUMBER: builtins.int
    CODE_FIELD_NUMBER: builtins.int
    ts: builtins.int
    close: builtins.float
    open: builtins.float
    high: builtins.float
    low: builtins.float
    volume: builtins.int
    code: builtins.str
    def __init__(
        self,
        *,
        ts: builtins.int = ...,
        close: builtins.float = ...,
        open: builtins.float = ...,
        high: builtins.float = ...,
        low: builtins.float = ...,
        volume: builtins.int = ...,
        code: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["close", b"close", "code", b"code", "high", b"high", "low", b"low", "open", b"open", "ts", b"ts", "volume", b"volume"]) -> None: ...

global___HistoryKbarMessage = HistoryKbarMessage

@typing_extensions.final
class HistoryCloseMessage(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    DATE_FIELD_NUMBER: builtins.int
    CODE_FIELD_NUMBER: builtins.int
    CLOSE_FIELD_NUMBER: builtins.int
    date: builtins.str
    code: builtins.str
    close: builtins.float
    def __init__(
        self,
        *,
        date: builtins.str = ...,
        code: builtins.str = ...,
        close: builtins.float = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["close", b"close", "code", b"code", "date", b"date"]) -> None: ...

global___HistoryCloseMessage = HistoryCloseMessage

@typing_extensions.final
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
