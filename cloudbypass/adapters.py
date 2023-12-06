import os
import re
from urllib.parse import urlparse
from requests.adapters import HTTPAdapter


def get_api_host(api_host=None):
    res = re.match(
        r"^((?:http|https):(//)?)?([\w.-]+)(:(\d+))?$",
        api_host or os.environ.get("CB_API_HOST", "https://api.cloudbypass.com")
    )
    if not res:
        raise ValueError("Invalid ENV_API_HOST")

    port = res.group(5)
    return ((res.group(1) or 'https:').strip('//') + "//") + res.group(3) + (':' + port if port else '')


ENV_API_HOST = get_api_host()


class CfbHTTPAdapter(HTTPAdapter):

    def __init__(self, api_host=None):
        super().__init__()
        self.api_host = get_api_host(api_host) or ENV_API_HOST

    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        request = request.copy()
        url = urlparse(request.url)
        request.url = f"{self.api_host}{url.path}" + (f"?{url.query}" if url.query else "")
        request.headers["x-cb-host"] = url.hostname
        request.headers["x-cb-protocol"] = url.scheme
        resp = super().send(
            request,
            stream=stream,
            timeout=timeout,
            verify=verify,
            cert=cert,
            proxies=proxies,
        )
        resp.request.url = url.geturl()
        return resp
