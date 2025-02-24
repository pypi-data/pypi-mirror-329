"""
这个文件用于加载插件
plugIns
"""
import os
import importlib
# import importlib.util
import sys
import traceback
from typing import Any
import inspect as inspectKB
import copy

from .information import fileMappingConfig as config
from .helperFunctions_expansion import helperFunctions as hF
from . import string

"""
empty 一个空 函数/方法
    - 当导入错误时，触发空函数，为了防止调用错误

method 公共方法

packageMethod(method)  包类
    
fileMethod(method)  文件类

f 调用函数
"""
class blacklist: ...


class empty:
    # 一个空函数/方法
    class main:
        def __init__(self): ...

    def run(self, **kwargs): ...

    def __init__(self):
        self.main = self.main()


class method:
    def __init__(self, path):
        self.pointer = None
        self.pack: Any| empty = None
        self.magicParameters: dict[str: Any] = {}
        # 调用对象
        self.path: str = path
        self.absolutePath = self.path if os.path.isabs(self.path) == True else os.path.realpath(self.path)
        # 相对路径 & 绝对路径
        logs = self.__import__()
        # 导入包
        if logs[0] is False:
            self.logs = logs[-1]

        else:
            self.logs = True


    def run(self, **kwargs):
        """
        运行包
        :return:
        """
        try:
            parameterFilling = hF.parameterFilling(self.pointer, kwargs)
            return self.pointer(**parameterFilling)

        except config.error_list_a2 as e:
            a = traceback.format_exc()
            return e

    def get(self, func):
        return {
            value: getattr(func, value) if value in dir(func) else config.functions[value]
            for value, data in config.functionsName.items()
        }

    def __import__(self) -> tuple:
        """
        导入包
        """
        logs = {}
        try:
            logs[1] = {}
            self.pack = py_import(
                os.path.dirname(self.absolutePath), os.path.basename(self.path)
            )
            if isinstance(self.pack, config.error_list_a2):
                logs[1] = {"error": self.pack, "traceback": traceback.format_exc(), "absolutePath": self.absolutePath, "path": self.path}
                return (False, logs)
            # builtInParameters = self.get(self.pack)
            # 获取包内的内定参数 & 没有就向config.functions中获取

        except config.error_list_a2 as e:
            logs[1] = {"error": e, "traceback": traceback.format_exc(), "absolutePath": self.absolutePath, "path": self.path}
            self.pack = empty()
            self.pointer = self.pack.run
            # builtInParameters = config.functions_bad

        # if builtInParameters[config.functionsName['__run__']] is False:
        #     # 禁止运行
        #     self.pointer = empty().run
        #     logs[2] = {"builtInParameters": builtInParameters, "absolutePath": self.absolutePath, "path": self.path}
        #     return (False, logs)
        #
        # elif builtInParameters[config.functionsName['__function__']] == '':
        #     self.pointer = empty().run
        #     logs[2] = {"builtInParameters": builtInParameters, "absolutePath": self.absolutePath, "path": self.path}
        #     return (False, logs)
        #
        # elif builtInParameters[config.functionsName['__function__']] in dir(self.pack):
        #     self.pointer = getattr(self.pack, builtInParameters[config.functionsName['__function__']])
        #     logs[2] = {"builtInParameters": builtInParameters, "absolutePath": self.absolutePath, "path": self.path}
        #     return (True, logs)

        if (self.pointer is None) and (self.pack is None):
            # 无 main
            string.thereIsNoMainFunction(self.path)
            return (False, logs)

        else:
            return (True, logs)


class packageMethod(method):
    """包方法"""
    __name__ = 'packageMethod'


class fileMethod(method):
    """文件方法"""
    __name__ = 'fileMethod'


def f(path: str) -> packageMethod | fileMethod | bool:
    """
    
    :param path: 
    """
    if path.endswith('__init__.py'):
        return packageMethod(os.path.dirname(path))

    else:
        return fileMethod(path)


def py_import(file_path: os.path, callObject: str):
    """
    :param callObject: 'main'
    :param file_path: 绝对路径
    :return:

    """
    path = copy.copy(sys.path)
    callObject = callObject.split('.')[0]  # 去除 .py
    try:
        sys.path = config.path+[file_path]
        the_api = importlib.import_module(callObject)

    except config.error_list_a2 as e:
        sys.path = path
        return e

    else:
        sys.path = path
        return the_api

