
from mag_tools.model.base_enum import BaseEnum


class WellControlType(BaseEnum):
    """
    井控类型枚举
    枚举值为井控类型的名称，如：WellControlType.BHP
    """
    BHP = (0, '定井底压力')  # 定井底压力
    THP = (1, '定井口压力')  # 定井口压力
    WRAT = (2, '定水产量')  # 定水产量
    GRAT = (3, '定气产量')  # 定气产量
    ORAT = (4, '定油产量')  # 定油产量
    LRAT = (5, '定总液量')  # 定总液量
    WIR = (6, '定流量注水')  # 定流量注水
    GIR = (7, '定流量注气')  # 定流量注气
    WIBHP = (8, '定 BHP 注水')  # 定 BHP 注水
    GIBHP = (9, '定 BHP 注气')  # 定 BHP 注气
    WITHP = (10, '定 THP 注水')  # 定 THP 注水
    GITHP = (11, '定 THP 注气')  # 定 THP 注气
    STOP = (12, '井口停产(射孔保持开启)')  # 井口停产(射孔保持开启)
    SHUT = (13, '关井(射孔也关闭)')  # 关井(射孔也关闭)

    def is_product(self):
        """
        判断是否为生产控制类型
        :return: 如果是生产控制类型，返回 True，否则返回 False
        """
        return self in {WellControlType.BHP, WellControlType.THP, WellControlType.WRAT, WellControlType.GRAT, WellControlType.ORAT, WellControlType.LRAT}

    def is_input(self):
        """
        判断是否为注入控制类型
        :return: 如果是注入控制类型，返回 True，否则返回 False
        """
        return self in {WellControlType.WIR, WellControlType.GIR, WellControlType.WIBHP, WellControlType.GIBHP, WellControlType.WITHP, WellControlType.GITHP}

if __name__ == '__main__':
    # 示例用法
    print(WellControlType.BHP.code)  # 输出: (0, '定井底压力')
    print(WellControlType.BHP.desc)  # 输出: BHP
    print(WellControlType.BHP.is_product())  # 输出: True
    print(WellControlType.WIR.is_input())  # 输出: True
