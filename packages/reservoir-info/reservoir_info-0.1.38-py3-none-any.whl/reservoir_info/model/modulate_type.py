from typing import Optional, Union

from mag_tools.model.base_enum import BaseEnum

class ModelType(BaseEnum):
    """
    模型模拟方式枚举
    """
    BLACKOIL = ('BLK', '黑油模型')  # 黑油模型
    COMP = ('Comp', '组分模型')  # 组分模型
    FRAC = ('Frac', '裂缝模型')  # 黑油模型