# Currency Converter
Currency converter using exchange rates from the http://fixer.io/ API. It uses [forex-python](https://github.com/MicroPyramid/forex-python) to get the currency rates, Flask for providing the web API.


## Installation

Python3 +
```
pip install -r requirements.txt
```

## API Usage

You can start the server by running:

```
python webservice.py
```

The API accepts GET parameters:

* amount 
* input_currency
* output_currency

To convert $15.24 to EUR, you can call:

[http://127.0.0.1:5000/currency_converter?amount=15.24&input_currency=$&output_currency=EUR](http://0.0.0.0:5000/currency_converter?amount=15.24&input_currency=$&output_currency=EUR)

which should return JSON:
```
{
    "input": {
        "amount": 15.24,
        "currency": "USD"
    },
    "output": {
        "EUR": 13.6035288
    }
}
```

In case of an error, you get 400/500 status codes and the returned JSON will look like:
```
{
    "error": "'amount' has to be a number."
}
```

## CLI Usage

```
usage: currency_converter.py [-h] -a AMOUNT -i INPUT_CURRENCY
                             [-o OUTPUT_CURRENCY]

Currency converter using exchange rates from the http://fixer.io/ API.

optional arguments:
  -h, --help            show this help message and exit
  -a AMOUNT, --amount AMOUNT
                        Amount to be converted.
  -i INPUT_CURRENCY, --input_currency INPUT_CURRENCY
                        Input currency. Use either 3 letter code (one of
                        {'USD', 'CHF', 'HRK', 'NZD', 'SGD', 'RON', 'CAD',
                        'KRW', 'BGN', 'MXN', 'RUB', 'DKK', 'HUF', 'THB',
                        'INR', 'EUR', 'AUD', 'SEK', 'BRL', 'IDR', 'CNY',
                        'PHP', 'NOK', 'ILS', 'PLN', 'JPY', 'TRY', 'HKD',
                        'MYR', 'ZAR', 'CZK', 'GBP'}) or currency symbol (one
                        of {'₪', '฿', 'zł', 'R$', 'lei', 'kr', '$', '£', 'RM',
                        '₩', 'Rp', '€', 'kn', '¥', 'руб', 'Php', 'Kč', 'лв',
                        'Ft', 'TL', 'R'})).
  -o OUTPUT_CURRENCY, --output_currency OUTPUT_CURRENCY
                        Currency you want to convert to. If omitted, converts
                        to all currencies {'USD', 'CHF', 'HRK', 'NZD', 'SGD',
                        'RON', 'CAD', 'KRW', 'BGN', 'MXN', 'RUB', 'DKK',
                        'HUF', 'THB', 'INR', 'EUR', 'AUD', 'SEK', 'BRL',
                        'IDR', 'CNY', 'PHP', 'NOK', 'ILS', 'PLN', 'JPY',
                        'TRY', 'HKD', 'MYR', 'ZAR', 'CZK', 'GBP'}.
```

## Tests

To run the test suite, call:

```
python test.py
```