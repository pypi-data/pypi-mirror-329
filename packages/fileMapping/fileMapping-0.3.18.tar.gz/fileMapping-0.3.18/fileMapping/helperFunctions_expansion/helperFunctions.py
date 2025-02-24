"""
辅助函数

用于 辅助 fileMapping 模块的功能实现
可以不用
"""
import os
import sys
import inspect as inspectKB

from ..information import information
from ..information import fileMappingConfig

from . import empty


class fileMapping_dict(dict):
    # 用于包装字典
    # 可以通过 . 访问属性
    def __getattr__(self, item):
        if item in self:
            return self.get(item)

        else:
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{item}'")


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
    return os.path.join(os.path.dirname(cpath)if os.path.isfile(cpath)else cpath, os.path.abspath(path))


def configConvertTodict(config) -> dict:
    """
    将配置文件转换为dict格式
    :param config: 配置文件
    :return: dict 格式的配置文件
    """
    # config_type_tuple -> (dict, list, tuple)
    if isinstance(config, fileMappingConfig.config_type_tuple):
        return config

    systemConfiguration = {}
    for obj in dir(config) if not isinstance(config, fileMappingConfig.config_type_tuple) else config:
        if obj.startswith("__"):
            continue

        if isinstance(getattr(config, obj), fileMappingConfig.config_type_tuple) \
                if not isinstance(config, fileMappingConfig.config_type_tuple) else isinstance(
                config[obj], fileMappingConfig.config_type_tuple):
            systemConfiguration[obj] = configConvertTodict(getattr(config, obj))

        else:
            if not obj in dir(empty.empty):
                systemConfiguration[obj] = getattr(config, obj) \
                    if not isinstance(config, fileMappingConfig.config_type_tuple) else config[obj]

    return systemConfiguration


def parameterFilling(pointer, kwargs: dict):
    """
    填充参数

    :param pointer: 参数指向的函数
    :param kwargs: 关键字参数
    :return:
    """
    if kwargs is None:
        kwargs = {}

    return {
        key: value for key, value in kwargs.items() if key in list(inspectKB.signature(pointer).parameters.keys())
    }


def deep_update(dict1: dict, dict2: dict) -> dict:
    """
    深度合并两个字典

    :param dict1: 字典1
    :param dict2: 字典2
    """
    for key, value in dict2.items():
        if key in dict1 and isinstance(dict1[key], dict) and isinstance(value, dict):
            # 如果键存在且对应的值都是字典，则递归调用 deep_update 进行深度合并
            deep_update(dict1[key], value)
        else:
            # 否则直接更新键值对
            dict1[key] = value

    return dict1


if sys.version_info.major == 3 and sys.version_info.minor < 7:
    """
    python 3.6 以下版本，需要使用 collections.OrderedDict 排序
    """

    def sort(original_dict):
        return {key: original_dict[key] for key in sorted(original_dict.keys())}


else:
    from collections import OrderedDict

    def sort(original_dict):
        return OrderedDict(sorted(original_dict.items()))


def getAppRegister(name: str, return_value = None) -> object | None:
    """
    获取注册的应用
    :param name: 应用名称
    :return: 应用注册 object
    """
    _ = information.appRegister.get(name)
    if _ is None:
        return return_value

    return _


