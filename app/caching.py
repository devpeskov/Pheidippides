import pickle

from redis import asyncio as redis  # type: ignore

from .objects import Coin

r = redis.Redis(host="localhost", port=6379, db=0)


def cache_coins(func):
    """Decorator for the "get_all_coins" function only!!!

    The decorator checks if there are "all" coins in the cache.
    If there are, it takes the result from the cache,
    if not, it executes the function and adds the result to the cache."""

    async def wrapper(*args, **kwargs):
        if await _are_inline_tokens_cached():
            coins = await _get_coins()
            if coins:
                # print("Took all tokens from cache")  # for debugging
                return coins
        else:
            result = await func(*args, **kwargs)
            if result:
                await _set_inline_tokens_cached_status()
                for coin in result:
                    await _cache_coin(coin)
            return result

    return wrapper


def cache_coin(func):
    """Decorator for the "_get_coins" function only!!!

    The decorator checks if there is a coin in the cache.
    If there is, it takes the result from the cache,
    if not, it executes the function and adds the result to the cache."""

    async def wrapper(coin_id: "str", *args, **kwargs):
        coin = await _get_cached_coin(coin_id)
        if coin:
            # print(f"Took {coin_id} from cache")  # for debugging
            return coin
        result = await func(coin_id, *args, **kwargs)
        await _cache_coin(result)
        return result

    return wrapper


async def _set_inline_tokens_cached_status():
    await r.set("are_inline_tokens_cached", "1", ex=30)


async def _are_inline_tokens_cached():
    if await r.exists("are_inline_tokens_cached"):
        return True
    else:
        return False


async def _cache_coin(coin: Coin) -> None:
    pickled_coin = pickle.dumps(coin)
    await r.set(f"coin:{coin.id}", pickled_coin, ex=32)


async def _get_cached_coin(coin_id: str) -> Coin:
    pickled_coin = await r.get(f"coin:{coin_id}")
    if pickled_coin:
        coin = pickle.loads(pickled_coin)
        return coin
    return pickled_coin


async def _get_coins() -> list[Coin]:
    coins: list[Coin] = []
    async for key in r.scan_iter("coin:*"):
        pickled_coin = await r.get(key)
        coin = pickle.loads(pickled_coin)
        coins.append(coin)
    return coins
