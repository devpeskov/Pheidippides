from decimal import Decimal
import json
from pathlib import Path

from .objects import Coin, MoodStickers

with open(Path(__file__).resolve().parent / "mood_stickers.json") as f:
    mood_stickers = json.load(f)


def chooseSticker(coins: list[Coin]) -> str:
    price_change_24h = _get_price_change_24h(coins)
    if price_change_24h < -23:
        return _get_file_id(MoodStickers.NEGATIVE23.value)
    elif price_change_24h < -15:
        return _get_file_id(MoodStickers.NEGATIVE19.value)
    elif price_change_24h < -11:
        return _get_file_id(MoodStickers.NEGATIVE15.value)
    elif price_change_24h < -8:
        return _get_file_id(MoodStickers.NEGATIVE11.value)
    elif price_change_24h < -4:
        return _get_file_id(MoodStickers.NEGATIVE8.value)
    elif price_change_24h < -1:
        return _get_file_id(MoodStickers.NEGATIVE4.value)
    elif price_change_24h < 4:
        return _get_file_id(MoodStickers.POSITIVE4.value)
    elif price_change_24h < 8:
        return _get_file_id(MoodStickers.POSITIVE8.value)
    elif price_change_24h < 11:
        return _get_file_id(MoodStickers.POSITIVE11.value)
    elif price_change_24h < 15:
        return _get_file_id(MoodStickers.POSITIVE15.value)
    elif price_change_24h < 19:
        return _get_file_id(MoodStickers.POSITIVE19.value)
    else:
        return _get_file_id(MoodStickers.POSITIVE23.value)


def _get_file_id(json_key) -> str:
    return mood_stickers.get(json_key)


def _get_price_change_24h(coins: list[Coin]) -> float:
    """The function finds the coin with the largest capitalization
    and returns its price_change_percentage_24h"""
    coin = min(coins, key=lambda x: x.market_cap_rank)
    return coin.price_change_24h


def _test():
    coins = [
        Coin(
            id="btc",
            symbol="btc",
            name="btc",
            img_small="af",
            img_large="a",
            price=Decimal(12),
            price_change_24h=-12,
            market_cap_rank=2,
        ),
        Coin(
            id="btc",
            symbol="btc",
            name="btc",
            img_small="af",
            img_large="a",
            price=Decimal(12),
            price_change_24h=-10,
            market_cap_rank=4,
        ),
        Coin(
            id="btc",
            symbol="btc",
            name="btc",
            img_small="af",
            img_large="a",
            price=Decimal(12),
            price_change_24h=20,
            market_cap_rank=8,
        ),
    ]
    print(_get_price_change_24h(coins))


if __name__ == "__main__":
    _test()
