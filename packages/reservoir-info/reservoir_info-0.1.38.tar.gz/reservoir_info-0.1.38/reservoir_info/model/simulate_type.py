
from mag_tools.model.base_enum import BaseEnum

class SimulateType(BaseEnum):
    """
    模型模拟方式枚举
    """
    BLK = ('BLK', '黑油模拟')  # 黑油模型
    COMP = ('Comp', '组分模拟')  # 组分模型
    FRAC = ('Frac', '裂缝模拟')  # 黑油模型