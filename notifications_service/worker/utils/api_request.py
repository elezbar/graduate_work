import json
import ssl
import urllib.parse

import urllib3


class ApiRequest:
    CONTENT_TYPE_URLENCODE = 'application/x-www-form-urlencoded'

    def __init__(self, access_token: str, timeout: int = 3600):
        self.access_token = access_token
        self.timeout = timeout

    def __request(self, method, url,
                  fields=None, headers=None, encode_multipart=True, multipart_boundary=None, **urlopen_kw):
        self.http_caller = urllib3.PoolManager(
            num_pools=50, ssl_context=ssl._create_unverified_context(), timeout=self.timeout, retries=20
        )
        urlopen_kw.update({"timeout": self.timeout})
        return self.http_caller.request(
            method, url, fields, headers, encode_multipart=encode_multipart,
            multipart_boundary=multipart_boundary, **urlopen_kw
        )

    def api_call(self, url, params, method='POST', content_type='application/json', **kwargs):
        request_url = url
        headers = kwargs.get("headers", {})
        headers.update({'Content-Type': content_type, 'Authorization': f"Bearer {self.access_token}"})
        headers["accept"] = headers.get("accept", "application/json")

        if content_type == ApiRequest.CONTENT_TYPE_URLENCODE:
            params = urllib.parse.urlencode(params)
        elif isinstance(params, dict):
            params = json.dumps(params)

        try:
            response = self.__request(method, request_url, body=params, headers=headers)
            return json.loads(response.data.decode())
        except json.JSONDecodeError:
            return None
