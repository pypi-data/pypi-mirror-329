from mag_tools.bean.common.data_format import DataFormat
from mag_tools.bean.common.text_format import TextFormat
from mag_tools.model.common.data_type import DataType
from mag_tools.model.common.justify_type import JustifyType
from mag_tools.utils.common.string_format import StringFormat
from mag_tools.utils.common.string_utils import StringUtils
from typing import List, Optional


class Rock:
    def __init__(self, pref: Optional[float] = None, compressibility: Optional[float] = None):
        """
        ROCK 表格有两个数据
        :param pref: 参考压力
        :param compressibility: 压缩系数
        """
        self.pref = pref
        self.compressibility = compressibility

        self.text_format = TextFormat(number_per_line=2, justify_type=JustifyType.LEFT, at_header='', decimal_places=6,
                                 decimal_places_of_zero=6)

    @classmethod
    def from_block(cls, block_lines: List[str]) -> 'Rock' or None:
        if not block_lines:
            return None

        items = block_lines[1].split()
        values = {
            'pref': StringUtils.to_value(items[0], DataType.FLOAT),
            'compressibility': StringUtils.to_value(items[1], DataType.FLOAT)
        }
        return cls(**values)

    def to_block(self) -> List[str]:
        pad_length = max(len(str(value)) for value in [self.pref, self.compressibility] if value is not None) + 2
        title_items = ['Pref', 'Compressibility']

        data_formats = {
            'pref': DataFormat(decimal_places=1, decimal_places_of_zero=1),
            'compressibility': DataFormat(decimal_places=6, decimal_places_of_zero=6)
        }

        value_items = [StringFormat.format_number(getattr(self, title.lower().strip()), data_formats[title.lower().strip()]) for title in title_items]
        return ['ROCK', f"{StringFormat.pad_values(value_items, pad_length, JustifyType.LEFT)}"]

    def __str__(self):
        return '\n'.join(self.to_block())


if __name__ == '__main__':
    _lines = ['ROCK',
              '3600.0 1.0E-6']

    rock = Rock.from_block(_lines)
    print(rock)
