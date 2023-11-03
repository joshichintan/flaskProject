import json
import os

import flask
from flask import Flask, request

from src.apis.ledger import LedgerAPIS

app = Flask(__name__)


# restAPI
@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/ledger/', methods=['GET'])
def list_ledger():
    ledger_apis = LedgerAPIS()
    content, status_code, after_cursor = ledger_apis.get_ledgers(per_page=request.args.get('per_page', '1'),
                                                                 after_cursor=request.args.get('after_cursor', ''))
    return content, 200, {'X-AFTER-CURSOR': after_cursor}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
