from enum import Enum


class SecurityType(str, Enum):
    """
    SecurityType is an enumeration for the security type of a security.

    Args:
        str (_type_): The type of the enumeration.
        Enum (_type_): The type of the enumeration.
    """

    Index = "IND"
    Stock = "STK"
    Future = "FUT"
    Option = "OPT"


class DayTrade(str, Enum):
    """
    DayTrade is an enumeration for the day trade type of a security.

    Args:
        str (_type_): The type of the enumeration.
        Enum (_type_): The type of the enumeration.
    """

    Yes = "Yes"
    OnlyBuy = "OnlyBuy"
    No = "No"


class OrderState(str, Enum):
    """
    OrderState is an enumeration for the state of an order.

    Args:
        str (_type_): The type of the enumeration.
        Enum (_type_): The type of the enumeration.
    """

    Order = "ORDER"
    TFTOrder = "TFTORDER"
    Deal = "DEAL"
    TFTDeal = "TFTDEAL"
    FOrder = "FORDER"
    FDeal = "FDEAL"
