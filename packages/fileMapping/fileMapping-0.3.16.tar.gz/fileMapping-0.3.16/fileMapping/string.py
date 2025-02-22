from .information import fileMappingConfig as cg
import sys


def printlog(log: str, printPosition: sys.stdout = sys.stdout, color: str = '32', printLog: bool = True):
    """
    打印日志
    :param log: 日志
    :param printPosition: 打印位置
    :param color: 颜色 31红色 32绿色 33黄色 34蓝色 35紫色 36青色 37白色
    :return:
    """
    if printLog is True:
        print(f"\033[1;{color}m{log}\033[0m", file=printPosition)
        return True

    else:
        return True



def endFailed(s1, s2):
    return printlog(**{
        "log": f"插件结束失败: {s1} 文件\n\tlog: {s2}",
        "printPosition":cg.log["printPosition"],
        "color": "31",
        "printLog": cg.log["printLog"]
    })


def endfunctionNotFound(s1, s2):
    return printlog(**{
        "log": f"插件结束失败: {s1} 文件\n\tlog: 找不到结束函数 '{s2}'",
        "printPosition":cg.log["printPosition"],
        "color": "31",
        "printLog": cg.log["printLog"]
    })


def errorNoFile(s1):
    return printlog(**{
        "log": f"运行文件错误: 没有 {s1} 文件",
        "printPosition":cg.log["printPosition"],
        "color": "31",
        "printLog": cg.log["printLog"]
    })

def theRunFileWasSuccessful(s1):
    return printlog(**{
        "log": f"运行文件成功: {s1} 文件",
        "printPosition":cg.log["printPosition"],
        "color": "32",
        "printLog": cg.log["printLog"]
    })

def theRunFileFailed(s1, s2):
    return printlog(**{
        "log": f"[00]运行文件失败: {s1} 文件\n\tlog: {s2}",
        "printPosition":cg.log["printPosition"],
        "color": "31",
        "printLog": cg.log["printLog"]
    })

def thereIsNoMainFunction(s1):
    return printlog(**{
        "log": f"运行文件失败: {s1} 文件\n\tlog: 没有 main 函数",
        "printPosition":cg.log["printPosition"],
        "color": "31",
        "printLog": cg.log["printLog"]
    })

def importError(s1, s2):
    return printlog(**{
        "log": f"file: {s1}\n导入错误 log: {s2}",
        "printPosition":cg.log["printPosition"],
        "color": "31",
        "printLog": cg.log["printLog"]
    })


