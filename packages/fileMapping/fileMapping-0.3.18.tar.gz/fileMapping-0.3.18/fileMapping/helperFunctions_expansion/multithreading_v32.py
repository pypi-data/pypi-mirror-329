"""
多线程处理文件映射

用 threading 模块实现多线程处理文件映射。
Version： python3.2 以下版本
"""

import threading

from ..register import timeit_wrapper
from .helperFunctions import sort


def task_run(task_list: list, semaphore: threading.Semaphore) -> list:
    """
    任务执行函数
    这里会阻塞等待所有任务完成
    :return: 任务执行结果列表
    """
    threads = []
    results = [None] * len(task_list)

    def run_task(index, task_info):
        with semaphore:
            if isinstance(task_info, tuple):
                # 如果是元组，假设第一个元素是任务函数，后面的元素是位置参数
                task_func = task_info[0]
                args = task_info[1:]
                results[index] = timeit_wrapper(task_func)(*args)
            elif isinstance(task_info, dict) and 'func' in task_info:
                # 如果是字典且包含 'func' 键，将其视为带关键字参数的任务
                task_func = task_info.pop('func')
                results[index] = timeit_wrapper(task_func)(**task_info)
            elif callable(task_info):
                # 如果是可调用对象，直接作为无参数任务
                results[index] = timeit_wrapper(task_info)()
            else:
                raise ValueError(f"Invalid task info: {task_info}")

    for i, task_info in enumerate(task_list):
        thread = threading.Thread(target=run_task, args=(i, task_info))
        threads.append(thread)
        thread.start()

    # 等待所有线程完成
    for thread in threads:
        thread.join()

    return results


def task_recursion(task: dict, semaphore: threading.Semaphore) -> dict:
    if all(isinstance(key, str) for key in task):
        # 如果所有键都是字符串，认为是任务名称字典，提交任务
        value = task_run(list(task.values()), semaphore)
        key = list(task.keys())
        return {
            key[i]: value[i] for i in range(len(key))
        }
    else:
        task = sort(task)
        return {
            key: task_recursion(value, semaphore) if isinstance(value, dict) else task_run([value] if not isinstance(value, list) else value, semaphore)
            for key, value in task.items()
        }


def threadPools(task: dict, max_workers: int = 3, callback_function=None, errorHandling=None):
    """
    多线程处理
    :param task: 任务字典
    :return: 任务处理结果
    """
    semaphore = threading.Semaphore(max_workers)
    try:
        # 递归处理任务字典
        return_DATA = task_recursion(task, semaphore)

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
