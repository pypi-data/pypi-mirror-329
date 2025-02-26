from mag_tools.bean.data_format import DataFormat
from mag_tools.bean.text_format import TextFormat

from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.string_format import StringFormat
from mag_tools.utils.data.string_utils import StringUtils
from typing import List, Optional


class Pvtw:
    def __init__(self, pref: Optional[float] = None, refbw: Optional[float] = None, cw: Optional[float] = None, refvisw: Optional[float] = None, cvisw: Optional[float] = None):
        """
        PVTW 水的 PVT 属性, 同一个 PVT 区域，PVTW 和 WATERTAB 只能使
        :param pref: 参考压力
        :param refbw: 参考体积系数
        :param cw: 压缩系数
        :param refvisw: 参考粘度
        :param cvisw: 粘度系数
        """
        self.pref = pref
        self.refbw = refbw
        self.cw = cw
        self.refvisw = refvisw
        self.cvisw = cvisw

        self.text_format = TextFormat(number_per_line=5, justify_type=JustifyType.LEFT, at_header='', decimal_places=6,
                                 decimal_places_of_zero=6)

    @classmethod
    def from_block(cls, block_lines: List[str]) -> 'Pvtw' or None:
        if not block_lines:
            return None

        # 处理标题行，为空则设置缺省值
        if 'Pref' not in block_lines[1]:
            titles_text = 'Pref refBw Cw refVisw Cvisw'
        else:
            titles_text = block_lines[1].replace('#', '')
        titles = titles_text.split()

        items = block_lines[2].split()
        values = {title.lower().strip(): StringUtils.to_value(items[index], float) for index, title in enumerate(titles)}

        return cls(**values)

    def to_block(self) -> List[str]:
        pad_length = max(len(str(value)) for value in [self.pref, self.refbw, self.cw, self.refvisw, self.cvisw] if value is not None)+2
        if pad_length <= 8: pad_length = 10

        title_items = ['Pref', 'refBw', 'Cw', 'refVisw', 'Cvisw']

        data_formats = {
            'pref': DataFormat(decimal_places=0, decimal_places_of_zero=0),
            'refbw': DataFormat(decimal_places=4, decimal_places_of_zero=4),
            'cw': DataFormat(decimal_places=6, decimal_places_of_zero=6),
            'refvisw': DataFormat(decimal_places=2, decimal_places_of_zero=2),
            'cvisw': DataFormat(decimal_places=0, decimal_places_of_zero=0)
        }

        value_items = [StringFormat.format_number(getattr(self, title.lower().strip()), data_formats[title.lower().strip()]) for title in title_items]

        return ['PVTW', f"# {StringFormat.pad_values(title_items, pad_length, JustifyType.LEFT)}",
                 f"  {StringFormat.pad_values(value_items, pad_length, JustifyType.LEFT)}"]

    def __str__(self):
        return '\n'.join(self.to_block())


if __name__ == '__main__':
    _lines = ['PVTW',
              '# Pref refBw Cw refVisw Cvisw',
              '3600 1.0034 1e-006 0.96 0']

    pvtw_set = Pvtw.from_block(_lines)
    print(pvtw_set)
