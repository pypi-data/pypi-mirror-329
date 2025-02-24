from . import config
from . import fileMappingConfig


class fileMapping_dict(dict):
    # 用于包装字典
    # 可以通过 . 访问属性
    def __getattr__(self, item):
        if item in self:
            return self.get(item)

        else:
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{item}'")



Application = fileMapping_dict({})

callObject = fileMapping_dict({})
invoke = fileMapping_dict({})
returnValue = fileMapping_dict({})
public = fileMapping_dict({})
information = fileMapping_dict({"appRegister": {}, "readRegistration": {}})
logs = fileMapping_dict({"run": 1, "parameterApplication": {"error": []}})

