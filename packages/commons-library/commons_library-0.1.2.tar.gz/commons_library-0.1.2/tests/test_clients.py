import logging
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from commons.media import Image

TEMP_DIR: Path = Path(tempfile.mkdtemp())
logging.getLogger(__file__).warning(f"Temporary directory: {TEMP_DIR.resolve()}")


class TestHTTPClients(unittest.TestCase):
    def test_currency_client(self):
        from commons.http.client import CurrencyClient, TransferQuote, CurrencyQuote

        quote: TransferQuote = CurrencyClient.transfer_quote(from_currency="BRL", to_currency="EUR",
                                                             recipient_gets_amount=Decimal(100))
        rate: CurrencyQuote = CurrencyClient.currency_quote(from_currency="EUR", to_currency="BRL")
        assert quote
        assert rate

    def test_gravatar_client(self):
        from commons.http.client import GravatarClient

        image: Image = GravatarClient.avatar("e5f43fe12e80783bd2666c529fbf33d0", size=120)
        assert image and image.read()

    def test_giphy_client(self):
        from commons.http.client import GiphyClient

        image: Image = GiphyClient.gif("l4HogOSqU3uupmvmg")
        assert image and image.read()
