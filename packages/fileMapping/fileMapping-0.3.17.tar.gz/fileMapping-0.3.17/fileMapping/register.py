"""
用于注册文件映射

注册后会保存到 fileMapping.register_DATA 字典中

"""
import functools
import time

# import rich
from . information import information
from .helperFunctions_expansion import helperFunctions as hF
from .helperFunctions_expansion import informationProcessing as iP


def threadRegistration(separate: bool = False, mainThread: bool = False, timingOfOperation: int = 1,
                       __level__: int = -1):
    """
    - 只会运行一次

    :param separate: 是否分开运行
        - 是否分开运行, 即是否在单独的线程中运行
        - 运行效率慢

    :param mainThread: 是否在主线程中运行
        - 一般的运行会在线程池中抽出线程来进行执行

    :param timingOfOperation: 运行时机
        - -1: __function__(main) 运行之前
        - 0: __function__(main) 运行之后
        - 1: 当所有插件都 __function__(main) 运行完毕之后

    :param __level__: 运行等级
        - 何时有用？
        - 当 timingOfOperation = 1 时
        - 会进行排序，然后进行异步执行
    """


def tickTask(tick: int = 1, timeout: bool | int = False, __level__: int = -1):
    """
    - 每个 tick 都会运行一次

    :param tick: 运行间隔
    :param timeout: 超时时间
        - 超过这个时间后 任务会停止
    :param __level__: 运行等级
    """


def secondsTask(seconds: int = 1, timeout: bool | int = False, __level__: int = -1):
    """
    - 每个 1s 段时间就会运行一次

    :param seconds: 运行间隔
    :param timeout: 超时时间
        - 超过这个时间后 任务会停止
    :param __level__: 运行等级
    """



def appRegister(func, name: str = None):
    """
    这是一个装饰器，用于注册插件
    注册后会保存到 fileMapping.information.appRegister 字典中
    -> {name: Register object}

    :param func: 注册函数
    :param name: 注册名称
    """
    information["appRegister"][name if not name is None else func.__name__] = func

    return func


"""
以下是 fileMapping 内部使用的register函数
"""


def timeit_wrapper(func):
    # time & 装饰器
    def wrapper(*args, **kwargs) -> dict:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return {
            "result": result,
            "time": end_time - start_time
        }

    return wrapper


def parameters_wrapper(func, parameters):
    # 参数装饰器
    if parameters is None:
        parameters = {}

    def wrapper(*args, **kwargs) -> dict:
        pa = hF.parameterFilling(func, parameters | kwargs)
        # 参数填充
        return func(*args, **pa)

    wrapper.__name__ = func.__name__
    return wrapper


# def wrapper_recursion(wrapper_list: list, func, parameter_library: dict):
#     print(">>> wrapper_recursion ", wrapper_list, func, parameter_library)
#     return parameters_wrapper(wrapper_list[0](func), parameter_library) \
#         if wrapper_list.__len__() == 1 \
#         else wrapper_recursion(wrapper_list[1:], parameters_wrapper(wrapper_list[0](func), parameter_library), parameter_library)


def wrapper_recursion(wrapper_list: list, func, parameter_library: dict):
    return wrapper_list[0](parameters_wrapper(func, parameter_library), parameter_library) \
        if wrapper_list.__len__() == 1 \
        else wrapper_recursion(wrapper_list[1:], wrapper_list[0](parameters_wrapper(func, parameter_library)),
                               parameter_library)


def my_wraps(name):
    """
    在层层(包装/装饰)下名字不变

    :param name: 名字
    """

    def decorator(func):
        func.__name__ = name

        return func

    return decorator


class TimeWrapper:
    def __init__(self):
        self.data = {}

    def wrapper(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            self.data[func.__name__] = {
                "init": start_time,
                "end": end_time,
                "take": end_time - start_time
            }
            return result

        return wrapper

    def get_data(self, func_id):
        return self.data.get(func_id, None)


class InfoWrapper:
    def __init__(self, info_dict):
        """
        信息装饰器
        可以快速的获取 file_object 的信息
        :param info_dict: 信息字典
            - 文件信息字典 {infoName: messageDefaults, ...}
        """
        self.info_dict = info_dict if not info_dict is None else {}
        self.data = {}

    def wrapper(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            self.data[func.__name__] = iP.get_file_info(result.pack, self.info_dict)

            return result

        return wrapper


def threadRegistration(separate: bool = False, mainThread: bool = False, timingOfOperation: int = 1,
                       __level__: int = -1, **kwargs):
    """
    - 只会运行一次

    :param separate: 是否分开运行
        - 是否分开运行, 即是否在单独的线程中运行
        - 运行效率慢

    :param mainThread: 是否在主线程中运行
        - 一般的运行会在线程池中抽出线程来进行执行

    :param timingOfOperation: 运行时机
        # -1: __function__(main) 运行之前
        # - 0: __function__(main) 运行之后
        - 1: 当所有插件都 __function__(main) 运行完毕之后

    :param __level__: 运行等级
        - 何时有用？
        - 当 timingOfOperation = 1 时
        - 会进行排序，然后进行异步执行

    :param kwargs: 其他参数
        - 其他参数会被传递给 func 函数
    """
    def wrapper(func):
        information["readRegistration"][func] = {
            "separate": separate,
            "mainThread": mainThread,
            "timingOfOperation": timingOfOperation,
            "level": __level__,
            "kwargs": kwargs
        }
        return func

    return wrapper
