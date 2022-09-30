import json
from pathlib import Path

from .objects import Coin


class KeyStorage:
    """Stores redis-keys in the correct order in JSON file"""

    def __init__(self):
        self._init_strorage()

    _jsonfile = Path(__file__).resolve().parent / "redis_keys.json"

    def set_keys(self, coins: list[Coin]) -> None:
        keys = self._form_array_of_keys(coins)
        self._write(keys)

    def get_keys(self) -> list[str]:
        with open(self._jsonfile, "r") as f:
            return json.load(f)

    def _form_array_of_keys(self, coins: list[Coin]) -> list[str]:
        keys = []
        for coin in coins:
            keys.append(f"coin:{coin.id}")
        return keys

    def _write(self, keys: list[str]) -> None:
        with open(self._jsonfile, "w") as f:
            json.dump(keys, f, ensure_ascii=False, indent=4)

    def _init_strorage(self) -> None:
        if not self._jsonfile.exists():
            self._jsonfile.write_text("[]")
