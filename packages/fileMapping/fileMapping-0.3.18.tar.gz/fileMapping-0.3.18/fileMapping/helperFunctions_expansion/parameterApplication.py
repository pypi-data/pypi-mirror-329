"""
参数的具体应用
fileMappingConfig.functions


"""
import shutil
import functools
import os

from . import empty


l = []


def ApplyParameter(self_info) -> list:
    """
    应用参数

    规定如下
    类, 初始化时必须包含self_info参数
    可以有 init 和 end 方法, 用于初始化和结束
    """
    end_list = []

    for i in l:
        func = i(self_info)
        try:
            func.init()
        except Exception as e:
            self_info.logs['parameterApplication']['error'].append({func: e})

        if hasattr(func, 'end'):
            end_list.append(func.end)

    return end_list


def wrapper(func):
    @functools.wraps(func)
    def wrapper_func(*args, **kwargs):
        return func(*args, **kwargs)

    l.append(wrapper_func)
    return wrapper_func


@wrapper
class framework:
    def __init__(self, self_info: dict):
        self.self_info = self_info

    def init(self):
        pass

    def end(self):
        pass


@wrapper
class TemporaryFolders:
    def __init__(self, self_info: dict):
        self.self_info = self_info
        self.temporaryFolders = True
        if not self_info.path in [False, True, None, '']:  # temporaryFolders 关闭
            self.path = os.path.join(self_info.path, self_info.public.config['temporaryFolders'])

            self.information_temporaryFolders = self.self_info.information["temporaryFolders"] = {}   # 临时文件夹信息
            self.logs = self.self_info.logs["temporaryFolders"] = {"error": []}
            self.create_path = []
            self.init_tmp = False
            # 用于判断临时的文件夹是否自主创建，如果是的话则在结束时删除
            if not os.path.exists(self.path):
                os.mkdir(self.path)
                self.init_tmp = True

        else:
            self.temporaryFolders = False

    def __mkdir(self, temporaryFolders):
        path = os.path.join(self.path, temporaryFolders)
        try:
            if not os.path.exists(path):
                os.mkdir(path)
                self.create_path.append(path)

            self.information_temporaryFolders[temporaryFolders] = path
            return True

        except FileExistsError as e:
            self.logs["error"].append({path: e})
            return False

    def init(self):
        if not self.temporaryFolders:
            return False

        for key, value in self.self_info.information.file_info.items():
            temporaryFolders = value['__temporaryFolders__']
            if temporaryFolders is None:
                continue

            if isinstance(temporaryFolders, str):
                self.__mkdir(temporaryFolders)

            else:  # temporaryFolders is a list
                for folder in temporaryFolders:
                    self.__mkdir(folder)

    def end(self):
        for i in self.create_path:
            shutil.rmtree(i)

        if self.init_tmp:
            shutil.rmtree(self.path)


@wrapper
class function:
    def __init__(self, self_info: dict):
        self.self_info = self_info

    def __empty__(self, key):
        self.self_info.callObject[key].pointer = empty.empty().run
        # pointer = empty.empty()
        #
        # return pointer


    def init(self):
        for key, value in self.self_info.information.file_info.items():
            # print(key, value['__function__'])
            if value['__function__'] in [None, '']:
                # self.self_info.callObject[key].pointer = empty.empty()
                # print("[012]>? ", key, value['__function__'])
                self.__empty__(key)
                # self.__empty__(self.self_info.callObject[key].pointer)

            else:
                try:
                    self.self_info.callObject[key].pointer = getattr(self.self_info.callObject[key].pack, value['__function__'])

                except AttributeError as e:
                    self.__empty__(key)
                    # self.__empty__(self.self_info.callObject[key].pointer)

@wrapper
class run:
    def __init__(self, self_info: dict):
        self.self_info = self_info


    def init(self):
        for key, value in self.self_info.information.file_info.items():
            # print(key, value['__run__'])
            if value['__run__'] is False:
                self.self_info.callObject[key].pointer = empty.empty().run

@wrapper
class readRegistration:
    def __init__(self, self_info: dict):
        """
        register.threadRegistration

        :param self_info:
        """
        self.self_info = self_info
        self.info = self_info.information["readRegistration"]
        self.logs = self_info.logs["readRegistration"] = {"error": []}

    def init(self):
        func_list = {}
        for key, value in self.info.items():
            level = value['level']
            if level not in func_list:
                func_list[level] = []

            func_list[level].append(key)

        func_list = sorted(func_list.items(), key=lambda x: x[0])
        for level, func_list in func_list:
            for func in func_list:
                try:
                    func(**self.info[func]['kwargs'])

                except Exception as e:
                    self.self_info.logs['readRegistration']['error'].append({func: e})


