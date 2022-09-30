import pickle

from redis import asyncio as redis  # type: ignore

from .objects import Coin

r = redis.Redis(host="localhost", port=6379, db=0)


def cache_all_coins(func):
    """Decorator for the "crypto_api_service.get_all_coins" function only!!!

    The decorator checks if there are all coins in the cache.
    If there are, it takes the coins from the cache,
    if not, it executes the function and adds the coins to the cache."""

    async def wrapper(*args, **kwargs):
        if await _are_coins_cached():
            coins = await _get_all_coins_from_cache()
            if coins:
                # print("Took all coins from cache")  # for debugging
                return coins
        else:
            result = await func(*args, **kwargs)
            if result:
                await _set_are_coins_cached_status()
                await _set_coin_key_list(result)
                for coin in result:
                    await _set_coin_to_cache(coin)
            return result

    return wrapper


def cache_coin(func):
    """Decorator for the "crypto_api_service._get_coins" function only!!!

    The decorator checks if there is a coin in the cache.
    If there is, it takes the coin from the cache,
    if not, it executes the function and adds the coin to the cache."""

    async def wrapper(coin_id: "str", *args, **kwargs):
        coin = await _get_coin_from_cache(coin_id)
        if coin:
            # print(f"Took {coin_id} from cache")  # for debugging
            return coin
        result = await func(coin_id, *args, **kwargs)
        await _set_coin_to_cache(result)
        return result

    return wrapper


async def _are_coins_cached() -> bool:
    if await r.exists("are_inline_tokens_cached"):
        return True
    else:
        return False


async def _set_are_coins_cached_status() -> None:
    await r.set("are_inline_tokens_cached", "1", ex=30)


async def _get_all_coins_from_cache() -> list[Coin]:
    coins: list[Coin] = []
    for key in await _get_coin_key_list():
        pickled_coin = await r.get(key)
        coin = pickle.loads(pickled_coin)
        coins.append(coin)
    return coins


async def _get_coin_from_cache(coin_id: str) -> Coin:
    pickled_coin = await r.get(f"coin:{coin_id}")
    if pickled_coin:
        coin = pickle.loads(pickled_coin)
        return coin
    return pickled_coin


async def _set_coin_to_cache(coin: Coin) -> None:
    pickled_coin = pickle.dumps(coin)
    await r.set(f"coin:{coin.id}", pickled_coin, ex=32)


async def _get_coin_key_list() -> list[str]:
    pickled_keys = await r.get("coin_key_list")
    if pickled_keys:
        keys = pickle.loads(pickled_keys)
        return keys
    return pickled_keys


async def _set_coin_key_list(coins: list[Coin]) -> None:
    """Stores a list of keys in the correct order
    (scan_iter() selects coins alphabetically - which is crooked.
    Coins need to be sorted by importance)"""

    key_list = [f"coin:{coin.id}" for coin in coins]
    pickled_keys = pickle.dumps(key_list)
    await r.set("coin_key_list", pickled_keys, ex=32)
