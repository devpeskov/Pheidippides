import asyncio
from decimal import Decimal
from typing import Literal, NamedTuple, TypedDict

from aiohttp import ClientSession  # type: ignore

_COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/"
_CurrencyCode = str
_ImgUrl = str


class Coin(NamedTuple):
    id: str
    name: str
    img_small: str
    img_large: str
    price: Decimal
    price_change_24h: float


class _ApiMarketData(TypedDict):
    current_price: dict[_CurrencyCode, float]
    price_change_percentage_24h: float


class _ApiResponseEntry(TypedDict):
    id: str
    name: str
    image: dict[Literal["thumb", "small", "large"], _ImgUrl]
    market_data: _ApiMarketData


async def get_all_coins(baseCurrency: str = "usd") -> list[Coin]:
    """Requests coin in coingecko-api and returns it"""
    coins: list[Coin] = []
    parent_response = await _get_parent_response()
    for response in parent_response:
        coin = await _parse_response(response, baseCurrency)
        coins.append(coin)
    return coins


async def get_specific_coins(
    coins_id: list["str"], baseCurrency: str = "usd"
) -> list[Coin]:
    """Requests coin in coingecko-api and returns it"""
    coins: list[Coin] = []
    for coin_id in coins_id:
        coin = await _get_coin(coin_id, baseCurrency)
        coins.append(coin)
    return coins


async def _get_coin(coin_id: str, baseCurrency: str = "usd") -> Coin:
    """Requests coin in coingecko-api and returns it"""
    response = await _get_response(coin_id)
    coin = await _parse_response(response, baseCurrency)
    return coin


async def _get_parent_response() -> list[_ApiResponseEntry]:
    # Need to consider about exceptions
    async with ClientSession() as session:
        async with session.get(_COINGECKO_URL) as resp:
            return await resp.json()


async def _get_response(curency=None) -> _ApiResponseEntry:
    # Need to consider about exceptions
    async with ClientSession() as session:
        async with session.get(_COINGECKO_URL + curency) as resp:
            return await resp.json()


async def _parse_response(response: _ApiResponseEntry, baseCurrency) -> Coin:
    market_data = response["market_data"]
    coinInfo = Coin(
        id=response["id"],
        name=response["name"],
        # "thumb" smaller than "small", bot too small
        img_small=response["image"]["small"],
        img_large=response["image"]["large"],
        price=_price_rounder(market_data["current_price"][baseCurrency]),
        price_change_24h=round(
            float(market_data["price_change_percentage_24h"]), 2
        ),
    )
    return coinInfo


def _price_rounder(price: float) -> Decimal:
    """Controls the number of digits after the decimal point"""
    decimal_price = Decimal(price)
    if decimal_price >= 100:
        return round(decimal_price, 0)
    elif decimal_price >= 10:
        return round(decimal_price, 1)
    elif decimal_price >= 1:
        return round(decimal_price, 2)
    elif decimal_price >= 0.1:
        return round(decimal_price, 3)
    elif decimal_price >= 0.01:
        return round(decimal_price, 4)
    elif decimal_price >= 0.001:
        return round(decimal_price, 5)
    elif decimal_price >= 0.0001:
        return round(decimal_price, 6)
    elif decimal_price >= 0.00001:
        return round(decimal_price, 7)
    else:
        return round(decimal_price, 8)


async def _test_service():
    # coins = await get_specific_coins(["bitcoin", "ethereum"])
    coins = await get_all_coins()
    for coin in coins:
        print(f"{coin.name}: {coin.price} ({coin.price_change_24h:+}%)")


if __name__ == "__main__":
    asyncio.run(_test_service())
