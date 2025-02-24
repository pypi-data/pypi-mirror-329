[TOC]

------

# fileMapping
## 当前版本 0.3.17
用于快速调用文件夹下的py文件或者包


## 安装
使用以下命令通过pip安装fileMapping库：
```shell
pip install fileMapping
```


## 环境要求
fileMapping库的开发环境是：
    Python 3.13
    Windows 10

# 如何使用?

## 示例代码 
### 文件结构树

文件结构树

```text
-
├─ main.py
├─ latest.log
├─ config.py / config.json
└─ plugins
   ├─ a.py
   ├─ b.py
   └─ C    # 是一个包
      ├─ __init__.py
      ├─ config.py
      └─ api.py
         └─ bilibili  # 是一个函数  bilibili(id) -> url
                      # 输入一个视频id，返回视频直链
```

### `config.py`

```python
# config.py

mysql = {
    # 数据库配置
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456",
}
```

### `config.json`

```json
{
  "mysql": {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "123456"
  }
}
```

### `C\\config.py`

```python
# C\\config.py

bilibili_url = "https://www.bilibili.com/video/"

```
上述中，config.py 和 config.json 都是配置文件，我们可以根据自己的需求选择其中一个作为配置文件。

------
------

### `main.py`

```python
# main.py
from flask import Flask
from fileMapping import File, pathConversion, configConvertTodict


# 如果 config 是py文件   config.py 
import config

f = open('latest.log', 'w', encoding='utf-8')
f = File(pathConversion(__file__, 'plugins'), config=configConvertTodict(config), printPosition=f, printLog=True)
# 例 printPosition=f 日志输出位置为 latest.log 文件


# # 如果 config 是json文件   config.json
import json

with open('config.json', 'r') as f:
    config = json.load(f)
    f = File(pathConversion(__file__, 'plugins'), config=config, printLog=False)
    # 例 printLog=False 关闭日志输出


"""
上述中
- printPosition
- printLog
- config

可以不添加

"""

if __name__ == '__main__':
    app = Flask(__name__)
    f.run(app.route)


```

### `a.py`

```python
# a.py

from fileMapping import File


# 调用config-mysql-host
def main():
    print(File.public['config']['mysql']['host'])


def video_url() -> str:
    # 'BV1mNimYkErX' -> 是视频id
    return File.invoke.C.api.bilibili('BV1mNimYkErX')

```

### `b.py`

```python
# b.py

from fileMapping import File


def main(route):
    
    @route('/bilibili/<Bv_id>')
    def bv(Bv_id) -> str:
        return File.invoke.C.api.bilibili(Bv_id)

```

### `C\\__init__.py`

```python
# C\\__init__.py

from C import api  


__function__ = ''
# 只调用不运行



```

### `C\\api.py`

```python
# C\\api.py
from . import config


def bilibili(Bv_id) -> str:
    # 调用config-bilibili_url
    # 这里只是一个简单的事例
    # 这一行代码无法获取直链
    # 若想获取直链，请添加其他代码
    return config.bilibili_url + Bv_id
```


## 函数介绍

### `fileMapping.File`

```python
class File:
    """
    callObject
        - 调用对象
    invoke
        - 内行参数
    returnValue
        - 返回参数
    public
        - 公共
    """
    def __init__(self,
                 absolutePath: os.path,
                 screening=None,
                 config: dict = None,
                 printLog: bool =False,
                 printPosition=sys.stdout
        ):
        """
        映射文件夹下的Python文件或者包
        :param absolutePath: 当前的根目录绝对路径
        :param screening: 要映射的文件
        :param config: 配置文件 它将会被映射到 public['config']
        :param printLog: 是否打印日志
        :param printPosition: 日志输出位置 默认为 sys.stdout 在终端输出
        """

    def run(self, *args, name: str = None, **kwargs):
        """
        运行映射文件
        :return:
        """
```

### `fileMapping.pathConversion`

```python
def pathConversion(cpath: os.path, path: os.path) -> os.path:
    """
    当要转化的文件目录在调用文件的临旁时,则可以用这个快速转化

    例：
    |--->
        |-> plugIns
        |-> x.py

    其中x.py要调用plugIns文件夹时即可快速调用

    pathConversion(__file__, "plugIns")
    :param cpath: __file__
    :param path: 必须为文件夹
    :return:
    """

```


### `fileMapping.configConvertTodict`

```python

def configConvertTodict(config) -> dict:
    """
    将配置文件转换为dict格式
    :param config: 配置文件
    :return: dict 格式的配置文件
    """

```
------

## [更新日志](https://github.com/bop-lp/fileMapping/blob/main/changelog.md)

