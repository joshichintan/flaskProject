import json
import os
import unittest
from unittest.mock import MagicMock, patch

import requests
import responses

from src.apis.custumexceptions import MissingAuthCred
from src.apis.ledger import LedgerAPIS


class TestLedgerAPIS(unittest.TestCase):

    def setUp(self):
        pass

    def test_class_initiation_failure(self):
        self.assertRaises(MissingAuthCred, LedgerAPIS)

    @patch.dict(os.environ, {"ORG_ID":'Test', "API_KEY":'Test', "MOD_T_API_URL":'Test'}, clear=True)
    def test_class_initiation_success(self):
        self.assertEqual(LedgerAPIS, type(LedgerAPIS()))

    @responses.activate
    @patch('requests.get')
    @patch.dict(os.environ, {"ORG_ID":'Test', "API_KEY":'Test', "MOD_T_API_URL":'Test'}, clear=True)
    def test_get_ledgers(self, test):
        test.return_value = MagicMock(status_code=200, content=json.dumps({"data": "test"}),headers={'X-After-Cursor': '213'} )
        ledger_apis = LedgerAPIS()
        content, status_code, cursor = ledger_apis.get_ledgers()
        self.assertEqual(content, {"data": "test"})
        self.assertEqual(status_code, 200)
        self.assertEqual(cursor, '213')

    def tearDown(self):
        pass
