
from mag_tools.model.base_enum import BaseEnum


class UnitType(BaseEnum):
    """
    单位类型枚举
    枚举值为单位类型的名称，如：UnitType.LENGTH
    """
    LENGTH = ('Length', '长度')  # 长度
    SURFACE_VOLUME_LIQ = ('Surface Volume of Liquid', '地表液体体积')  # 地表液体体积
    SURFACE_VOLUME_GAS = ('Surface Volume of Gas', '地表气体体积')  # 地表气体体积
    SUBSURFACE_VOLUME = ('Subsurface Volume', '地下体积')  # 地下体积
    DENSITY = ('Density', '密度')  # 密度
    PRESSURE = ('Pressure', '压力')  # 压力
    TIME = ('Time', '时间')  # 时间
    ABS_TEMPERATURE = ('Absolute temperature', '绝对温度')  # 绝对温度
    REL_TEMPERATURE = ('Relative temperature', '相对温度')  # 相对温度
    WI = ('Well Index (WI)', '井指数')  # 井指数
    TF = ('Transmissivity Factor', '井/网格传导率系数')  # 井/网格传导率系数
    PERMEABILITY = ('permeability', '渗透率')  # 渗透率
    VISCOSITY = ('viscosity', '粘度')  # 粘度
    SURFACE_TENSION = ('surface tension', '表面张力')  # 表面张力
    FORCHHEIMER_BETA = ('Coefficients of Forchheimer', 'Forchheimer 公式的系数')  # Forchheimer 公式的系数

if __name__ == '__main__':
    # 示例用法
    print(UnitType.LENGTH.code)  # 输出: ('Length', '长度')
    print(UnitType.SURFACE_VOLUME_LIQ.code)  # 输出: ('Surface Volume of Liquid', '地表液体体积')
    print(UnitType.PERMEABILITY.code)  # 输出: ('permeability', '渗透率')
