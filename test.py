#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import json
from urllib.parse import urlencode

from webservice import app


AMOUNT = 21.45
INPUT_CURRENCY = 'EUR'
OUTPUT_CURRENCY = 'USD'
NON_EXISTING_CURRENCY = 'Kčs'


class BasicTestCases(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def _get(self, params, *args, **kwargs):
        query_string = urlencode(params)
        response = self.app.get('/currency_converter/?{}'.format(query_string), *args, **kwargs)
        result = json.loads(response.data.decode('utf-8'))
        return response, result

    def assert_response(self, response, code):
        self.assertEqual(response.mimetype, 'application/json')
        self.assertEqual(response.status_code, code)

    def assert_error(self, response, result, message, code=400):
        self.assert_response(response, code)
        self.assertIn('error', result)
        self.assertEqual(message, result['error'])

    def assert_success(self, response, result, code=200):
        self.assert_response(response, code)
        self.assertIn('input', result)
        self.assertIn('currency', result['input'])
        self.assertIn('amount', result['input'])
        self.assertIn('output', result)
        self.assertGreaterEqual(len(result['output']), 1)

    def test_empty_amount(self):
        response, result = self._get(params={'input_currency': INPUT_CURRENCY, 'amount': ''})

        self.assert_error(response, result, "'amount' argument is required.")

    def test_nan_amount(self):
        response, result = self._get(params={'input_currency': INPUT_CURRENCY, 'amount': 'hunter2'})

        self.assert_error(response, result, "'amount' has to be a number.")

    def test_zero_amount(self):
        amount = 0
        response, result = self._get(params={'input_currency': INPUT_CURRENCY, 'amount': amount,
                                             'output_currency': OUTPUT_CURRENCY})

        self.assert_success(response, result)
        self.assertEqual(result['output'][OUTPUT_CURRENCY], amount)

    def test_negative_amount(self):
        response, result = self._get(params={'input_currency': INPUT_CURRENCY, 'amount': -12.45})

        self.assert_error(response, result, "'amount' has to be non-negative.")

    def test_special_float_amount(self):
        response, result = self._get(params={'input_currency': INPUT_CURRENCY, 'amount': 'inf'})

        self.assert_error(response, result, "'amount' has to be a number.")

    def test_whitespace_amount(self):
        response, result = self._get(params={'input_currency': INPUT_CURRENCY, 'amount': '     {}     '.format(AMOUNT)})

        self.assert_success(response, result)

    def test_empty_input_currency(self):
        response, result = self._get(params={'amount': AMOUNT, 'input_currency': ''})

        self.assert_error(response, result, "'input_currency' argument is required.")

    def test_non_existing_input_currency(self):
        response, result = self._get(params={'input_currency': NON_EXISTING_CURRENCY, 'amount': AMOUNT})

        self.assert_error(response, result, "'input_currency' is not a currency/symbol.")

    def test_whitespace_input_currency(self):
        response, result = self._get(params={'input_currency': '       {}  '.format(INPUT_CURRENCY), 'amount': AMOUNT})

        self.assert_success(response, result)

    def test_symbol_input_currency(self):
        response, result = self._get(params={'input_currency': 'Kč', 'amount': AMOUNT})

        self.assert_success(response, result)
        self.assertEqual(result['input']['currency'], 'CZK')

    def test_non_existing_output_currency(self):
        response, result = self._get(params={'output_currency': NON_EXISTING_CURRENCY, 'amount': AMOUNT,
                                             'input_currency': INPUT_CURRENCY})

        self.assert_error(response, result, "'output_currency' is not a currency/symbol.")

    def test_symbol_output_currency(self):
        response, result = self._get(params={'output_currency': '$', 'amount': AMOUNT,
                                             'input_currency': INPUT_CURRENCY})

        self.assert_success(response, result)
        self.assertIn(OUTPUT_CURRENCY, result['output'])

    def test_whitespace_output_currency(self):
        response, result = self._get(params={'output_currency': '   {}  '.format(OUTPUT_CURRENCY), 'amount': AMOUNT,
                                             'input_currency': INPUT_CURRENCY})

        self.assert_success(response, result)

    def test_omitted_output_currency(self):
        response, result = self._get(params={'amount': AMOUNT, 'input_currency': INPUT_CURRENCY})

        self.assert_success(response, result)
        self.assertGreater(len(result['output']), 1)

    def test_correct_input(self):
        response, result = self._get(params={'output_currency': OUTPUT_CURRENCY, 'amount': AMOUNT,
                                             'input_currency': INPUT_CURRENCY})

        self.assert_success(response, result)
        self.assertEqual(result['input']['currency'], INPUT_CURRENCY)
        self.assertIn(OUTPUT_CURRENCY, result['output'])
        self.assertEqual(result['input']['amount'], AMOUNT)

    def test_same_input_currency_output_currency(self):
        response, result = self._get(params={'output_currency': OUTPUT_CURRENCY, 'amount': AMOUNT,
                                             'input_currency': OUTPUT_CURRENCY})

        self.assert_error(response, result, "'input_currency' and 'output_currency' can't be the same.")


if __name__ == '__main__':
    unittest.main()
