
from .. import register
from ..helperFunctions_expansion.informationProcessing import get_all
from ..helperFunctions_expansion.multithreading import enableMultithreading


def _task(func, T: enableMultithreading, text_dict: dict):
    task: list = [(func, i[-1]) for i in text_dict.items()]
    task: list[dict] = T.task_run(task)

    _, i = {}, 0
    for key in text_dict:
        _[key] = task[i]
        i += 1

    return _


def file_read(T: enableMultithreading, path_dist: dict, mode: str = 'r', encoding: str = 'utf-8'):
    """
    多线程读取文件内容

    :param T: enableMultithreading object
    :param path_dist: list of file paths
    :param mode: file open mode
    :param encoding: file encoding
    :return: list of file objects
    """
    def func(path):
        with open(path, mode=mode, encoding=encoding) as f:
            return f.read()

    return _task(func, T, path_dist)


def text_parsing(T: enableMultithreading, text_dict: dict):
    """
    多线程文件内容解析

    :param T: enableMultithreading object
    :param text_dict: list of file contents
    :return: list of parsed contents
    """
    def func(text):
        return get_all(text)

    return _task(func, T, text_dict)


def file_import(T: enableMultithreading, import_func, file_list: list, file_path_list: dict, **kwargs):
    """
    多线程文件导入

    :param T: enableMultithreading object
    :param import_func: function for importing file
    :param file_list: list of file objects
    :param file_path_list: list of file paths
    :return: list of imported objects
    """
    def wrapper_func(name: str):
        @register.my_wraps(name)  # 效果是保证, 在层层(包装/装饰)下名字不变
        def func(file_name: str):
            return import_func(file_path_list[file_name])

        return func

    return T.task_run([(wrapper_func(i), i) for i in file_list], **kwargs)

