from typing import List, Optional

from mag_tools.bean.data_format import DataFormat
from mag_tools.bean.text_format import TextFormat
from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.string_format import StringFormat
from mag_tools.utils.data.string_utils import StringUtils


class Density:
    def __init__(self, oil: Optional[float] = None, water: Optional[float] = None, gas: Optional[float] = None):
        """
        DENSITY 表地面标况下油、水、气的密度
        :param oil: 油密度
        :param water: 水密度
        :param gas: 气密度
        """
        self.oil = oil
        self.water = water
        self.gas = gas

        self.text_format = TextFormat(number_per_line=3, justify_type=JustifyType.RIGHT, at_header='', decimal_places=4,
                                      decimal_places_of_zero=4)

    @classmethod
    def from_block(cls, block_lines: List[str]) -> 'Density' or None:
        if not block_lines:
            return None

        # 处理标题行，为空则设置缺省值
        if 'Oil' not in block_lines[1]:
            titles_text = 'Oil Water Gas'
        else:
            titles_text = block_lines[1].replace('#', '')
        titles = titles_text.split()

        items = block_lines[2].split()
        values = {title.lower().strip(): StringUtils.to_value(items[index], float) for index, title in enumerate(titles)}

        return cls(**values)

    def to_block(self) -> List[str]:
        pad_length = max(len(str(value)) for value in [self.oil, self.water, self.gas] if value is not None) + 2
        if pad_length <= 5: pad_length = 7

        title_items = ['Oil', 'Water', 'Gas']

        data_formats = {
            'oil': DataFormat(decimal_places=2, decimal_places_of_zero=2),
            'water': DataFormat(decimal_places=2, decimal_places_of_zero=2),
            'gas': DataFormat(decimal_places=4, decimal_places_of_zero=4)
        }

        value_items = [StringFormat.format_number(getattr(self, title.lower().strip()), data_formats[title.lower().strip()]) for title in title_items]

        return ['DENSITY', f"# {StringFormat.pad_values(title_items,  pad_length, JustifyType.RIGHT)}",
                f"  {StringFormat.pad_values(value_items, pad_length, JustifyType.RIGHT)}"]

    def __str__(self):
        return '\n'.join(self.to_block())


if __name__ == '__main__':
    _lines = ['DENSITY',
              '# Oil Water Gas',
              '44.98 63.01 0.0702']

    density_set = Density.from_block(_lines)
    print(density_set)
