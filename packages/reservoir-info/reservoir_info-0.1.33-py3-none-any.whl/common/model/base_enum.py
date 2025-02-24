from enum import Enum
from typing import Optional, Union


class BaseEnum(Enum):
    def __init__(self, code: Optional[Union[str or int]] = None, desc: Optional[str] = None):
        self.code = code
        self.desc = desc

    @classmethod
    def get_by_code(cls, code: Optional[Union[str or int]]):
        """
        根据代码获取枚举
        :param code: 代码
        :return: 枚举
        """
        for _enum in cls:
            if _enum.code == code:
                return _enum
        return None

    @classmethod
    def get_by_desc(cls, desc: str):
        for _enum in cls:
            if _enum.desc == desc:
                return _enum
        return None
