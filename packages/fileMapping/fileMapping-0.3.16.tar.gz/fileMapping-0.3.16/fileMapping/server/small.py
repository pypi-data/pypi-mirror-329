import hashlib
import json
import os
import sys
import zipfile


class MyStream:
    def write(self, text):
        pass

    def flush(self):
        pass

    def close(self):
        pass


def pull_DNS_TXT(domain: str) -> str:
    """
    解析域名的TXT记录
    需要 dns 库

    :param domain: 域名
    :return: TXT记录
    """
    try:
        import dns.resolver

        # 解析域名的 TXT 记录
        answer = dns.resolver.resolve(domain, 'TXT').rrset.items
        for key, _ in answer.items():
            answer = json.loads(str(key).strip('"').replace("'", '"'))

        return answer

    except Exception as e:
        return e


def pip_install(package_name: str, pip_accelerationSource=None, pip_install_print: bool = False) -> bool:
    """
    安装依赖包
    :param package_name: 依赖包名称
    :return:
    """
    try:
        from pip._internal.cli import main as pip
        import importlib
        # pip.main 方法可能在以后的版本中被移除
        # https://github.com/pypa/pip/issues/7498

        # 先使用 pip.main 的 api 进行安装
        # 更好的方法是使用 os.system 调用 pip 命令
        # 但是在打包成 exe 后, os.system 调用 可能没有 path 环境变量 pip
        # 也无法在 exe 内部安装依赖包

    except ImportError as e:
        # 无法导入依赖包
        return e

    if not pip_install_print:
        stdout = sys.stdout
        sys.stdout = MyStream()

    try:
        # 尝试安装依赖包
        if not pip_accelerationSource in ["", None, ' ', False]:
            pip.main(['install', package_name, "-i"] + pip_accelerationSource.strip().split(" "))
            # 加速源

        else:
            pip.main(['install', package_name])

        if not pip_install_print:
            sys.stdout = stdout

        importlib.import_module(package_name)
        return True

    except Exception as e:
        if not pip_install_print:
            sys.stdout = stdout

        # 无法安装依赖包 & 导入依赖包
        return e


class folderCompression:
    def __init__(self, path, ):
        """
        初始化文件夹压缩类。
        :param path: 要压缩的文件夹路径 或 zip文件路径
        """
        self.path = path

    def compress_folder(self, zip_file_name: str = None, zip_file_path: str = None, zip_blacklist: list = None):
        """
        此函数压缩给定的文件夹并返回压缩文件的名称。

        :param zip_file_name: 压缩文件名称，默认为None。
        :param zip_file_path: 压缩文件路径，默认为None。
        :param zip_blacklist: 压缩文件黑名单，默认为None。
        """
        zip_file_name = zip_file_name + ".zip" if (not zip_file_name is None) and (
            not zip_file_name.endswith(".zip")) else zip_file_name
        zip_file_path = zip_file_path
        zip_blacklist = zip_blacklist if not zip_blacklist is None else []

        try:
            # 创建一个压缩文件
            if (not zip_file_name is None) and (not zip_file_path is None):
                path = os.path.join(zip_file_path, zip_file_name)
            else:
                path = self.path if self.path.endswith(".zip") else f"{self.path}.zip"

            with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for root, dirs, files in os.walk(self.path):
                    for file in files:
                        full_path = os.path.join(root, file)
                        if not any(black_item in full_path for black_item in zip_blacklist):
                            zip_file.write(full_path)

            # 所有文件添加完成后返回压缩文件的名称
            return path
        except Exception as e:
            return e

    def decompress_folder(self, path: str = None):
        """
        此函数解压缩给定的压缩文件并返回解压缩文件夹的名称。
        """
        if not os.path.exists(self.path):
            return None

        try:
            # 解压文件到指定目录
            with zipfile.ZipFile(self.path, "r") as zip_file:
                zip_file.extractall(path)
                # 解压完成后返回解压后的文件夹名称
            return self.path

        except Exception as e:
            return e


def file_md5(file_path: str) -> FileNotFoundError | str | Exception:
    """
    此函数计算给定文件的 MD5 值。
    :param file_path: 文件路径。
    :return: 文件的 MD5 值。
    """
    try:
        md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()

    except FileNotFoundError as e:
        return e

    except Exception as e:
        return e
