from mag_tools.bean.data_format import DataFormat
from mag_tools.bean.text_format import TextFormat

from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.string_format import StringFormat
from mag_tools.utils.data.string_utils import StringUtils
from typing import List, Optional


class Swof:
    def __init__(self, sw: Optional[float] = None, krw: Optional[float] = None, krow: Optional[float] = None, pcow: Optional[float] = None):
        """
        SWOF 表格有四列数据
        :param sw: 水饱和度
        :param krw: 水的相对渗透率
        :param krow: 油在水中的相对渗透率
        :param pcow: 毛管力 Pcow(=Po-Pw)
        """
        self.sw = sw
        self.krw = krw
        self.krow = krow
        self.pcow = pcow

    @classmethod
    def from_text(cls, text: str, titles: List[str]) -> 'Swof':
        items = text.split()
        values = {title.lower().replace('(=po-pw)', '').strip(): StringUtils.to_value(items[index], float) for index, title in enumerate(titles)}
        return cls(**values)

    def to_text(self, titles: List[str], pad_length: int) -> str:
        data_formats = {
            'sw': DataFormat(decimal_places=6, decimal_places_of_zero=6),
            'krw': DataFormat(decimal_places=9, decimal_places_of_zero=6),
            'krow': DataFormat(decimal_places=6, decimal_places_of_zero=6),
            'pcow': DataFormat(decimal_places=9, decimal_places_of_zero=6)
        }

        items = [StringFormat.format_number(getattr(self, title.lower().replace('(=po-pw)', '').strip()), data_formats[title.lower().replace('(=po-pw)', '').strip()]) for title in titles]
        return StringFormat.pad_values(items, pad_length, JustifyType.LEFT)

    def get_max_length(self) -> int:
        return max(len(str(value)) for value in [self.sw, self.krw, self.krow, self.pcow] if value is not None)

class SwofSet:
    def __init__(self, titles=None, swofs=None):
        """
        油水共存时关于 Sw 的饱和度函数函数，用于黑油模型、油水模型和组分模型
        :param titles: 列名数组
        :param swofs: SWOF数组
        """
        self.titles = titles
        self.swofs = swofs if swofs else []

        self.text_format = TextFormat(number_per_line=4, justify_type=JustifyType.LEFT, at_header='', decimal_places=5, decimal_places_of_zero=0)
        self.pad_length = 0

    @classmethod
    def from_block(cls, block_lines):
        swof_set = SwofSet()

        # 处理标题行，为空则设置缺省值
        block_lines = ListUtils.trim(block_lines)
        if 'Sw' not in block_lines[1]:
            titles_text = 'Sw Krw Krow Pcow(=Po-Pw)'
        else:
            titles_text = block_lines[1].replace('#', '')
            if '(' not in titles_text:
                titles_text = titles_text.replace('Pc', 'Pcow(=Po-Pw)')
        swof_set.titles = titles_text.split()

        max_length = 0
        for line in block_lines[2:]:
            if line.strip() != '/':
                swof = Swof.from_text(line, swof_set.titles)
                swof_set.swofs.append(swof)
                max_length = max(max_length, swof.get_max_length())
        swof_set.pad_length = max_length+2 if max_length > 12 else 12

        return swof_set

    def to_block(self):
        lines = ['SWOF']
        title_items = ['# Sw', 'Krw', 'Krow', 'Pcow(=Po-Pw)']
        lines.append(StringFormat.pad_values(title_items, self.pad_length, JustifyType.LEFT))

        for swof in self.swofs:
            lines.append(swof.to_text(self.titles, self.pad_length))
        lines.append('/')

        return lines

    def __str__(self):
        return '\n'.join(self.to_block())

if __name__ == '__main__':
    _lines = ['SWOF',
'#           Sw         Krw       Krow       Pcow(=Po-Pw)',
       '0.15109           0           1         400',
       '0.15123           0     0.99997      359.19',
       '0.15174           0     0.99993      257.92',
       '0.15246           0     0.99991      186.31',
       '0.15647           0     0.99951       79.06',
       '0.16585           0     0.99629       40.01',
       '0.17835           0     0.99159       27.93',
       '0.20335      1e-005     0.97883        20.4']
    _swof_set = SwofSet.from_block(_lines)
    print(_swof_set)
