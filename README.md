<p align="center">
  <a href="https://cloudbypass.com/" target="_blank" rel="noopener noreferrer" >
    <div align="center">
        <img src="https://raw.githubusercontent.com/cloudbypass/example/main/assets/img.png" alt="Cloudbypass" height="50">
    </div>
  </a>
</p>

## Cloudbypass SDK for Python

### 开始使用

> Cloudbypass Python SDK 仅支持 Python 3.7 及以上版本。

在`psf/requests`基础上封装的穿云SDK，支持穿云API服务的调用。通过内置的会话管理器，可以自动处理会话请求，无需手动管理Cookie等信息。

[![cloudbypass](https://img.shields.io/pypi/pyversions/cloudbypass)](https://pypi.org/project/cloudbypass/)
[![cloudbypass](https://img.shields.io/pypi/v/cloudbypass)](https://pypi.org/project/cloudbypass/)
[![cloudbypass](https://img.shields.io/pypi/dd/cloudbypass)](https://pypi.org/project/cloudbypass/#files)
[![cloudbypass](https://img.shields.io/pypi/wheel/cloudbypass)](https://pypi.org/project/cloudbypass/)

### 安装

```shell
python3 -m pip install cloudbypass -i https://pypi.org/simple
```

### 发起请求

`cloudbypass` 基于 `requests` 库，支持所有 `requests` 的方法。

通过添加初始化参数 `apikey` 和 `proxy`，分别用于设置穿云 API 服务密钥和代理 IP。

定制用户可以通过设置 `api_host` 参数来指定服务地址。

> 以上参数也可以通过环境变量 `CB_APIKEY`、`CB_PROXY` 和 `CB_APIHOST` 进行配置。

```python
from cloudbypass import Session

if __name__ == '__main__':
    with Session(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = session.get("https://opensea.io/category/memberships")
        print(resp.status_code, resp.headers.get("x-cb-status"))
        print(resp.text)
```

#### async

```python
import asyncio
from cloudbypass import AsyncSession


async def main():
    async with AsyncSession(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = await session.get("https://opensea.io/category/memberships")
        print("Status:", resp.status)
        text = await resp.text()
        print("Body:", text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

### 使用V2

穿云API V2适用于需要通过JS质询验证的网站。例如访问https://etherscan.io/accounts/label/lido ，请求示例：

```python
from cloudbypass import SessionV2

if __name__ == '__main__':
    # Cookie模式：服务端返回加密Cookie，下次请求时由客户端发送验证Cookie
    with SessionV2(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status_code, resp.headers.get("x-cb-status"))
        print("Cookie:", resp.headers.get("set-cookie"))
        print("Body:", resp.text)

    # Part模式：由服务端管理验证Cookie，客户端只需要控制part参数
    with SessionV2(apikey="<APIKEY>", proxy="http://proxy:port", part="0") as session:
        resp = session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status_code, resp.headers.get("x-cb-status"))
        print("Body:", resp.text)

```

#### async

```python
import asyncio
from cloudbypass import AsyncSessionV2


async def main():
    # Cookie模式：服务端返回加密Cookie，下次请求时由客户端发送验证Cookie
    async with AsyncSessionV2(apikey="<APIKEY>", proxy="http://proxy:port") as session:
        resp = await session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status)
        print("Cookie:", resp.headers.get("set-cookie"))
        text = await resp.text()
        print("Body:", text)

    # Part模式：由服务端管理验证Cookie，客户端只需要控制part参数
    async with AsyncSessionV2(apikey="<APIKEY>", proxy="http://proxy:port", part="0") as session:
        resp = await session.get("https://etherscan.io/accounts/label/lido")
        print("Status:", resp.status)
        text = await resp.text()
        print("Body:", text)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

### 查询余额

使用`get_balance`方法可以查询当前账户余额。

```python
from cloudbypass import get_balance

if __name__ == '__main__':
    print(get_balance("<APIKEY>", "<EMAIL>"))

```

#### async

```python
import asyncio
from cloudbypass import async_get_balance


async def main():
    print(await async_get_balance("<APIKEY>", "<EMAIL>"))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```

### 提取代理

通过`Proxy`类可以提取穿云动态代理IP和时效代理IP。

+ `copy()` 复制当前对象，使原有的对象不会受到影响。
+ `set_dynamic()` 设置为动态代理。
+ `set_expire(int)` 设置为时效代理，参数为IP过期时间，单位为秒。
+ `set_region(str)` 设置代理IP地区。
+ `clear_region()` 清除代理的地区。
+ `format(str)` 格式化代理IP，参数为格式化字符串，例如`{username}:{password}@gateway`。
+ `limit(int, str)` 返回一个代理IP字符串迭代器，参数为提取数量及代理格式化字符串。
+ `loop(int, str)` 返回一个代理IP字符串循环迭代器，参数为实际数量及代理格式化字符串。

```python
from cloudbypass import Proxy

if __name__ == '__main__':
    proxy = Proxy("username-res:password")

    # 提取动态代理
    print("Extract dynamic proxy: ")
    print(str(proxy.set_dynamic()))
    print(str(proxy.set_region('US')))

    # 提取时效代理并指定地区
    print("Extract proxy with expire and region: ")
    print(str(proxy.copy().set_expire(60 * 30).set_region('US')))

    # 批量提取
    print("Extract five 10-minute aging proxies: ")
    pool = proxy.copy().set_expire(60 * 10).set_region('US').limit(5)
    for _ in pool:
        print(_)

    # 循环提取
    print("Loop two 10-minute aging proxies: ")
    loop = proxy.copy().set_expire(60 * 10).set_region('US').loop(2)
    for _ in range(10):
        print(loop.__next__())
```

### 关于重定向问题

使用SDK发起请求时，重定向操作会自动处理，无需手动处理。且重定向响应也会消耗积分。

### 关于服务密钥

请访问[穿云控制台](https://console.cloudbypass.com/#/api/account)获取服务密钥。