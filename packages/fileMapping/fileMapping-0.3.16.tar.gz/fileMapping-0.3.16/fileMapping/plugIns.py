import _io
import os
import sys
import atexit
import time
import types

# try:
#     from rich import inspect
#     import rich
#     # 这里是测试时用的, 实际上应该注释掉

# except ImportError:
#     pass

from . import information as fileMapping_information
from .helperFunctions_expansion import helperFunctions
from .helperFunctions_expansion.helperFunctions import fileMapping_dict
from .helperFunctions_expansion import multithreading

from .information import error as file_error
from . import helperFunctions_expansion
from .multithreading_fileMapping import fileMapping_func
from . import pluginLoading
from .information import fileMappingConfig as fileMappingConfig
from . import string
from . import register

Application: fileMapping_information.fileMapping_dict = fileMapping_information.Application
# Application = fileMapping_dict({})


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
    information
        - 信息
    logs
        - 日志
    """
    callObject: fileMapping_information.fileMapping_dict = fileMapping_information.callObject
    invoke: fileMapping_information.fileMapping_dict = fileMapping_information.invoke
    returnValue: fileMapping_information.fileMapping_dict = fileMapping_information.returnValue
    public: fileMapping_information.fileMapping_dict = fileMapping_information.public
    information: fileMapping_information.fileMapping_dict = fileMapping_information.information
    logs: fileMapping_information.fileMapping_dict = fileMapping_information.logs

    # callObject = fileMapping_dict({})
    # invoke = fileMapping_dict({})
    # returnValue = fileMapping_dict({})
    # public = fileMapping_dict({})
    # information = fileMapping_dict({})
    # logs = fileMapping_dict({"run": 1})
    path = None

    def __init__(self,
                 absolutePath: os.path,
                 screening=None,
                 config: dict = None,
                 printLog: bool = False,
                 printPosition = sys.stdout
        ):
        """
        映射文件夹下的Python文件或者包
        :param absolutePath: 当前的根目录绝对路径
        :param screening: 要映射的文件
        :param config: 配置文件 它将会被映射到 public['config']
        :param printLog: 是否打印日志
        :param printPosition: 日志输出位置 默认为 sys.stdout 在终端输出
        """
        """
        设计思路
        
        1. 遍历文件夹下的所有文件
        2. 筛选出符合要求的文件
        3. 加载配置文件
        4. 加载映射文件 
            - 多线程 & 异步
        5. 运行映射文件
            - 多线程 & 异步
        """
        if screening is None:
            screening = ["py"]

        if not ((not os.path.isabs(absolutePath)) or (not os.path.islink(absolutePath))):
            raise FileNotFoundError(f"不是一个有效的绝对路径。: '{absolutePath}'")

        # 加载配置文件
        self.public["config"] = helperFunctions.deep_update(helperFunctions.configConvertTodict(fileMapping_information.config), config) \
            if config else helperFunctions.configConvertTodict(fileMapping_information.config)

        self.printLog = printLog
        self.printPosition = printPosition
        self.path = absolutePath

        self.run_order = {}
        self.listOfFiles = {}
        fileMappingConfig.log['printPosition'] = self.printPosition
        fileMappingConfig.log['printLog'] = self.printLog
        self.listOfFiles = {
            i.split('.')[0]: os.path.join(absolutePath, i)
            if os.path.isfile(os.path.join(absolutePath, i)) and i.split('.')[-1] in screening
            else os.path.join(absolutePath, i, fileMappingConfig.functionsName["__init__.py"])
            for i in os.listdir(absolutePath)
            if(os.path.isfile(os.path.join(absolutePath, i)))
            or(os.path.isdir(os.path.join(absolutePath, i))
            and os.path.isfile(os.path.join(absolutePath, i, fileMappingConfig.functionsName["__init__.py"])))
        }
        if self.public.config.get('multithreading', False):
            self.multithreading = multithreading.enableMultithreading(
                self.public['config']['numberOfThreads']
            )
            self.__multithreading__()

        else:
            self.__singleThreaded__()
        # 使用应用参数
        Application["end"] = helperFunctions_expansion.parameterApplication.ApplyParameter(self)

    def __run__(self, name, kwargs):
        """
        运行映射文件
        :return:
        """
        _ = self.returnValue[name] = self.callObject[name].run(**kwargs)
        if not isinstance(_, fileMappingConfig.error_list_a2):
            string.theRunFileWasSuccessful(name)

        else:
            string.theRunFileFailed(name, _)

    def runAll(self, **kwargs):
        """
        运行所有映射文件
        :return:
        """
        for key, data in self.run_order.items():
            for i in data:
                if self.callObject[i]:
                    self.__run__(i, kwargs)

    def runOne(self, name: str, **kwargs):
        """
        运行单个映射文件
        :return:
        """
        if self.callObject.get(name, False):
            self.__run__(name, kwargs)

        else:
            string.errorNoFile(name)

    def run(self, name: str = None, **kwargs):
        """
        计划在后续版本移除

        运行映射文件
        :return:
        """
        if name is None:
            for key, data in self.listOfFiles.items():
                if self.callObject[key]:
                    self.__run__(key, kwargs)

        else:
            if self.callObject.get(name, False):
                self.__run__(name, kwargs)

            else:
                string.errorNoFile(name)

    def __multithreading__(self):
        """
        多线程运行
        :return:
        """
        # 读取文件 & 文本解析 & 排序插件
        self.run_order = fileMapping_func.file_read(self.multithreading, self.listOfFiles)
        self.run_order = fileMapping_func.text_parsing(self.multithreading, self.run_order)
        self.run_order = helperFunctions_expansion.informationProcessing.sorting_plugin(self.run_order)
        if not isinstance(self.run_order, tuple):
            time_wrapper = register.TimeWrapper()
            info_wrapper = register.InfoWrapper(fileMappingConfig.functions)
            for __level__, L in self.run_order.items():
                data = fileMapping_func.file_import(self.multithreading, pluginLoading.f, L, self.listOfFiles,
                                                    wrapper_list=[time_wrapper.wrapper, info_wrapper.wrapper])
                self.callObject |= dict(zip(L, data))
                self.invoke |= dict(zip(L, [i.pack for i in data]))
                # TypeError（“'NoneType' 对象不可下标”）

            else:
                # 获取 时间 & 信息 -> information.run_time & file_info
                self.information["run_time"] = time_wrapper.data
                self.information["file_info"] = info_wrapper.data

        else:
            # sorting_plugin -> tuple 表示插件循环依赖
            self.logs = file_error.circularDependenciesError(self.logs, self.run_order)
            return False

    def __singleThreaded__(self):
        """
        单线程运行
        """
        # 读取文件 & 文本解析 & 排序插件
        self.run_order = {}
        for i in self.listOfFiles:
            with open(self.listOfFiles[i], "r", encoding="utf-8") as f:
                self.run_order[i] = helperFunctions_expansion.informationProcessing.get_all(f.read())

        self.information = {"file_info": self.run_order, "run_time": {}}
        self.run_order = helperFunctions_expansion.informationProcessing.sorting_plugin(self.run_order)
        if not isinstance(self.run_order, tuple):
            time_wrapper = register.TimeWrapper()
            info_wrapper = register.InfoWrapper(fileMappingConfig.functions)
            for __level__, L in self.run_order.items():
                for name in L:
                    pluginLoading.f.__name__ = name
                    self.callObject[name] = info_wrapper.wrapper(time_wrapper.wrapper(pluginLoading.f))(self.listOfFiles[name])
                    self.invoke[name] = self.callObject[name].pack

            else:
                # 获取 时间 & 信息 -> information.run_time & file_info
                self.information["run_time"] = time_wrapper.data
                self.information["file_info"] = info_wrapper.data

        # sorting_plugin -> tuple 表示插件循环依赖
        else:
            file_error.circularDependenciesError(self.logs, self.run_order)
            return False


@atexit.register
def end():
    """
    结束插件运行
    :return:
    """
    if not fileMappingConfig.endTheTask:
        return

    for key, value in File.invoke.items():
        if fileMappingConfig.functionsName["__end__"] in dir(value):
            name = getattr(value, fileMappingConfig.functionsName["__end__"])
            if isinstance(name, types.FunctionType):
                try:
                    name()

                except fileMappingConfig.error_list_a2 as e:
                    string.endFailed(key, e)

                continue

            if not name in dir(value):
                string.endfunctionNotFound(key, name)
                continue

            pointer = getattr(value, name)
            try:
                pointer()
                continue

            except fileMappingConfig.error_list_a2 as e:
                string.endFailed(key, e)


@atexit.register
def fileMapping_end():
    """
    结束
    :return:
    """
    for i in Application.get("end", []):
        try:
            i()

        except Exception as e:
            pass


def temporaryFolders(name: str, *args) -> str | bool:
    """
    临时文件夹
    :return:
    """
    if name in File.information.temporaryFolders:
        if args is None:
            return File.information.temporaryFolders[name]

        else:
            return os.path.join(File.information.temporaryFolders[name], *args)

    else:
        return False


def fileOperations(path: str, *args, **kwargs) -> _io.open:
    """
    文件操作
    :return:
    """
    try:
        file = open(path, *args, **kwargs)
        return file

    except Exception as e:
        return False