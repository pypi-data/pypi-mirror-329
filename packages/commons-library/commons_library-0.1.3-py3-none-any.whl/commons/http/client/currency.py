import json
from datetime import datetime
from decimal import Decimal
from logging import getLogger, Logger
from typing import Optional

import httpx
from pydantic import BaseModel, computed_field, Field
from commons.http import query

logger: Logger = getLogger(__file__)


class _WiseQuote(BaseModel):
    rate: Decimal
    fee: Decimal
    dateCollected: datetime
    sourceCountry: Optional[str]
    targetCountry: Optional[str]
    markup: Decimal
    receivedAmount: Optional[Decimal]
    sendAmount: Optional[Decimal]
    isConsideredMidMarketRate: bool

    @computed_field
    @property
    def amount(self) -> Decimal:
        if self.sendAmount:
            return self.sendAmount
        elif self.receivedAmount:
            return self.receivedAmount
        else:
            return Decimal(0)


class _WiseQuotationProvider(BaseModel):
    id: int
    alias: str
    name: str
    logos: dict
    type: str
    partner: bool
    quotes: list[_WiseQuote]


class _WiseQuotationResponse(BaseModel):
    sourceCurrency: str
    targetCurrency: str
    sourceCountry: Optional[str] = None
    targetCountry: Optional[str] = None
    providerCountry: Optional[str] = None
    providerTypes: list[str]
    amount: Decimal
    amountType: str
    providers: list[_WiseQuotationProvider]

    @computed_field
    @property
    def quotation(self) -> _WiseQuote:
        provider: Optional[_WiseQuotationProvider] = None
        quote: Optional[_WiseQuote] = None

        if self.providers:
            for provider in self.providers:
                if provider.alias == "wise":
                    break

        if provider and len(provider.quotes) >= 1:
            quote = provider.quotes[0]

        return quote


class CurrencyQuote(BaseModel):
    source_currency: str
    target_currency: str
    date: datetime
    rate: Decimal


class TransferQuote(BaseModel):
    provider: str = "wise"
    quote: CurrencyQuote
    sourceCountry: Optional[str]
    targetCountry: Optional[str]
    date: datetime = Field(validation_alias="dateCollected")
    amount: Decimal
    fee: Decimal

    @computed_field
    @property
    def no_fee_amount(self) -> Decimal:
        return self.amount - self.fee


class CurrencyClient:
    """
    Implements a client that fetches currency data from Wise.
    Documentation: https://docs.wise.com/api-docs/api-reference/comparison
    """

    # noinspection PyUnresolvedReferences
    @staticmethod
    def transfer_quote(from_currency: str, to_currency: str,
                       send_amount: Optional[Decimal] = None,
                       recipient_gets_amount: Optional[Decimal] = None,
                       source_country: Optional[str] = None, target_country: Optional[str] = None,
                       decimal_precision: int = 2) -> TransferQuote:
        """
        Get a transfer quotation between two currencies. Either `send_amount` or `recipient_gets_amount` should be specified.

        :param from_currency: ISO-4217 currency as string
        :param to_currency: ISO-4217 currency as string
        :param send_amount: [Optional] Amount to send
        :param recipient_gets_amount: [Optional] Amount to receive
        :param source_country: [Optional] ISO-3166-1 Alpha-2 country code as string
        :param target_country: [Optional] ISO-3166-1 Alpha-2 country code as string
        :param decimal_precision: [Optional] Precision used on amount conversion. Default is 2.
        """
        # --- Build parameters
        from pycountry import currencies, countries
        params: dict = {
            "sourceCurrency": currencies.lookup(from_currency).alpha_3,
            "targetCurrency": currencies.lookup(to_currency).alpha_3
        }

        if send_amount:
            params["sendAmount"] = f"{send_amount:.{decimal_precision}f}"
        elif recipient_gets_amount:
            params["recipientGetsAmount"] = f"{recipient_gets_amount:.{decimal_precision}f}"
        else:
            raise ValueError("Either `send_amount` or `recipient_gets_amount` must be specified.")

        if source_country:
            params["sourceCountry"] = countries.lookup(source_country).alpha_2
        if target_country:
            params["targetCountry"] = countries.lookup(target_country).alpha_2

        # --- Request data
        response = httpx.get(f"https://api.wise.com/v4/comparisons/?{query.build(params)}")
        if response and response.status_code == 200:
            # build response
            wise_response: _WiseQuotationResponse = _WiseQuotationResponse(**json.loads(response.content.decode()))
            quote: CurrencyQuote = CurrencyQuote(
                **{"source_currency": wise_response.sourceCurrency,
                   "target_currency": wise_response.targetCurrency,
                   "date": wise_response.quotation.dateCollected,
                   "rate": wise_response.quotation.rate}
            )
            transfer_quote: TransferQuote = TransferQuote(**({"quote": quote} | wise_response.quotation.model_dump()))

            return transfer_quote
        else:
            raise ConnectionError(f"An error has occurred while fetching Wise API: {response.status_code} - {response.content}")

    @classmethod
    def currency_quote(cls, from_currency: str, to_currency: str) -> CurrencyQuote:
        """
        Get currency rate between two currencies.

        :param from_currency: ISO-4217 currency as string
        :param to_currency: ISO-4217 currency as string
        """
        return cls.transfer_quote(from_currency, to_currency, recipient_gets_amount=Decimal(1)).quote
