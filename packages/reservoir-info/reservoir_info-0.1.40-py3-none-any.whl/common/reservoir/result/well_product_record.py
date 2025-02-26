import re
from typing import List

from mag_tools.bean.common.base_data import BaseData
from mag_tools.utils.common.string_format import StringFormat

from mag_common.model.reservoir.product_column_name import ProductColumnName


class WellProductRecord(BaseData):

    def __init__(self, report_time, work_time, water_product_rate, gas_product_rate, oil_product_rate,
                 water_inject_rate, gas_inject_rate, water_product_total, gas_product_total, oil_product_total,
                 water_inject_total, gas_inject_total, bottom_hole_pressure, tubing_head_pressure, liquid_product_rate,
                 liquid_product_total, water_cut, water_gas_ratio, gas_oil_ratio, increase_time, molar_flow_rate):
        """
        井生产数据类，包含了井的生产和注入数据。

        参数：
        :param report_time: 报告时间，格式为 'YYYY-MM-DD HH:MM'
        :param work_time: 工作时长，单位为  DAYS
        :param water_product_rate: 水生产速率，单位为 STB/DAY
        :param gas_product_rate: 气生产速率，单位为 Mscf/DAY
        :param oil_product_rate: 油生产速率，单位为 STB/DAY
        :param water_inject_rate: 水注入速率，单位为 STB/DAY
        :param gas_inject_rate: 气注入速率，单位为 Mscf/DAY
        :param water_product_total: 累计水生产量，单位为 STB
        :param gas_product_total: 累计气生产量，单位为 Mscf
        :param oil_product_total: 累计油生产量，单位为 STB
        :param water_inject_total: 累计水注入量，单位为 STB
        :param gas_inject_total: 累计气注入量，单位为 Mscf
        :param bottom_hole_pressure: BHP，井底压力，单位为 PSIA
        :param tubing_head_pressure: THP,油管头压力，单位为 PSIA
        :param liquid_product_rate: 液体生产速率，单位为 STB/DAY
        :param liquid_product_rate: 液体生产速率，单位为 STB/DAY
        :param liquid_product_total: 液体生产总量，单位为 STB
        :param water_cut: 生产液体中水的比例，单位：STB/STB
        :param water_gas_ratio: 水汽比，单位为 STB/Mscf
        :param gas_oil_ratio: 汽油比，单位为 STB/Mscf
        :param increase_time: 递增时间，单位为 DAY
        :param molar_flow_rate: 摩尔流速，单位为 mol/s
        """
        super().__init__()
        self.report_time = report_time
        self.work_time = work_time
        self.water_product_rate = water_product_rate
        self.gas_product_rate = gas_product_rate
        self.oil_product_rate = oil_product_rate
        self.water_inject_rate = water_inject_rate
        self.gas_inject_rate = gas_inject_rate
        self.water_product_total = water_product_total
        self.gas_product_total = gas_product_total
        self.oil_product_total = oil_product_total
        self.water_inject_total = water_inject_total
        self.gas_inject_total = gas_inject_total
        self.bottom_hole_pressure = bottom_hole_pressure
        self.tubing_head_pressure = tubing_head_pressure
        self.liquid_product_rate = liquid_product_rate
        self.liquid_product_total = liquid_product_total
        self.water_cut = water_cut
        self.water_gas_ratio = water_gas_ratio
        self.gas_oil_ratio = gas_oil_ratio
        self.increase_time = increase_time
        self.molar_flow_rate = molar_flow_rate

    @staticmethod
    def from_line(column_names, line_text):
        """
        从一行文本中解析数据并创建 WellProduction 对象。
        参数：
        :param column_names: 列名列表
        :param line_text: 生产数据的数值列表
        :return: WellProduction
        """
        values = [value.strip() for value in re.split(r'\t', line_text.strip())]
        data = {name: value for name, value in zip(column_names, values)}

        try:
            return WellProductRecord(report_time=data[ProductColumnName.REPORT_TIME],
                                     work_time=int(data[ProductColumnName.WORK_TIME]),
                                     water_product_rate=float(data[ProductColumnName.WATER_PRODUCT_RATE]),
                                     gas_product_rate=float(data[ProductColumnName.GAS_PRODUCT_RATE]),
                                     oil_product_rate=float(data[ProductColumnName.OIL_PRODUCT_RATE]),
                                     water_inject_rate=float(data[ProductColumnName.WATER_INJECT_RATE]),
                                     gas_inject_rate=float(data[ProductColumnName.GAS_INJECT_RATE]),
                                     water_product_total=float(data[ProductColumnName.WATER_PRODUCT_TOTAL]),
                                     gas_product_total=float(data[ProductColumnName.GAS_PRODUCT_TOTAL]),
                                     oil_product_total=float(data[ProductColumnName.OIL_PRODUCT_TOTAL]),
                                     water_inject_total=float(data[ProductColumnName.WATER_INJECT_TOTAL]),
                                     gas_inject_total=float(data[ProductColumnName.GAS_INJECT_TOTAL]),
                                     bottom_hole_pressure=float(data[ProductColumnName.BOTTOM_HOLE_PRESSURE]),
                                     tubing_head_pressure=float(data[ProductColumnName.TUBING_HEAD_PRESSURE]),
                                     liquid_product_rate=float(data[ProductColumnName.LIQUID_PRODUCT_RATE]),
                                     liquid_product_total=float(data[ProductColumnName.LIQUID_PRODUCT_TOTAL]),
                                     water_cut=float(data[ProductColumnName.WATER_CUT]),
                                     water_gas_ratio=float(data[ProductColumnName.WATER_GAS_RATIO]),
                                     gas_oil_ratio=float(data[ProductColumnName.GAS_OIL_RATIO]),
                                     increase_time=int(data[ProductColumnName.INCREASE_TIME]),
                                     molar_flow_rate=None)
        except Exception:
            print(f"{data}")

    def to_line(self, column_names:List[ProductColumnName], sep:str, pad_length:int, decimal_places:int=5)->str:
        """
        将 WellProductRecord 对象转换为以 分隔符分隔的字符串。
        参数：
        :param pad_length: 字段及分隔符的长度，不足空格填补
        :param column_names: 列名列表
        :param sep: 分隔符
        :param decimal_places: 小数位数
        :return: 以 sep 分隔的字符串
        """
        self.set_decimal_places(decimal_places)

        data = {ProductColumnName.REPORT_TIME: self.report_time,
                ProductColumnName.WORK_TIME: self.work_time,
                ProductColumnName.WATER_PRODUCT_RATE: self.water_product_rate,
                ProductColumnName.GAS_PRODUCT_RATE: self.gas_product_rate,
                ProductColumnName.OIL_PRODUCT_RATE: self.oil_product_rate,
                ProductColumnName.WATER_INJECT_RATE: self.water_inject_rate,
                ProductColumnName.GAS_INJECT_RATE: self.gas_inject_rate,
                ProductColumnName.WATER_PRODUCT_TOTAL: self.water_product_total,
                ProductColumnName.GAS_PRODUCT_TOTAL: self.gas_product_total,
                ProductColumnName.OIL_PRODUCT_TOTAL: self.oil_product_total,
                ProductColumnName.WATER_INJECT_TOTAL: self.water_inject_total,
                ProductColumnName.GAS_INJECT_TOTAL: self.gas_inject_total,
                ProductColumnName.BOTTOM_HOLE_PRESSURE: self.bottom_hole_pressure,
                ProductColumnName.TUBING_HEAD_PRESSURE: self.tubing_head_pressure,
                ProductColumnName.LIQUID_PRODUCT_RATE: self.liquid_product_rate,
                ProductColumnName.LIQUID_PRODUCT_TOTAL: self.liquid_product_total,
                ProductColumnName.WATER_CUT: self.water_cut,
                ProductColumnName.WATER_GAS_RATIO: self.water_gas_ratio,
                ProductColumnName.GAS_OIL_RATIO: self.gas_oil_ratio,
                ProductColumnName.INCREASE_TIME: self.increase_time,
                ProductColumnName.MOLAR_FLOW_RATE: self.molar_flow_rate}

        self.set_same_pad_length(pad_length)
        self.set_decimal_places(decimal_places)
        text = self.get_text([column_name.name for column_name in column_names])
        print(text)

        values = [StringFormat.format_number(data[column_name], self.get_data_format(column_name.name)) for column_name in column_names]
        format_values = StringFormat.pad_values(values, pad_length, self._text_format.justify_type, sep)
        text = ''.join(format_values)
        print(text)
        return text

if __name__ == '__main__':
    title_str = '''
    Time	    WorkTime	 WatProdRate	 GasProdRate	 OilProdRate	  WatInjRate	  GasInjRate	WatProdTotal	GasProdTotal	OilProdTotal	 WatInjTotal	 GasInjTotal	         BHP	         THP	 LiqProdRate	LiqProdTotal	    WaterCut	 WatGasRatio	 GasOilRatio	    IncrTime
    '''
    value_str = '''
    0.02	        0.01	     27.5575	           0	     16130.5	        5000	           0	    0.576931	           0	     387.606	         100	           0	     6021.85	           0	       16158	     388.183	   0.0017055	         INF	           0	        0.02
           '''
    titles = title_str.split()

    col_nums = [ProductColumnName.get_by_code(title) for title in titles]

    record = WellProductRecord.from_line(col_nums, value_str)

    _lines = record.to_line(col_nums, '\t', 12, 5)
    for line in _lines:
        print(line)
