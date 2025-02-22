"""
多线程处理


用 concurrent.futures 模块实现多线程处理
python 3.2 及以上版本才支持

"""
import concurrent.futures

from .. import register
from ..register import parameters_wrapper
from .helperFunctions import deep_update
from .helperFunctions import sort

task = {
    0: [object, ...],
    1: {
        "taskName": object
    },
    2: {
        0: [...],
        1: {...},
    },
}
# 任务字典, key 为任务编号, value 为任务列表
multithreading = None


def _task_run(executor: concurrent.futures.ThreadPoolExecutor, task_list: list, wrapper_list: list = None, wrapper_parameters: dict = None, parameters: dict = None):
    """
    任务执行函数

    :param executor: 线程池
    :param task_list: function list
    :param wrapper_list: 装饰列表
    :param wrapper_parameters: 装饰器参数字典
    :param parameters: 参数字典
    :return: 任务执行结果
    """

    def func(executor, wrapper_list, wrapper_parameters, task_func, *args, **kwargs) -> concurrent.futures.Future:
        return executor.submit(register.wrapper_recursion(wrapper_list, task_func, wrapper_parameters), *args, **kwargs)

    wrapper_list = [parameters_wrapper] if wrapper_list is None else wrapper_list + [parameters_wrapper]
    parameters = {} if parameters is None else parameters
    wrapper_parameters = {} if wrapper_parameters is None else wrapper_parameters

    wrapper_parameters = deep_update(wrapper_parameters, {"parameters": {"parameters": parameters}})
    futures = []
    for task_info in task_list:
        if isinstance(task_info, tuple):
            # 如果是元组，假设第一个元素是任务函数，后面的元素是位置参数
            task_func = task_info[0]
            args = task_info[1:]
            future = func(executor, wrapper_list, wrapper_parameters, task_func, *args)

        elif isinstance(task_info, dict):
            # 如果是字典，假设 'func' 键对应任务函数，其他键为关键字参数
            task_func = task_info.pop('func')
            future = func(executor, wrapper_list, wrapper_parameters, task_func, **task_info)

        else:
            # 如果不是元组也不是字典，直接认为是无参数的任务函数
            future = func(executor, wrapper_list, wrapper_parameters, task_info)
        futures.append(future)

    return futures


def task_run(*args, **kwargs) -> list:
    """
    任务执行函数
    这里会阻塞等待所有任务完成
    :return: 任务执行结果列表
    """
    futures = _task_run(*args, **kwargs)
    concurrent.futures.wait(futures)
    # 等待所有任务完成
    thread_return = [future.result()
                     if future.exception() is None else future.exception()
                     for future in futures]
    # 获取所有任务结果
    return thread_return


def task_recursion(task: dict, *args, **kwargs):
    if isinstance(next(iter(task)), str):
        # 任务名称存在, 提交任务到线程池
        value = task_run(task_list=list(task.values()), *args, **kwargs)
        key = list(task.keys())
        return {
            key[i]: value[i] for i in range(len(key))
        }

    else:
        task = sort(task)

        return {
            key: task_recursion(task_list=value, *args, *kwargs)
            if isinstance(value, dict) else task_run(value, *args, **kwargs)
            for key, value in task.items()
        }


def task_run_clogging(*args, **kwargs):
    """
    任务执行函数
    不会阻塞等待所有任务完成
    """

    return _task_run(*args, **kwargs)


def task_recursion_clogging(task: dict, *args, **kwargs):
    """
    递归处理任务字典
    :param task: 任务字典
    :return: None
    """
    # task = sort(task)  # 排序字典
    if isinstance(next(iter(task)), str):
        # 任务名称存在, 提交任务到线程池
        value = task_run_clogging(list(task.values()), *args, **kwargs)
        key = list(task.keys())
        return {
            key[i]: value[i] for i in range(len(key))
        }

    else:
        task = sort(task)
        # 排序字典

    return {
        key: task_recursion_clogging(value, *args, **kwargs)
        if isinstance(value, dict) else task_run_clogging(value, *args, **kwargs)
        for key, value in task.items()
    }


def threadPools(task: dict, wrapper_list: list = None, wrapper_parameters: dict=None, max_workers: int = 3, callback_function=None, errorHandling=None,
                parameters: dict = None):
    """
    多线程处理
    :param task: 任务字典
    :return: 任务处理结果
    """
    try:
        # 创建线程池
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # 递归处理任务字典
            return_DATA = task_recursion(executor=executor, task=task, wrapper_list=wrapper_list, wrapper_parameters=wrapper_parameters, parameters=parameters)

            if callback_function is not None:
                # 回调函数处理结果
                return callback_function(return_DATA)
            else:
                return return_DATA

    except Exception as e:
        if errorHandling is not None:
            # 错误处理函数处理错误
            return errorHandling(e)
        else:
            return e


class enableMultithreading:
    def __init__(self, max_workers: int = 3, callback_function=None, errorHandling=None):
        """
        多线程处理
        """
        self.max_workers = max_workers
        self.callback_function = callback_function
        self.errorHandling = errorHandling

        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

    def __func__(self, func, **kwargs):
        return func(executor=self.executor, **kwargs)

    def task_run(self, task_list: list, clogging: bool=True, wrapper_list: list=None, wrapper_parameters: dict=None, parameters: dict=None):
        kwargs = {
            "task_list": task_list,
            "wrapper_list": wrapper_list,
            "wrapper_parameters": wrapper_parameters,
            "parameters": parameters
        }
        if not clogging:
            return self.__func__(task_run_clogging, **kwargs)

        else:
            return self.__func__(task_run, **kwargs)

    def task_recursion(self, task_dict: dict, clogging: bool=True, wrapper_list: list=None, wrapper_parameters: dict=None, parameters: dict=None) -> dict:
        kwargs = {
            "task": task_dict,
            "wrapper_list": wrapper_list,
            "wrapper_parameters": wrapper_parameters,
            "parameters": parameters
        }

        if not clogging:
            return self.__func__(task_recursion_clogging, **kwargs)
            # return task_recursion_clogging(executor=self.executor, task=task_dict, wrapper_list=wrapper_list, wrapper_parameters=, parameters=parameters)

        else:
            return self.__func__(task_recursion, **kwargs)
            # return task_recursion(executor=self.executor, task=task_dict, wrapper_list=wrapper_list, wrapper_parameters, parameters=parameters)

    def close(self):
        self.executor.shutdown()
