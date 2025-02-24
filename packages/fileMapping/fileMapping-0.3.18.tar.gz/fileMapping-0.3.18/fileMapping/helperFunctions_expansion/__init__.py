import sys

from . import informationProcessing
from . import helperFunctions
from . import empty
from . import parameterApplication


if sys.version_info.major == 3 and sys.version_info.minor >= 3:
    # 多线程处理使用了 concurrent.futures 模块
    # concurrent.futures 模块在 python 3.2 之前版本中并没有加入到标准库中
    from . import multithreading

else:
    from . import multithreading_v32 as multithreading
