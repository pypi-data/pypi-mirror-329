
from mag_tools.model.base_enum import BaseEnum


class UnitConvertFactor(BaseEnum):
    """
    单位转换因子枚举
    枚举值为单位转换因子的名称，如：UnitConvertFactor.DARCY
    """
    DARCY = ('Darcy', '达西')  # 达西
    GRAVITY = ('Gravity', '重力')  # 重力
    FORCHHEIMER = ('Forchheimer quadratic term', 'Forchheimer 二次项')  # Forchheimer 二次项
    IDEAL_GAS_CONSTANT = ('Ideal gas constant', '理想气体常数')  # 理想气体常数

if __name__ == '__main__':
    # 示例用法
    print(UnitConvertFactor.DARCY.code)  # 输出: ('Darcy', '达西')
    print(UnitConvertFactor.GRAVITY.code)  # 输出: ('Gravity', '重力')
    print(UnitConvertFactor.FORCHHEIMER.code)  # 输出: ('Forchheimer quadratic term', 'Forchheimer 二次项')
    print(UnitConvertFactor.IDEAL_GAS_CONSTANT.code)  # 输出: ('Ideal gas constant', '理想气体常数')
