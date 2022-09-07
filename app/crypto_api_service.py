import asyncio
from decimal import Decimal
from typing import NamedTuple, TypedDict

from aiohttp import ClientSession  # type: ignore

_COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/"
_CurrencyCode = str


class Coin(NamedTuple):
    name: str
    price: Decimal
    price_change_24h: float


class _ApiMarketData(TypedDict):
    current_price: dict[_CurrencyCode, Decimal]
    price_change_percentage_24h: float


class _ApiResponseEntry(TypedDict):
    name: str
    market_data: _ApiMarketData


async def get_coin(coin_id: str, baseCurrency: str = "usd") -> Coin:
    """Requests coin in coingecko-api and returns it"""
    response = await _get_response(coin_id)
    coin = await _parse_response(response, baseCurrency)
    return coin


async def _get_response(curency=None) -> _ApiResponseEntry:
    # Need to consider about exceptions
    async with ClientSession() as session:
        async with session.get(_COINGECKO_URL + curency) as resp:
            return await resp.json()


async def _parse_response(response: _ApiResponseEntry, baseCurrency) -> Coin:
    market_data = response["market_data"]
    coinInfo = Coin(
        name=response["name"],
        price=round(
            Decimal(market_data["current_price"][f"{baseCurrency}"]), 2
        ),
        price_change_24h=round(
            float(market_data["price_change_percentage_24h"]), 2
        ),
    )
    return coinInfo


async def _test_service():
    print(await get_coin("bitcoin"))
    print(await get_coin("ethereum"))


if __name__ == "__main__":
    asyncio.run(_test_service())
