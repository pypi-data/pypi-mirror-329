from typing import Optional, Union

from mag_tools.model.base_enum import BaseEnum

class ModuleType(BaseEnum):
    """
    模块类型枚举
    枚举值为不包含前缀的模块类型名，如：ModuleType.GASWATER
    """
    GASWATER = ('GasWater', '气-水两相模型', 'GW')  # 气-水两相模型
    OILWATER = ('OilWater', '油-水两相模型', 'OW')  # 油-水两相模型
    BLACKOIL = ('BlackOil', '黑油模型', 'BLK')  # 黑油模型
    COMP = ('Comp', '组分模型', 'Comp')  # 组分模型

    def __init__(self, code: Union[str or int], desc: str, alias: str):
        super().__init__(code, desc)
        self.alias = alias