import os
from requests import request,Session
from .adapters import CfbHTTPAdapter as HTTPAdapter
from .exceptions import (
    BypassError,
    BypassRequestError,
    BypassFailedError,
    BypassTimeoutError,
    BypassServerError, APIError
)

ENV_APIKEY = os.environ.get("CB_APIKEY", "")
ENV_PROXY = os.environ.get("PROXY", "")


class CloudbypassSession(Session):

    def __init__(self, apikey=None, proxy=None, api_host=None):
        super().__init__()
        self.apikey = apikey or ENV_APIKEY
        self.headers.update({
            "x-cb-proxy": proxy or ENV_PROXY
        })
        self.mount("https://", HTTPAdapter(api_host))
        self.mount("http://", HTTPAdapter(api_host))

    def request(self, method, url, **kwargs):
        options = set(kwargs.get("headers", {}).get("x-cb-options", "").lower().split(","))
        options.add("disable-redirect")
        options.add("full-cookie")

        headers = {
            "x-cb-apikey": self.apikey,
            "x-cb-options": ",".join(options)
        }

        if kwargs.get("headers"):
            kwargs['headers'].update(headers)
        else:
            kwargs['headers'] = headers

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