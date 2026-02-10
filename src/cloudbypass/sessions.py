import os
import re

from yarl import URL
from aiohttp.client import _RequestContextManager
from requests import request, Session
from aiohttp import ClientSession, ClientRequest, InvalidURL
from .proxy import CloudbypassProxy
from .adapters import CfbHTTPAdapter as HTTPAdapter
from .exceptions import (
    BypassError,
    APIError
)

ENV_APIKEY = os.environ.get("CB_APIKEY", "")
ENV_PROXY = os.environ.get("CB_PROXY", "")


def get_api_host(api_host=None):
    res = re.match(
        r"^((?:http|https):(//)?)?([\w.-]+)(:(\d+))?$",
        api_host or os.environ.get("CB_APIHOST", "https://api.cloudbypass.com")
    )
    if not res:
        raise ValueError("Invalid ENV_API_HOST")

    port = res.group(5)
    return ((res.group(1) or 'https:').strip('//') + "//") + res.group(3) + (':' + port if port else '')


def parse_options(options):
    _options = {"disable-redirect", "full-cookie"}
    if isinstance(options, (list, set)):
        _options.update(options)
    if isinstance(options, str):
        _options.update(options.lower().replace(" ", "").split(","))
    return ",".join(_options)


class CloudbypassSession(Session):

    def __init__(
            self,
            apikey=None,
            proxy=None,
            api_host=None,
            options=None,
            use_v2=False,
            part=None,
            raise_for_cloudbypass=True
    ):
        super().__init__()
        self.apikey = apikey or ENV_APIKEY
        self.options = parse_options(options)
        self.headers.update({
            "x-cb-proxy": (str(proxy) if isinstance(proxy, CloudbypassProxy) else proxy) or ENV_PROXY,
        })
        self.use_v2 = use_v2
        self.part = part
        self.raise_for_cloudbypass = raise_for_cloudbypass
        self.mount("https://", HTTPAdapter(get_api_host(api_host)))
        self.mount("http://", HTTPAdapter(get_api_host(api_host)))

    def v2(self, method, url, part="0", **kwargs):
        return self.request(method, url, part=part, **kwargs)

    def request(self, method, url, apikey="", part=None, options=None, **kwargs):
        kwargs['headers'] = kwargs.get("headers", {})

        headers = {
            "x-cb-apikey": apikey or self.apikey,
            "x-cb-options": parse_options(options or self.options)
        }

        # Use V2 API
        part = part if part is not None else self.part
        if part is not None and str(part).isdigit():
            headers['x-cb-version'] = "2"
            headers['x-cb-part'] = str(part)

        if self.use_v2:
            headers['x-cb-version'] = "2s" if kwargs.get("stream") else "2"

        # Use Proxy
        if kwargs.get("proxy"):
            headers['x-cb-proxy'] = str(kwargs.pop("proxy"))

        kwargs['headers'].update(headers)

        resp = super().request(method, url, **kwargs)

        if self.raise_for_cloudbypass and resp.status_code != 200 and resp.headers.get("x-cb-status") != "ok":
            if resp.headers.get("content-type", "").lower().startswith("application/json"):
                raise BypassError(**resp.json())

        return resp

    def get_balance(self, apikey=None, email=None):
        resp = request(
            "GET", "https://console.cloudbypass.com/api/v1/balance",
            params={"apikey": apikey or self.apikey, "email": email}
        )
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


class CloudbypassSessionV2(CloudbypassSession):
    def __init__(self, apikey=None, proxy=None, api_host=None, options=None, part=None):
        super().__init__(apikey, proxy, api_host, options, True, part)


def make_request_class(api_host: URL):
    class AsyncCloudbypassClientRequest(ClientRequest):
        def __init__(self, method: str, url: URL, *args, **kwargs):
            headers = kwargs.get("headers", {})
            if url.host != api_host.host:
                headers["x-cb-host"] = url.host
                kwargs["headers"] = headers
                query = f"?{'&'.join([f'{k}={v}' for k, v in url.query.items()])}" if url.query else ""
                url = URL(f"{api_host}{url.path}" + query)

            super().__init__(method, url, *args, **kwargs)

    return AsyncCloudbypassClientRequest


class AsyncCloudbypassSession(ClientSession):

    def __init__(self, apikey=None, proxy=None, api_host=None, options=None, use_v2=False, part=None, **kwargs):
        super().__init__(**kwargs)
        self.apikey = apikey or ENV_APIKEY
        self.api_host = URL(get_api_host(api_host))
        self.options = parse_options(options)
        self.use_v2 = use_v2
        self.part = part
        self.headers.update({
            "x-cb-proxy": (str(proxy) if isinstance(proxy, CloudbypassProxy) else proxy) or ENV_PROXY,
        })
        self._request_class = make_request_class(self.api_host)

    def v2(self, method, url, part="0", **kwargs) -> _RequestContextManager:
        return self.request(method, url, part=part, **kwargs)

    def request(self, method, url, apikey="", part=None, options=None, **kwargs) -> _RequestContextManager:
        kwargs['headers'] = kwargs.get("headers", {})

        headers = {
            "x-cb-apikey": apikey or self.apikey,
            "x-cb-options": parse_options(options or self.options)
        }

        # Use V2 API
        part = part if part is not None else self.part
        if part is not None and str(part).isdigit():
            headers['x-cb-version'] = "2"
            headers['x-cb-part'] = str(part)

        if self.use_v2:
            headers['x-cb-version'] = "2s" if kwargs.get("stream") else "2"

        # Use Proxy
        if kwargs.get("proxy"):
            headers['x-cb-proxy'] = str(kwargs.pop("proxy"))

        kwargs['headers'].update(headers)

        return _RequestContextManager(self._request(method, url, **kwargs))

        # if resp.status != 200 and resp.headers.get("x-cb-status") != "ok":
        #     if resp.headers.get("content-type", "").lower().startswith("application/json"):
        #         raise BypassError(**await resp.json())
        #
        # return resp

    async def get_balance(self, apikey=None, email=None):
        async with ClientSession() as session:
            resp = await session.get(
                "https://console.cloudbypass.com/api/v1/balance",
                params={"apikey": apikey or self.apikey, "email": email}
            )

        if resp.status != 200:
            raise APIError(**await resp.json())

        return (await resp.json())["balance"]

    def get(self, url, **kwargs) -> _RequestContextManager:
        return self.request("GET", url, **kwargs)

    def options(self, url, **kwargs):
        return super().options(url, **kwargs)

    def head(self, url, **kwargs):
        return super().head(url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs) -> _RequestContextManager:
        return self.request("POST", url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs) -> _RequestContextManager:
        return self.request("PUT", url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs) -> _RequestContextManager:
        return self.request("PATCH", url, data=data, **kwargs)

    def delete(self, url, **kwargs) -> _RequestContextManager:
        return self.request("DELETE", url, **kwargs)

    async def _request(
            self,
            method: str,
            str_or_url: str,
            *args, **kwargs
    ):
        try:
            url = self._build_url(str_or_url)
        except ValueError as e:
            raise InvalidURL(str_or_url) from e

        headers = kwargs.get("headers", {})
        headers["x-cb-host"] = url.host
        kwargs["headers"] = headers
        query = f"?{'&'.join([f'{k}={v}' for k, v in url.query.items()])}" if url.query else ""
        url = URL(f"{self.api_host}{url.path}" + query)
        return await super()._request(method, url, *args, **kwargs)


class AsyncCloudbypassSessionV2(AsyncCloudbypassSession):
    def __init__(self, apikey=None, proxy=None, api_host=None, options=None, part=None):
        super().__init__(apikey, proxy, api_host, options, True, part)
