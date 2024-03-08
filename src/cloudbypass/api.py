from aiohttp.client import _RequestContextManager

from . import sessions


def request(method, url, **kwargs):
    with sessions.CloudbypassSession() as session:
        return session.request(method=method, url=url, **kwargs)


def get(url, params=None, **kwargs):
    return request("get", url, params=params, **kwargs)


def options(url, **kwargs):
    return request("options", url, **kwargs)


def head(url, **kwargs):
    kwargs.setdefault("allow_redirects", False)
    return request("head", url, **kwargs)


def post(url, data=None, json=None, **kwargs):
    return request("post", url, data=data, json=json, **kwargs)


def put(url, data=None, **kwargs):
    return request("put", url, data=data, **kwargs)


def patch(url, data=None, **kwargs):
    return request("patch", url, data=data, **kwargs)


def delete(url, **kwargs):
    return request("delete", url, **kwargs)


def get_balance(apikey=None):
    with sessions.CloudbypassSession() as session:
        return session.get_balance(apikey=apikey)


async def _async_request(method, url, **kwargs):
    return await sessions.AsyncCloudbypassSession().request(method=method, url=url, **kwargs)


def async_request(method, url, **kwargs) -> _RequestContextManager:
    return _RequestContextManager(_async_request(method, url, **kwargs))


def async_get(url, params=None, **kwargs) -> _RequestContextManager:
    return async_request("get", url, params=params, **kwargs)


def async_options(url, **kwargs) -> _RequestContextManager:
    return async_request("options", url, **kwargs)


def async_head(url, **kwargs) -> _RequestContextManager:
    kwargs.setdefault("allow_redirects", False)
    return async_request("head", url, **kwargs)


def async_post(url, data=None, json=None, **kwargs) -> _RequestContextManager:
    return async_request("post", url, data=data, json=json, **kwargs)


def async_put(url, data=None, **kwargs) -> _RequestContextManager:
    return async_request("put", url, data=data, **kwargs)


def async_patch(url, data=None, **kwargs) -> _RequestContextManager:
    return async_request("patch", url, data=data, **kwargs)


def async_delete(url, **kwargs) -> _RequestContextManager:
    return async_request("delete", url, **kwargs)


async def async_get_balance(apikey=None):
    async with sessions.AsyncCloudbypassSession() as session:
        return await session.get_balance(apikey=apikey)