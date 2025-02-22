import _io

"""
这是一个用于插件模板文件, 定义参数或者方法
"""

__function__ = object
# 参数名称: 运行函数
# 是否必须: 否
# 加入版本: init
# 类型: object
# 默认值: main
# 描述: 用于指定运行时的函数
# 在之前的版本(0.3.8)必须是字符串, 现版本可以是函数对象或者字符串, 字符串会被解释为函数名


__version__ = int
# 参数名称: 插件版本
# 是否必须: 否
# 加入版本: 0.3.15
# 类型: str
# 默认值: 1
# 描述: 插件的版本号, 用于标识插件的不同版本


__run__ = bool
# 参数名称: 是否运行
# 是否必须: 否
# 加入版本: 0.3.3
# 类型: bool
# 默认值: True
# 描述: 用于指定是否运行插件, 默认为True
# 当为False时, 插件不会运行, 但会被加载到内存中
# 一般由API进行使用


__level__ = int
# 参数名称: 运行等级
# 是否必须: 否
# 加入版本: 0.3.13
# 类型: int
# 默认值: -1
# 描述: 用于指定插件运行的优先级, 值越大, 优先级越高
# 当多个插件同时运行时, 按照优先级进行运行
# 一般由API进行使用

__dependencyPackages__ = list | dict
# 参数名称: 依赖包
# 是否必须: 否
# 加入版本: 0.3.15
# 类型: list | dict
# 默认值: []
# 描述: 用于指定插件运行所需的依赖包
# dict 类型时, 格式为 {"packageName": "version", ...}
# list 类型时, 格式为 ["packageName", "packageName", ...]


__dependenciesOnPlugins__ = list | dict
# 参数名称: 依赖插件
# 是否必须: 否
# 加入版本: 0.3.15
# 类型: list | dict
# 默认值: []
# 描述: 用于指定插件运行所需的依赖插件
# dict 类型时, 格式为 {"pluginName": "version", ...}
# list 类型时, 格式为 ["pluginName", "pluginName", ...]


__temporaryFolders__ = str | list
# 参数名称: 临时文件夹
# 是否必须: 否
# 加入版本: 0.3.15
# 类型: str | list
# 默认值: None
# 描述: 用于申请一个临时文件夹
# fileMapping 会在init时申请一个临时文件夹, 并在插件结束时删除
# fileMapping.temporaryFolders() 会返回申请的临时文件夹路径
# 无法动态申请


__error__ = object
# 参数名称: 错误处理函数
# 是否必须: 否
# 加入版本: 0.3.15
# 类型: object
# 默认值: None
# 当运行插件错误时会进行运行该函数


__underlying__ = bool


# 参数名称: 底层插件
# 是否必须: 否
# 加入版本: 0.3.15
# 类型: bool
# 默认值: False
# 描述:
# 用于指定插件是否为底层插件
# 允许插件修改 fileMapping 的类 & 方法
# __function__(main) 需要一定格式(dict), 不然无法更改


def main(**kwargs):
    """
    这里由函数制定义, 例如:
    def main(app): ...
    当fileMapping.run()调用时, 会自动调用main()函数, 并传入app参数

    :param kwargs: 运行参数
    :return: 可以返回任何参数
    """
    # 这里可以定义插件的主要功能代码


def end(**kwargs):
    """
    这里由函数制定义, 例如:
    def end(app): ...
    当fileMapping.run()调用时, 会自动调用end()函数, 并传入app参数

    :param kwargs: 运行参数
    :return: None
    """


"""
以下部分为 fileMapping 包的解释
可以进行注册等函数解释
fileMapping.File 类

"""


class File:
    callObject: dict
    invoke: dict
    returnValue: dict
    public: dict
    # 可以通过 . 访问属性, 已经重写 __getattr__ 方法
    """
    callObject: 对插件进行调用时会保存在这个字典里面
    invoke: 内行参数 用于调用插件内的参数
    returnValue: 返回参数 __function__ 运行的结果
    public: 公共参数 用于调用插件的公共参数
        config: 配置参数 这个是由fileMapping在File执行中添加
            - kwargs 运行参数
    """


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


class Plugin:
    def get(self, pluginName: str, objectName: str, *args) -> object | tuple[object]:
        """
        - 获取插件的对象

        :param pluginName: 插件名称
        :param objectName: 对象名称
        :param args: 多个 objectionName 参数
        """


def temporaryFolders(path: str = None, *args) -> str:
    """
    返回申请的临时文件夹路径

    :param path: 插件申请的临时文件路径
        - 会验证该路径
        - None: 直接返回临时文件路径

    :param args:
        - 做拼接, 不会验证路径的真实性
    """


def fileOperations(path: str, mode: str, *args, **kwargs) -> _io.open:
    """
    本质上在操作文件中加了一个中间层

    - 用于对文件进行操作
    """


def getAppRegister(name: str) -> object:
    """
    返回一个插件的 register 实例
    :param app: 插件 注册在名称
    """
