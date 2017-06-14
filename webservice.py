#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify

from utils import convert_currency

app = Flask(__name__)
app.config.from_object('config')


@app.route('/currency_converter/', methods=['GET'])
def convert_view():
    status = 200
    error = ''
    try:
        args = request.args
        result = convert_currency(args.get('amount'), args.get('input_currency'), args.get('output_currency'))
    except (KeyboardInterrupt, SystemExit):
        raise
    except ValueError as e:
        status = 400
        error = e
    except Exception as e:
        status = 500
        error = e
    if error:
        result = {'error': str(error)}

    return jsonify(result), status


if __name__ == '__main__':
    app.run()
