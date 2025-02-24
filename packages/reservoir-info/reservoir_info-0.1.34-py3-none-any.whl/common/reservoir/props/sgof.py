from mag_tools.bean.common.data_format import DataFormat
from mag_tools.bean.common.text_format import TextFormat
from mag_tools.model.common.data_type import DataType
from mag_tools.model.common.justify_type import JustifyType
from mag_tools.utils.common.string_format import StringFormat
from mag_tools.utils.common.string_utils import StringUtils
from typing import List, Optional


class Sgof:
    def __init__(self, sg: Optional[float] = None, krg: Optional[float] = None, krog: Optional[float] = None, pcgo: Optional[float] = None):
        """
        SGOF 表格有四列数据
        :param sg: 气体饱和度
        :param krg: 气体的相对渗透率
        :param krog: 油在气中的相对渗透率
        :param pcgo: 毛管力 Pcgo(=Pg-Po)
        """
        self.sg = sg
        self.krg = krg
        self.krog = krog
        self.pcgo = pcgo

    @classmethod
    def from_text(cls, text: str, titles: List[str]) -> 'Sgof':
        items = text.split()
        values = {title.lower().replace('(=pg-po)', '').strip(): StringUtils.to_value(items[index], DataType.FLOAT) for index, title in enumerate(titles)}
        return cls(**values)

    def to_text(self, titles: List[str], pad_length: int) -> str:
        data_formats = {
            'sg': DataFormat(decimal_places=6, decimal_places_of_zero=6),
            'krg': DataFormat(decimal_places=9, decimal_places_of_zero=6),
            'krog': DataFormat(decimal_places=6, decimal_places_of_zero=6),
            'pcgo': DataFormat(decimal_places=9, decimal_places_of_zero=6)
        }

        items = [StringFormat.format_number(getattr(self, title.lower().replace('(=pg-po)', '').strip()), data_formats[title.lower().replace('(=pg-po)', '').strip()]) for title in titles]
        return StringFormat.pad_values(items, pad_length, JustifyType.LEFT)

    def get_max_length(self) -> int:
        return max(len(str(value)) for value in [self.sg, self.krg, self.krog, self.pcgo] if value is not None)

class SgofSet:
    def __init__(self, titles=None, sgofs=None):
        """
        油，气，不动水共存时关于 Sg 的饱和度函数，用于黑油模型和组分模型
        :param titles: 列名数组
        :param sgofs: SWOF数组
        """
        self.titles = titles
        self.sgofs = sgofs if sgofs else []

        self.text_format = TextFormat(number_per_line=4, justify_type=JustifyType.LEFT, at_header='', decimal_places=6,
                                 decimal_places_of_zero=6)
        self.pad_length = 0

    @classmethod
    def from_block(cls, block_lines: [str]) -> 'SgofSet' or None:
        if not block_lines:
            return None

        sgof_set = cls()

        # 处理标题行，为空则设置缺省值
        if 'Sg' not in block_lines[1]:
            titles_text = 'Sg Krg Krog Pcgo(=Pg-Po)'
        else:
            titles_text = block_lines[1].replace('#', '')
        sgof_set.titles = titles_text.split()

        max_length = 0
        for line in block_lines[2:]:
            if line.strip() != '/':
                sgof = Sgof.from_text(line, sgof_set.titles)
                sgof_set.sgofs.append(sgof)
                max_length = max(max_length, sgof.get_max_length())
        sgof_set.pad_length = max_length + 2 if max_length > 12 else 12
        return sgof_set

    def to_block(self) -> [str]:
        lines = ['SGOF']
        title_items = ['# Sg', 'Krg', 'Krog', 'Pcgo(=Pg-Po)']
        lines.append(StringFormat.pad_values(title_items, self.pad_length, JustifyType.LEFT))

        for sgof in self.sgofs:
            lines.append(sgof.to_text(self.titles, self.pad_length))
        lines.append('/')

        return lines

    def __str__(self):
        return '\n'.join(self.to_block())


if __name__ == '__main__':
    _lines = ['#           Sg         Krg       Krog       Pcgo(=Pg-Po)',
    '0.0500000 0.000000 0.593292 0.0523257',
    '0.111111 0.000823045 0.292653 0.0696509',
    '0.172222 0.00658436 0.131341 0.0845766',
    '0.355556 0.102881 0.00457271 0.129908']

    _sgof_set = SgofSet.from_block(_lines)
    print(_sgof_set)
