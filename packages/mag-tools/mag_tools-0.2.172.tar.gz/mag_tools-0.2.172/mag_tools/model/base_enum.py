from enum import Enum
from typing import Optional, Union


class BaseEnum(Enum):
    def __init__(self, code: Union[str or int], desc: Optional[str] = None):
        self._code = code
        self._desc = desc

    @classmethod
    def of_code(cls, code: Optional[Union[str or int]]):
        """
        根据代码获取枚举
        :param code: 代码
        :return: 枚举
        """
        if code is not None:
            for _enum in cls:
                if str(_enum.code).upper() == str(code).upper():
                    return _enum
        return None

    @classmethod
    def of_desc(cls, desc: str):
        for _enum in cls:
            if _enum.desc == desc:
                return _enum
        return None

    @property
    def code(self):
        return self._code

    @property
    def desc(self):
        return self._desc

    def __str__(self):
        return f"{self.name}[code={self.code}, desc={self.desc}]"
