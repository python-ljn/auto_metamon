import os
from typing import Dict, Any

import requests

os.environ.setdefault("NO_PROXY", "https://metamon-api.radiocaca.com/")


class Session:

    def __init__(self):
        self.session = requests.session()

    def post(self, url, headers: Dict[str, Any], data: Dict[str, Any]):
        return self.session.post(url, headers=headers, data=data)


class MetamonSession(Session):

    def __init__(self, token):
        super(MetamonSession, self).__init__()
        self.token = token
        self.base_headers = {
            'origin': 'https://metamon.radiocaca.com',
            'referer': 'https://metamon.radiocaca.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            "accesstoken": self.token
        }

    def post(self, url, headers: Dict[str, Any] = None, data: Dict[str, Any] = None, **kwargs):
        if not headers:
            headers = self.base_headers
        ret = super().post(url, headers, data).json()
        if ret["code"] != "SUCCESS":
            raise ValueError(f"请求失败{ret}")
        return ret
