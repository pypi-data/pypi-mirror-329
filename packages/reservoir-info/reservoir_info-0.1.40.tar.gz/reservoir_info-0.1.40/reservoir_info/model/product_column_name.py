
from mag_tools.model.base_enum import BaseEnum


class ProductColumnName(BaseEnum):
    """
    产品列名称枚举
    枚举值为产品列的名称，如：ProductColumnName.REPORT_TIME
    """
    REPORT_TIME = ('Time', '报告时间')  # 报告时间
    WORK_TIME = ('WorkTime', '工作时间')  # 工作时间
    WATER_PRODUCT_RATE = ('WatProdRate', '水产量速率')  # 水产量速率
    GAS_PRODUCT_RATE = ('GasProdRate', '气产量速率')  # 气产量速率
    OIL_PRODUCT_RATE = ('OilProdRate', '油产量速率')  # 油产量速率
    WATER_INJECT_RATE = ('WatInjRate', '水注入速率')  # 水注入速率
    GAS_INJECT_RATE = ('GasInjRate', '气注入速率')  # 气注入速率
    WATER_PRODUCT_TOTAL = ('WatProdTotal', '水总产量')  # 水总产量
    GAS_PRODUCT_TOTAL = ('GasProdTotal', '气总产量')  # 气总产量
    OIL_PRODUCT_TOTAL = ('OilProdTotal', '油总产量')  # 油总产量
    WATER_INJECT_TOTAL = ('WatInjTotal', '水总注入量')  # 水总注入量
    GAS_INJECT_TOTAL = ('GasInjTotal', '气总注入量')  # 气总注入量
    BOTTOM_HOLE_PRESSURE = ('BHP', '底孔压力')  # 底孔压力
    TUBING_HEAD_PRESSURE = ('THP', '管头压力')  # 管头压力
    LIQUID_PRODUCT_RATE = ('LiqProdRate', '液体产量速率')  # 液体产量速率
    LIQUID_PRODUCT_TOTAL = ('LiqProdTotal', '液体总产量')  # 液体总产量
    WATER_CUT = ('WaterCut', '含水率')  # 含水率
    WATER_GAS_RATIO = ('WatGasRatio', '水气比')  # 水气比
    GAS_OIL_RATIO = ('GasOilRatio', '气油比')  # 气油比
    INCREASE_TIME = ('IncrTime', '增加时间')  # 增加时间
    MOLAR_FLOW_RATE = ('MolarFlowRate', '摩尔流速')  # 摩尔流速

if __name__ == '__main__':
    # 示例用法
    print(ProductColumnName.REPORT_TIME.code)  # 输出: ('Time', '报告时间')
    print(ProductColumnName.WATER_PRODUCT_RATE.code)  # 输出: ('WatProdRate', '水产量速率')
    print(ProductColumnName.WATER_PRODUCT_RATE.desc)  # 输出: 水产量速率
