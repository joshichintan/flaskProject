import json
import logging
import os
import requests
from .custumexceptions import MissingAuthCred

logger = logging.getLogger(os.path.basename(__file__))


class LedgerAPIS:
    def __init__(self):
        try:
            self.header = {"accept": "application/json"}
            self.auth = (os.environ['ORG_ID'], os.environ['API_KEY'])
            self.base_url = os.environ['MOD_T_API_URL']
        except KeyError as e:
            logger.error(f'Missing Authentication creds {",".join(e.args)}')
            raise MissingAuthCred(f'Missing authentication creds {",".join(e.args)}')

    def get_ledgers(self, per_page: str = '1', after_cursor: str = '') -> (str, int):
        url = os.path.join(self.base_url, 'ledger_accounts')
        payload = {}
        if after_cursor:
            payload['after_cursor'] = after_cursor
        if per_page:
            payload['per_page'] = per_page
        response = requests.get(url, headers=self.header,
                                auth=self.auth, params=payload)
        content = json.loads(response.content)
        new_cursor = response.headers['X-After-Cursor']

        return content, response.status_code, new_cursor
