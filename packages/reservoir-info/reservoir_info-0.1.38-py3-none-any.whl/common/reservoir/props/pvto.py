from mag_tools.bean.common.data_format import DataFormat
from mag_tools.bean.common.text_format import TextFormat
from mag_tools.model.common.data_type import DataType
from mag_tools.model.common.justify_type import JustifyType
from mag_tools.utils.common.list_utils import ListUtils
from mag_tools.utils.common.string_format import StringFormat
from mag_tools.utils.common.string_utils import StringUtils
from typing import List, Optional


class Pvto:
    def __init__(self, rssat: Optional[float] = None, pres: Optional[float] = None, bo: Optional[float] = None, vis: Optional[float] = None):
        """
        PVTO 活油(live oil)的 PVT 属性
        :param rssat: 溶解气油比
        :param pres: 压力
        :param bo: 体积系数
        :param vis: 粘度
        """
        self.rssat = rssat
        self.pres = pres
        self.bo = bo
        self.vis = vis

    @classmethod
    def from_text(cls, text: str, titles: List[str]) -> 'Pvto':
        items = text.replace('/', '').split()
        if len(items) != len(titles):
            raise ValueError(f"Data length {len(items)} does not match titles length {len(titles)}")

        values = {title.lower().strip(): StringUtils.to_value(items[index], DataType.FLOAT) for index, title in enumerate(titles)}
        return cls(**values)

    def to_text(self, titles: List[str], pad_length: int, is_first_line=False) -> str:
        data_formats = {
            'rssat': DataFormat(decimal_places=3, decimal_places_of_zero=3),
            'pres': DataFormat(decimal_places=1, decimal_places_of_zero=1),
            'bo': DataFormat(decimal_places=4, decimal_places_of_zero=4),
            'vis': DataFormat(decimal_places=3, decimal_places_of_zero=3)
        }

        items = [StringFormat.format_number(getattr(self, title.lower().strip()), data_formats[title.lower().strip()]) for title in titles]

        if not is_first_line:
            items[0] = ' ' * len(items[0])

        return StringFormat.pad_values(items, pad_length, JustifyType.LEFT)

    def get_max_length(self) -> int:
        return max(len(str(value)) for value in [self.rssat, self.pres, self.bo, self.vis] if value is not None)


class PvtoSet:
    def __init__(self, titles: List[str] = None, pvtos: List[List[Pvto]] = None) -> None:
        """
        活油(live oil)的 PVT 属性
        :param titles: 列名数组
        :param pvtos: PVTO二维数组，是一个组合表格
        """
        self.titles = titles
        self.pvtos = pvtos if pvtos else list()

        self.text_format = TextFormat( number_per_line=4, justify_type=JustifyType.LEFT, at_header='', decimal_places=6,
                                 decimal_places_of_zero=6)
        self.pad_length = 0

    @classmethod
    def from_block(cls, block_lines: List[str]) -> 'PvtoSet':
        pvto_set = cls()

        # 处理标题行，为空则设置缺省值
        block_lines = ListUtils.trim(block_lines)
        if 'Rssat' not in block_lines[1]:
            titles_text = 'Rssat Pres Bo Vis'
        else:
            titles_text = block_lines[1].replace('#', '').strip()
            block_lines = block_lines[2:]
        pvto_set.titles = titles_text.split()

        current_block_lines = []
        for line in block_lines:
            if '/' in line and len(line.strip()) > 1:
                current_block_lines.append(line)
                subtable = cls.__get_subtable(current_block_lines, pvto_set.titles)
                pvto_set.pvtos.append(subtable)
                current_block_lines = []
            elif '/' not in line:
                current_block_lines.append(line)

        # 取最大长度
        max_length = 0
        for subtable in pvto_set.pvtos:
            for pvto in subtable:
                max_length = max(max_length, pvto.get_max_length())

        pvto_set.pad_length = max_length + 2 if max_length > 12 else 12

        return pvto_set

    def to_block(self) -> List[str]:
        lines = ['PVTO']
        title_items = ['#', 'Rssat', 'Pres', 'Bo', 'Vis']
        lines.append(StringFormat.pad_values(title_items, self.pad_length, JustifyType.LEFT))

        for subtable in self.pvtos:
            lines.extend(self.__subtable_to_lines(subtable))

        lines.append('/')

        return lines

    def __str__(self) -> str:
        return '\n'.join(self.to_block())

    @classmethod
    def __get_subtable(cls, subtable_block_lines:List[str], titles) -> List[Pvto]:
        subtable = []
        subtable_block_lines = cls.__complete_subtable_lines(subtable_block_lines)

        for line in subtable_block_lines:
            subtable.append(Pvto.from_text(line, titles))

        return subtable

    def __subtable_to_lines(self, subtable: List[Pvto]) -> List[str]:
        if subtable is None or len(subtable) == 0:
            return []

        lines = [StringFormat.pad_value('', self.pad_length) +subtable[0].to_text(self.titles, self.pad_length, True)]
        for index, pvto in enumerate(subtable[1:]):
            lines.append(StringFormat.pad_value('', self.pad_length) +pvto.to_text(self.titles, self.pad_length))
        lines[-1] += '/'
        return lines

    @classmethod
    def __complete_subtable_lines(cls, lines: List[str]) -> List[str]:
        current_rssat = lines[0].split()[0]
        return [f"{current_rssat} {line.strip()}" if (len(line.split()) < 4 or (len(line.split()) == 4 and '/' in line)) else line for line in lines]


if __name__ == '__main__':
    _lines = [
        'PVTO',
        '# Rssat Pres Bo Vis',
        '0.165 400 1.012 1.17 /',
        '0.335 800 1.0255 1.14 /',
        '0.5 1200 1.038 1.11 /',
        '0.665 1600 1.051 1.08 /',
        '0.828 2000 1.063 1.06 /',
        '0.985 2400 1.075 1.03 /',
        '1.13 2800 1.087 1.00 /',
        '1.270 4014.7 1.695 0.51',
        '      5014.7 1.671 0.549',
        '      9014.7 1.579 0.74 /',
        '1.618 5014.7 1.827 0.449',
        '      9014.7 1.726 0.605 /',
        '/'
    ]

    _pvto_set = PvtoSet.from_block(_lines)
    print(_pvto_set)
