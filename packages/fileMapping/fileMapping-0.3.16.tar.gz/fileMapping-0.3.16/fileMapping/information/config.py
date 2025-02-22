"""
这是一个 config 文件，用于配置一些全局变量

可以在这里配置一些全局变量
在运行 fileMapping.File 文件时, 会自动读取 config.py 中的变量, 写入 File.public["config"] 字典中

同时在 fileMapping.File 有一个 config 参数, 可以传入字典, 用于覆盖 config.py 中的变量
"""
"""
一般来说是由用户自定义的变量
这里的用户, 不是指开发者, 而是指使用者, 也就是最终用户
"""

# 以下是一些 fileMapping 的变量
multithreading: bool = True
# 是否开启多线程
numberOfThreads: int = 4
# 线程数 - 合理的线程数 4 - 6
tick: int = 2
# 每秒运行多少次
# 合理的 tick 值 2 - 5

temporaryFolders: str = "temp"
# 临时文件夹的名称
dataFolder: str = "file_DATA"
# 数据文件夹的名称

logFolder: str = "log"
# 日志文件夹的名称
logFile: str = "fileMapping.json"
# 日志文件的名称
