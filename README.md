<p align="center">
  <a href="https://cloudbypass.com/" target="_blank" rel="noopener noreferrer" >
    <div align="center">
        <img src="https://github.com/cloudbypass/example/blob/main/assets/img.png?raw=true" alt="Cloudbypass" height="50">
    </div>
  </a>
</p>


## Cloudbypass SDK for Python

### 开始使用

> Cloudbypass Python SDK 仅支持 Python 3.6 及以上版本。

在`psf/requests`基础上封装的穿云SDK，支持穿云API服务的调用。通过内置的会话管理器，可以自动处理会话请求，无需手动管理Cookie等信息。

使用`get_balance`方法可以查询当前账户余额。

[![cloudbypass](https://img.shields.io/pypi/pyversions/cloudbypass)](https://pypi.org/project/cloudbypass/)
[![cloudbypass](https://img.shields.io/pypi/v/cloudbypass)](https://pypi.org/project/cloudbypass/)
[![cloudbypass](https://img.shields.io/pypi/dd/cloudbypass)](https://pypi.org/project/cloudbypass/#files)
[![cloudbypass](https://img.shields.io/pypi/wheel/cloudbypass)](https://pypi.org/project/cloudbypass/)

### 安装

```shell
python3 -m pip install cloudbypass -i https://pypi.org/simple
```

### 发起请求

`Session`类继承自`requests.Session`，支持`requests`的所有方法。

增加初始化参数`apikey`和`proxy`，分别用于设置穿云API服务密钥和代理IP。

定制用户可以通过设置`api_host`参数来指定服务地址。

> 以上参数可使用环境变量`CB_APIKEY`、`CB_PROXY`和`CB_APIHOST`进行配置。

```python
from cloudbypass import Session

if __name__ == '__main__':
    with Session(apikey="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", proxy="http://proxy:port") as session:
        resp = session.get("https://opensea.io/category/memberships")
        print(resp.status_code, resp.headers.get("x-cb-status"))
        print(resp.text)
```

### 查询余额

```python
from cloudbypass import Session

if __name__ == '__main__':
    with Session(apikey="xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") as session:
        print(session.get_balance())

```

### 关于重定向问题

使用SDK发起请求时，重定向操作会自动处理，无需手动处理。且重定向响应也会消耗积分。

### 关于服务密钥

请访问[穿云控制台](https://console.cloudbypass.com/#/api/account)获取服务密钥。