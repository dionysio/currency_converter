#!/usr/bin/env python
# -*- coding: utf-8 -*-
import decimal

from forex_python.converter import CurrencyRates

from _currencies import symbol_to_currency, all_currencies


def to_currency(symbol, currency_type):
    currency = None
    cleaned_symbol = symbol.strip()
    try:
        currency = symbol_to_currency[cleaned_symbol]
    except KeyError:
        if cleaned_symbol not in all_currencies:
            raise ValueError("'{}' is not a currency/symbol.".format(currency_type))

    return currency or cleaned_symbol


def validate_arguments(amount, input_currency, output_currency=None):
    if not amount:
        raise ValueError("'amount' argument is required.")
    if not input_currency:
        raise ValueError("'input_currency' argument is required.")

    try:
        amount = amount.strip()
        if not amount.replace('.', '', 1).replace('-', '', 1).isdigit():  # get rid of special strings like inf
            raise decimal.InvalidOperation('')
        amount = decimal.Decimal(amount)
        if amount < 0:
            raise ValueError("'amount' has to be non-negative.")
    except decimal.InvalidOperation:
        raise ValueError("'amount' has to be a number.")

    input_currency = to_currency(input_currency, 'input_currency')
    if output_currency:
        output_currency = to_currency(output_currency, 'output_currency')

    return amount, input_currency, output_currency


def convert_currency(amount, input_currency, output_currency=None):
    amount, input_currency, output_currency = validate_arguments(amount, input_currency, output_currency)

    converter = CurrencyRates(force_decimal=True)
    if output_currency:
        if output_currency == input_currency:
            raise ValueError("'input_currency' and 'output_currency' can't be the same.")
        else:
            rate = converter.convert(input_currency, output_currency, amount)
            output = {output_currency: rate}
    else:  # output_currency was omitted so we get all available rates at once
        rates = converter.get_rates(input_currency)
        output = {currency: rate*amount for currency, rate in rates.items()}

    return {'output': output, 'input': {'amount': amount, 'currency': input_currency}}
