from mag_tools.model.base_enum import BaseEnum

class ModuleType(BaseEnum):
    """
    模块类型枚举
    枚举值为不包含前缀的模块类型名，如：ModuleType.GASWATER
    """
    GASWATER = ('GasWater', '气-水两相模型')  # 气-水两相模型
    OILWATER = ('OilWater', '油-水两相模型')  # 油-水两相模型
    BLACKOIL = ('BlackOil', '黑油模型')  # 黑油模型
    COMP = ('Comp', '组分模型')  # 组分模型

if __name__ == '__main__':
    # 示例用法
    print(ModuleType.GASWATER.code)  # 输出: GasWater
    print(ModuleType.GASWATER.desc)  # 输出: 气-水两相模型
    print(ModuleType.get_by_desc("油-水两相模型"))  # 输出: 油-水两相模型
