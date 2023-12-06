# Cloudbypass Python SDK

## 开始使用

> 网络姻缘一线牵 珍惜这段缘

[![cloudbypass](https://img.shields.io/pypi/v/cloudbypass)](https://pypi.org/project/cloudbypass/)
[![cloudbypass](https://img.shields.io/pypi/dd/cloudbypass)](https://pypi.org/project/cloudbypass/#files)
[![cloudbypass](https://img.shields.io/pypi/wheel/cloudbypass)](https://pypi.org/project/cloudbypass/)

### 安装
    
```shell
python3 -m pip install cloudbypass -i https://pypi.org/simple
```

### 运行

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