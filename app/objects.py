from decimal import Decimal
from enum import Enum
from typing import Literal, NamedTuple, TypedDict

CurrencyCode = str
ImgUrl = str


class Coin(NamedTuple):
    id: str
    symbol: str
    name: str
    img_small: str
    img_large: str
    price: Decimal
    price_change_24h: float
    market_cap_rank: int


class _ApiMarketData(TypedDict):
    current_price: dict[CurrencyCode, float]
    price_change_percentage_24h: float
    market_cap_rank: int


class ApiResponseEntry(TypedDict):
    id: str
    symbol: str
    name: str
    image: dict[Literal["thumb", "small", "large"], ImgUrl]
    market_data: _ApiMarketData


class MoodStickers(Enum):
    """Sticker-switcher depending on the percentage price change 24h"""
    NEGATIVE23 = "negative23"
    NEGATIVE19 = "negative19"
    NEGATIVE15 = "negative15"
    NEGATIVE11 = "negative11"
    NEGATIVE8 = "negative8"
    NEGATIVE4 = "negative4"
    POSITIVE4 = "positive4"
    POSITIVE8 = "positive8"
    POSITIVE11 = "positive11"
    POSITIVE15 = "positive15"
    POSITIVE19 = "positive19"
    POSITIVE23 = "positive23"
