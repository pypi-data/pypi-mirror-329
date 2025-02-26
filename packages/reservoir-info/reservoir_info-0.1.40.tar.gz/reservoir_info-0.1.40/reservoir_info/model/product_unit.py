
from mag_tools.model.base_enum import BaseEnum


class ProductUnit(BaseEnum):
    """
    产品单位枚举
    枚举值为产品的单位，如：ProductUnit.REPORT_TIME
    """
    REPORT_TIME = ('YYYY-MM-DD HH:MM', '报告时间')  # 报告时间
    WORK_TIME = ('DAYS', '工作时间')  # 工作时间
    WATER_PRODUCT_RATE = ('STB/DAY', '水产量速率')  # 水产量速率
    GAS_PRODUCT_RATE = ('Mscf/DAY', '气产量速率')  # 气产量速率
    OIL_PRODUCT_RATE = ('STB/DAY', '油产量速率')  # 油产量速率
    WATER_INJECT_RATE = ('STB/DAY', '水注入速率')  # 水注入速率
    GAS_INJECT_RATE = ('Mscf/DAY', '气注入速率')  # 气注入速率
    WATER_PRODUCT_TOTAL = ('STB', '水总产量')  # 水总产量
    GAS_PRODUCT_TOTAL = ('Mscf', '气总产量')  # 气总产量
    OIL_PRODUCT_TOTAL = ('STB', '油总产量')  # 油总产量
    WATER_INJECT_TOTAL = ('STB', '水总注入量')  # 水总注入量
    GAS_INJECT_TOTAL = ('Mscf', '气总注入量')  # 气总注入量
    BOTTOM_HOLE_PRESSURE = ('PSIA', '底孔压力')  # 底孔压力
    TUBING_HEAD_PRESSURE = ('PSIA', '管头压力')  # 管头压力
    LIQUID_PRODUCT_RATE = ('STB/DAY', '液体产量速率')  # 液体产量速率
    LIQUID_PRODUCT_TOTAL = ('STB', '液体总产量')  # 液体总产量
    WATER_CUT = ('STB/STB', '含水率')  # 含水率
    WATER_GAS_RATIO = ('STB/Mscf', '水气比')  # 水气比
    GAS_OIL_RATIO = ('Mscf/STB', '气油比')  # 气油比
    INCREASE_TIME = ('DAY', '增加时间')  # 增加时间
    MOLAR_FLOW_RATE = ('mol/s', '摩尔流速')  # 摩尔流速

if __name__ == '__main__':
    # 示例用法
    print(ProductUnit.REPORT_TIME.code)  # 输出: ('YYYY-MM-DD HH:MM', '报告时间')
    print(ProductUnit.WATER_PRODUCT_RATE.code)  # 输出: ('STB/DAY', '水产量速率')
    print(ProductUnit.WATER_PRODUCT_RATE.desc)  # 输出: 水产量速率
