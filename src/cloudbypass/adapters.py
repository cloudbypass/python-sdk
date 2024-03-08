from urllib.parse import urlparse
from requests.adapters import HTTPAdapter


class CfbHTTPAdapter(HTTPAdapter):

    def __init__(self, api_host):
        super().__init__()
        self.api_host = api_host

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
