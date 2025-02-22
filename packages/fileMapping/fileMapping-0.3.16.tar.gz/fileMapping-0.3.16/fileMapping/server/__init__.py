import os
import traceback


try:
    from . import small
except ImportError:
    import small


dependence = [
    "dnspython",
    "requests"
    # 第三方依赖包
]

try:
    import dns
    import requests

    dependence = True
except ImportError as e:
    pass



class Pull_plugin:
    def __init__(self, path: os.path, plugin_name: str,
                 pull_url: str="txt.fileMapping.78ya.top",
                 pullValidation: bool=False,
                 MD5_value_validation: bool=False,
                 SH1_value_validation: bool=False,
                 encryption: bool=False,
                 pip_install: bool=False,
                 pip_accelerationSource: str="https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple some-package",
                 pip_install_print: bool=False,
                 logs: bool=True,
                 ):
        """
        拉取插件
        该插件用于拉取插件，并验证插件的完整性、完整性、完整性。

        步骤如下:
        1. 验证依赖包是否存在
        2. 验证 path 是否存在
        3. 请求 DNS服务器(TXT记录) 拉取服务端配置信息
        4. 下载插件
        5. 验证插件

        pull_url: 拉取地址
        是一个域名, 插件将从该域名拉取插件。
        :param path: 保存插件的路径
        :param plugin_name: 插件
        :param pull_url: 拉取地址
        :param pullValidation: 是否需要拉取验证
        :param MD5_value_validation: 是否需要MD5值验证
        :param SH1_value_validation: 是否需要SH1值验证
        :param encryption: 是否需要加密
        :param pip_install: 是否需要自动安装依赖包
        :param pip_accelerationSource: pip加速源
        :param logs: 是否需要记录日志
        """
        self.path = path
        self.plugin_name = plugin_name
        self.pull_url = pull_url
        self.pullValidation = pullValidation
        self.MD5_value_validation = MD5_value_validation
        self.SH1_value_validation = SH1_value_validation
        self.encryption = encryption
        self.pip_install = pip_install
        self.pip_accelerationSource = pip_accelerationSource
        self.pip_install_print = pip_install_print
        # logs -> 记录数据
        self.logs = {}

        self.logs[1] = {}
        environment = True
        if (isinstance(dependence, list)) and self.pip_install:
            # 验证依赖包是否存在
            # 自动安装依赖包
            self.logs[1]["pip_install"] = True
            for min_package in dependence:
                if not small.pip_install(min_package, pip_accelerationSource, pip_install_print):
                    # 无法安装依赖包
                    environment = False
                    self.logs[1]["data"] = {"environment": environment, "min_package": min_package,
                        "pip_accelerationSource": pip_accelerationSource, "pip_install_print": pip_install_print}
                    break

        elif isinstance(dependence, list):
            # 依赖包不存在
            environment = False
            self.logs[1]["pip_install"] = False
            self.logs[1]["data"] = {"environment": environment, "min_package": dependence}

        self.logs[2] = {}
        if not os.path.exists(self.path):
            # 验证 path 是否存在
            environment = False
            self.logs[2]["data"] = {"environment": environment, "path": self.path}

        self.logs["environment"] = environment
        if environment:
            # 环境满足
            # 验证插件是否存在
            self.logs[3] = {}
            txt_value = small.pull_DNS_TXT(self.pull_url)
            if not isinstance(txt_value, dict):
                # 解析失败
                self.logs[3]["data"] = {"environment": environment, "pull_url": self.pull_url, "txt_value": txt_value}

            else:
                url = txt_value.get("url")
                ip = txt_value.get("ip")
                agreement = txt_value.get("agreement")
                if url != None and ip != None and agreement != None:
                    self.__pull_plugin(url, ip, agreement)

                else:
                    # 解析失败
                    self.logs[3]["dict"] = "url, ip, agreement| iDonTCorrespond"
                    self.logs[3]["data"] = {"environment": environment, "pull_url": self.pull_url,
                        "txt_value": txt_value, "url": url, "ip": ip, "agreement": agreement}

        if not logs:
            # 清除 logs 日志
            self.logs = None

    def __pull_plugin(self, url, ip, agreement) -> bool|Exception:
        """
        拉取插件
        requests

        步骤如下:
        1. 向服务端获取下载url
        2. 下载插件
        3. 验证插件完整性
        4. 解压zip文件

        :param url: 插件下载 url
        :param ip: 插件下载地址的 IP 地址
        :param agreement: 协议 https | http
        :return:
        """
        import requests


        ip = "192.168.10.104:5000"
        try:
            self.logs[4] = {1: True}
            url = f"{agreement}://{ip}{url}/pull"
            data = requests.post(url, json={"name": self.plugin_name}, timeout=10)
            if data.status_code != 200:
                self.logs[4]["pull_url"] = False
                self.logs[4]["data"] = {"url": url, "plugin_name": self.plugin_name, "return_data": data.text, "code": data.status_code}
                return False

            data = data.json()
            url = data.get("url", False)
            server_md5 = data.get("file_attribute", {}).get("md5", False)
            file_name = data.get("zip_file_name", False)
            if not ((isinstance(url, str)) and (isinstance(server_md5, str)) and (isinstance(file_name, str))):
                # 极大有可能为服务端失败
                self.logs[4]["url_check"] = False
                self.logs[4]["data"] = {"data": data, "url": url, "server_md5": server_md5, "file_name": file_name}

                return False

            self.logs[4][2] = True
            url = f"{agreement}://{ip}{url}"
            data = requests.post(url, timeout=10)
            if data.status_code != 200:
                # 下载失败
                self.logs[4]["download_url"] = False
                self.logs[4]["data"] = {"url": url, "return_data": data.text, "code": data.status_code}
                return False

            file_path = os.path.join(self.path, file_name)
            with open(file_path, "wb") as f:
                f.write(data.content)

            self.logs[4][3] = True
            md5 = small.file_md5(file_path)
            if not isinstance(md5, str):
                # MD5值无法获取
                self.logs[4]["md5_check"] = None
                self.logs[4]["data"] = {"file_path": file_path, "md5": md5}
                return False

            if md5 != server_md5:
                # MD5值验证失败
                self.logs[4]["md5_check"] = False
                self.logs[4]["data"] = {"file_path": file_path, "md5": md5, "server_md5": server_md5}
                os.remove(file_path)  # 删除文件
                return False

            # 解压zip文件 & 删除文件
            self.logs[4][4] = True
            unzip_path = os.path.join(self.path, self.plugin_name)
            os.mkdir(unzip_path)
            zip_data = small.folderCompression(file_path).decompress_folder(unzip_path)
            os.remove(file_path)
            if not isinstance(zip_data, str):
                # 解压失败
                self.logs[4]["unzip_check"] = False
                self.logs[4]["data"] = {"file_path": file_path, "zip_data": zip_data}
                return False

            return True

        except Exception as e:
            self.logs[4][e.__class__.__name__] = False
            self.logs[4]["data"] = {"error": e, "data": locals(), "traceback_error": traceback.format_exc()}

            return e


class Upload_plugin:
    def __init__(self, path: os.path, plugin_name: str,
                 plugin_version: str,
                 upload_url: str="txt.fileMapping.78ya.top",
                 pip_install: bool=False,
                 pip_accelerationSource: str="https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple some-package",
                 logs: bool=True,
                 ):
        """
        上传插件
        该插件用于上传插件，并验证插件的完整性、完整性、完整性。

        步骤如下:
        1. 验证依赖包是否存在
        2. 验证 path 是否存在
        3. 压缩插件
        4. 上传插件

        upload_url: 上传地址
        是一个域名, 插件将上传到该域名
        :param path: 保存插件的路径
        :param plugin_name: 插件
        :param plugin_version: 插件版本
        :param upload_url: 上传地址
        :param pip_install: 是否需要自动安装依赖包
        :param pip_accelerationSource: pip加速源
        :param logs: 是否需要记录日志
        """
        self.path = path
        self.plugin_name = plugin_name
        self.plugin_version = plugin_version
        self.upload_url = upload_url
        self.pip_install = pip_install
        self.pip_accelerationSource = pip_accelerationSource
        # logs -> 记录数据
        self.logs = {}

        self.logs[1] = {}
        environment = True
        if (isinstance(dependence, list)) and self.pip_install:
            # 验证依赖包是否存在
            # 自动安装依赖包
            self.logs[1]["pip_install"] = True
            for min_package in dependence:
                if not small.pip_install(min_package, pip_accelerationSource):
                    # 无法安装依赖包
                    environment = False
                    self.logs[1]["data"] = {"environment": environment, "min_package": min_package,
                        "pip_accelerationSource": pip_accelerationSource}
                    break

        elif isinstance(dependence, list):
            # 依赖包不存在
            environment = False
            self.logs[1]["pip_install"] = False
            self.logs[1]["data"] = {"environment": environment, "min_package": dependence}

        self.logs[2] = {}
        if not os.path.exists(self.path):
            # 验证 path 是否存在
            environment = False
            self.logs[2]["path"] = False
            self.logs[2]["data"] = {"environment": environment, "path": self.path}

        self.logs[3] = {}
        self.logs["environment"] = environment
        if environment:
            # 环境满足
            # 压缩插件
            zip_file_name = f"{self.plugin_name}_{self.plugin_version}.zip"
            zip_file_path = ''
            zip_data = small.folderCompression(self.path).compress_folder(zip_file_name, zip_file_path)
            if not isinstance(zip_data, str):
                # 压缩失败
                self.logs[3]["zip_check"] = False
                self.logs[3]["data"] = {"environment": environment, "zip_file_path": zip_file_path, "zip_data": zip_data}

            # 上报插件
            self.logs[4] = {}
            self.reports = self.__upload_plugin(zip_file_name)

        if not logs:
            # 清除 logs 日志
            self.logs = None

    def __upload_plugin(self, file_path) -> dict| bool| Exception:
        """
        上传插件
        requests

        步骤如下:
        1.请求 DNS服务器(TXT记录) 拉取服务端配置信息
        2.打开文件
        3.上传插件

        :param file_path: 压缩文件路径
        :return:
        """
        import requests


        try:
            self.logs[5] = {1: True}
            txt_value = small.pull_DNS_TXT(self.upload_url)
            if not isinstance(txt_value, dict):
                # 解析失败
                self.logs[5]["pull_url"] = False
                self.logs[5]["data"] = {"upload_url": self.upload_url, "txt_value": txt_value}
                return False

            ip = txt_value.get("ip", False)
            agreement = txt_value.get("agreement", False)
            url = txt_value.get("url", False)
            ip = "192.168.10.104:5000"
            if not ((isinstance(ip, str)) and (isinstance(agreement, str)) and (isinstance(url, str))):
                # 极大有可能为服务端失败
                self.logs[5]["url_check"] = False
                self.logs[5]["data"] = {"txt_value": txt_value, "ip": ip, "agreement": agreement, "url": url}
                return False

            self.logs[5][2] = True
            url = f"{agreement}://{ip}{url}/upload"
            with open(file_path, 'rb') as file:
                files = {'file': file}
                self.logs[5][3] = True
                data = requests.post(url, files=files,
                                     data={'version': self.plugin_version, "file_name": self.plugin_name})

                if data.status_code == 410:
                    # 文件已存在
                    self.logs[5]["upload_url"] = "文件已存在"
                    self.logs[5]["data"] = {"url": url, "file_path": file_path, "return_data": data.text, "code": data.status_code}
                    return False

                elif data.status_code != 200:
                    self.logs[5]["upload_url"] = False
                    self.logs[5]["data"] = {"url": url, "file_path": file_path, "return_data": data.text,
                                            "code": data.status_code}
                    return False

                data = data.json()
                if not isinstance(data, dict):
                    # 极大有可能为服务端失败
                    self.logs[5]["upload_check"] = False
                    self.logs[5]["data"] = {"data": data}
                    return False

                return data

        except Exception as e:
            self.logs[5][e.__class__.__name__] = False
            self.logs[5]["data"] = {"error": e, "data": locals(), "traceback_error": traceback.format_exc()}

            return e

