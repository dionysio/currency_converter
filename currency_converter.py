#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse

import simplejson as json

from utils import convert_currency, all_currencies, symbol_to_currency


def currency_converter(*args, **kwargs):
    try:
        result = convert_currency(*args, **kwargs)
    except (KeyboardInterrupt, SystemExit):
        raise
    except Exception as e:
        result = {'error': str(e)}

    return json.dumps(result, indent=4, sort_keys=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Currency converter using exchange rates from the http://fixer.io/ API.')
    parser.add_argument('-a', '--amount', required=True, help='Amount to be converted.')
    parser.add_argument('-i', '--input_currency', required=True, help='Input currency. Use either 3 letter code (one of {}) or currency symbol (one of {})).'.format(all_currencies, set(symbol_to_currency.keys())))
    parser.add_argument('-o', '--output_currency', help='Currency you want to convert to. If omitted, converts to all currencies {}.'.format(all_currencies))
    args = parser.parse_args()

    print(currency_converter(**dict(args._get_kwargs())))
