from decimal import Decimal
from typing import Literal, NamedTuple, TypedDict

CurrencyCode = str
ImgUrl = str


class Coin(NamedTuple):
    id: str
    name: str
    img_small: str
    img_large: str
    price: Decimal
    price_change_24h: float


class _ApiMarketData(TypedDict):
    current_price: dict[CurrencyCode, float]
    price_change_percentage_24h: float


class ApiResponseEntry(TypedDict):
    id: str
    name: str
    image: dict[Literal["thumb", "small", "large"], ImgUrl]
    market_data: _ApiMarketData
