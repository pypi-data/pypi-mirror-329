from typing import List, Optional

from mag_tools.bean.data_format import DataFormat
from mag_tools.bean.text_format import TextFormat

from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.string_format import StringFormat
from mag_tools.utils.data.string_utils import StringUtils


class Pvdg:
    def __init__(self, pres: Optional[float] = None, bg: Optional[float] = None, vis: Optional[float] = None):
        """
        PVDG 表格有三列数据
        :param pres: 压力
        :param bg: 气体体积系数
        :param vis: 粘度
        """
        self.pres = pres
        self.bg = bg
        self.vis = vis

    @classmethod
    def from_text(cls, text: str, titles: List[str]) -> 'Pvdg':
        items = text.split()
        values = {title.lower().strip(): StringUtils.to_value(items[index], float) for index, title in enumerate(titles)}
        return cls(**values)

    def to_text(self, titles: List[str], pad_length: int) -> str:
        data_formats = {
            'pres': DataFormat(decimal_places=0, decimal_places_of_zero=0),
            'bg': DataFormat(decimal_places=4, decimal_places_of_zero=4),
            'vis': DataFormat(decimal_places=4, decimal_places_of_zero=4)
        }

        items = [StringFormat.format_number(getattr(self, title.lower().strip()), data_formats[title.lower().strip()]) for title in titles]
        return StringFormat.pad_values(items, pad_length, JustifyType.LEFT)

    def get_max_length(self) -> int:
        return max(len(str(value)) for value in [self.pres, self.bg, self.vis] if value is not None)

class PvdgSet:
    def __init__(self, titles: List[str]=None, pvdgs: List[Pvdg]=None) -> None:
        """
        油，气，不动水共存时关于 Sg 的饱和度函数，用于黑油模型和组分模型
        :param titles: 列名数组
        :param pvdgs: PVDG数组
        """
        self.titles = titles
        self.pvdgs = pvdgs if pvdgs else []

        self.text_format = TextFormat(number_per_line=3, justify_type=JustifyType.LEFT, at_header='', decimal_places=6,
                                 decimal_places_of_zero=6)
        self.pad_length = 0

    @classmethod
    def from_block(cls, block_lines: [str]) -> 'PvdgSet':
        pvdg_set = cls()

        # 处理标题行，为空则设置缺省值
        if 'Pres' not in block_lines[1]:
            titles_text = 'Pres Bg Vis'
        else:
            titles_text = block_lines[1].replace('#', '')
        pvdg_set.titles = titles_text.split()

        max_length = 0
        for line in block_lines[2:]:
            if line != '/':
                pvdg = Pvdg.from_text(line, pvdg_set.titles)
                pvdg_set.pvdgs.append(pvdg)
                max_length = max(max_length, pvdg.get_max_length())
        pvdg_set.pad_length = max_length + 2
        return pvdg_set

    def to_block(self) -> [str]:
        lines = ['PVDG']
        title_items = ['#', 'Pres', 'Bg', 'Vis']
        lines.append(StringFormat.pad_values(title_items, self.pad_length, JustifyType.LEFT))

        for pvdg in self.pvdgs:
            lines.append(StringFormat.pad_value('', self.pad_length) + pvdg.to_text(self.titles, self.pad_length))
        lines.append('/')

        return lines

    def __str__(self):
        return '\n'.join(self.to_block())


if __name__ == '__main__':
    _lines = ['PVDG',
              '# Pres Bg Vis',
    '400 5.4777 0.013',
    '800 2.7392 0.0135',
    '1200 1.8198 0.014',
    '1600 1.3648 0.0145',
    '2000 1.0957 0.015',
    '2400 0.9099 0.0155']

    _pvdg_set = PvdgSet.from_block(_lines)
    print(_pvdg_set)
