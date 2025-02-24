import re
from collections import OrderedDict

from mag_tools.utils.common.string_format import StringFormat

from mag_common.reservoir.result.well_product_record import WellProductRecord
# from mag_common.conf.config import Config
from mag_common.model.reservoir.product_column_name import ProductColumnName


class WellProduction:

    def __init__(self, well_name, unit_map, product_records):
        self.well_name = well_name
        self.unit_map = unit_map
        self.product_records = product_records

    def get_column_names(self):
        return [key.value for key in self.unit_map.keys()]

    @staticmethod
    def from_block(block_lines):
        # 获取油井名
        well_name_line = block_lines[0].strip().replace("'", '')
        well_name = well_name_line.split(' ')[1] if 'WELL' in well_name_line else well_name_line

        #获取列名与单位名
        column_names = [name.strip() for name in re.split(r'\t', block_lines[1].strip())]
        unit_names = [name.strip() for name in re.split(r'\t', block_lines[2].strip())]
        # 列名枚举与单位的映射表
        unit_map = OrderedDict((ProductColumnName.get_by_code(column_name), unit_name) for column_name, unit_name in zip(column_names, unit_names))

        # 读取数据
        product_records = []
        for line in block_lines[3:]:
            if line:
                record = WellProductRecord.from_line(column_names, line)
                product_records.append(record)

        return WellProduction(well_name, unit_map, product_records)

    def to_block(self):
        """
        将 WellProduction 对象转换为一个 block
        :return: 文本行的数据
        """
        block_lines = []
        # 添加油井名
        if 'FIELD_TOTAL' not in self.well_name and 'FIP_REG' not in self.well_name:
            block_lines.append(f"WELL '{self.well_name}'")
        else:
            block_lines.append(self.well_name)

        # 添加列名和单位名
        column_names = self.get_column_names()
        unit_names = [self.unit_map[ProductColumnName.get_by_code(name)]+'\t' for name in column_names]

        new_column_names = [' '*12+name+'\t' if name == ProductColumnName.REPORT_TIME.code else name for name in column_names]

        # 对Time列，应设置宽度为16
        block_lines.append(StringFormat.pad_values(new_column_names, 12))
        block_lines.append(StringFormat.pad_values(unit_names, 12))

        # 添加数据行
        for record in self.product_records:
            block_lines.append(record.to_line(column_names, '\t', 12, self.get_decimal_places()))

        return block_lines