import os
from typing import Dict, Any

import requests

os.environ.setdefault("NO_PROXY", "https://metamon-api.radiocaca.com/")


class Session:

    def __init__(self):
        self.session = requests.session()
        self.base_headers = {
            'origin': 'https://metamon.radiocaca.com',
            'referer': 'https://metamon.radiocaca.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        }

    def post(self, url, headers: Dict[str, Any], data: Dict[str, Any]):
        if headers:
            headers.update(self.base_headers)
        return self.session.post(url, headers=headers, data=data)


class MetamonSession(Session):

    def __init__(self, token):
        super(MetamonSession, self).__init__()
        self.token = token

    def post(self, url, headers: Dict[str, Any] = None, data: Dict[str, Any] = None, **kwargs):
        if not headers:
            headers = dict()
        headers.update(accesstoken=self.token)
        ret = super().post(url, headers, data).json()
        if ret["code"] != "SUCCESS":
            raise ValueError(f"请求失败{ret}")
        return ret
