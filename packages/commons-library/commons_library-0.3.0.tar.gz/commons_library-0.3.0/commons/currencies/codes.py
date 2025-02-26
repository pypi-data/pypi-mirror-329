# def _iso4217_codes():
import pycountry
import json
from pathlib import Path

_CRYPTO_CURRENCIES: list[dict] = [{"alpha_3": "BTC", "name": "Bitcoin"}]
_iso4217_codes = json.loads((Path(pycountry.DATABASE_DIR) / "iso4217.json").read_bytes())["4217"]


for _v in _CRYPTO_CURRENCIES + _iso4217_codes:
    globals()[_v["alpha_3"]] = _v["name"]


# noinspection PyUnresolvedReferences
def lookup(currency: str) -> str:
    """
    Lookup for a currency code. It supports Bitcoin.
    :param currency: a currency representation
    :return: an Alpha-3 ISO-4217 upper-case code
    """
    try:
        currency = currency.upper()
        return currency if globals().get(currency) else None
    except LookupError:
        raise ValueError(f"'{currency}' is neither a crypto or ISO-4217 (Alpha-3) currency code.")
