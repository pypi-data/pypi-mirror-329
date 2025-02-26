import unittest
from decimal import Decimal

from commons.media import Image


class TestHTTPClients(unittest.TestCase):
    def test_currency_client(self):
        from commons import currencies
        from commons.currencies import TransferQuote
        from commons.currencies import CurrencyQuote

        transfer_quote: TransferQuote = currencies.get_transfer_quote(from_currency="BRL", to_currency="EUR",
                                                                      recipient_gets_amount=Decimal(100))
        eur_to_brl_quote: CurrencyQuote = currencies.get_quote(from_currency="EUR", to_currency="BRL")
        btc_to_brl_quote: CurrencyQuote = currencies.get_quote(from_currency="BTC", to_currency="BRL")

        assert transfer_quote
        assert eur_to_brl_quote
        assert btc_to_brl_quote

    def test_gravatar_client(self):
        from commons.media import gravatar

        image: Image = gravatar.avatar("e5f43fe12e80783bd2666c529fbf33d0", size=120)
        assert image and image.read()

    def test_giphy_client(self):
        from commons.media import giphy

        image: Image = giphy.gif("l4HogOSqU3uupmvmg")
        assert image and image.read()
        return image
