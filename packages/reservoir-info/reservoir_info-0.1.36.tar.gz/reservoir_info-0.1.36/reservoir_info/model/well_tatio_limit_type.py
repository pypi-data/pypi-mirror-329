
from mag_tools.model.base_enum import BaseEnum


class WellRatioLimitType(BaseEnum):
    """
    井比率限制类型枚举
    枚举值为井比率限制类型的名称，如：WellRatioLimitType.WCUT
    """
    WCUT = ('含水率', '含水率')  # 含水率
    GOR = ('气-油比', '气-油比')  # 气-油比
    GLR = ('气-液比', '气-液比')  # 气-液比
    WGR = ('水-气比', '水-气比')  # 水-气比

if __name__ == '__main__':
    # 示例用法
    print(WellRatioLimitType.WCUT.code)  # 输出: ('含水率', '含水率')
    print(WellRatioLimitType.GOR.code)  # 输出: ('气-油比', '气-油比')
    print(WellRatioLimitType.GLR.code)  # 输出: ('气-液比', '气-液比')
    print(WellRatioLimitType.WGR.code)  # 输出: ('水-气比', '水-气比')
