import os
from requests import request, Session
from .adapters import CfbHTTPAdapter as HTTPAdapter
from .exceptions import (
    BypassError,
    BypassRequestError,
    BypassFailedError,
    BypassTimeoutError,
    BypassServerError, APIError
)

ENV_APIKEY = os.environ.get("CB_APIKEY", "")
ENV_PROXY = os.environ.get("CB_PROXY", "")


class CloudbypassSession(Session):

    def __init__(self, apikey=None, proxy=None, api_host=None):
        super().__init__()
        self.apikey = apikey or ENV_APIKEY
        self.headers.update({
            "x-cb-proxy": proxy or ENV_PROXY
        })
        self.mount("https://", HTTPAdapter(api_host))
        self.mount("http://", HTTPAdapter(api_host))

    def v2(self, method, url, part="0", **kwargs):
        return self.request(method, url, part=part, **kwargs)

    def request(self, method, url, part=None, **kwargs):
        kwargs['headers'] = kwargs.get("headers", {})
        options = set(kwargs.get("headers", {}).get("x-cb-options", "").lower().split(","))
        options.add("disable-redirect")
        options.add("full-cookie")

        headers = {
            "x-cb-apikey": self.apikey,
            "x-cb-options": ",".join(options)
        }

        # Use V2 API
        if part is not None and str(part).isdigit():
            headers['x-cb-version'] = "2"
            headers['x-cb-part'] = str(part)

        # Use Proxy
        if kwargs.get("proxy"):
            headers['x-cb-proxy'] = kwargs.pop("proxy")

        kwargs['headers'].update(headers)

        resp = super().request(method, url, **kwargs)

        if resp.status_code != 200 and resp.headers.get("x-cb-status") != "ok":
            if resp.headers.get("content-type", "").lower().startswith("application/json"):
                raise BypassError(**resp.json())

        return resp

    def get_balance(self, apikey=None):
        resp = request("GET", "https://console.cloudbypass.com/api/v1/balance?apikey=" + (apikey or self.apikey))
        if resp.status_code != 200:
            raise APIError(**resp.json())

        return resp.json()["balance"]

    def get(self, url, **kwargs):
        return super().get(url, **kwargs)

    def options(self, url, **kwargs):
        return super().options(url, **kwargs)

    def head(self, url, **kwargs):
        return super().head(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return super().post(url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return super().put(url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return super().patch(url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return super().delete(url, **kwargs)
