
from mag_tools.model.base_enum import BaseEnum

class ModelType(BaseEnum):
    """
    模块类型枚举
    枚举值为不包含前缀的模块类型名，如：ModelType.GASWATER
    """
    GASWATER = ('GasWater', '气-水两相模型')  # 气-水两相模型
    OILWATER = ('OilWater', '油-水两相模型')  # 油-水两相模型
    BLACKOIL = ('BlackOil', '黑油模型',)  # 黑油模型
    COMP = ('Comp', '组分模型')  # 组分模型