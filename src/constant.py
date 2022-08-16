from enum import Enum


class SecurityType(str, Enum):
    Index = "IND"
    Stock = "STK"
    Future = "FUT"
    Option = "OPT"


class DayTrade(str, Enum):
    Yes = "Yes"
    OnlyBuy = "OnlyBuy"
    No = "No"


class OrderState(str, Enum):
    Order = "ORDER"
    TFTOrder = "TFTORDER"
    Deal = "DEAL"
    TFTDeal = "TFTDEAL"
    FOrder = "FORDER"
    FDeal = "FDEAL"
