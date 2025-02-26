from typing import List, Optional

from mag_tools.bean.text_format import TextFormat
from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.array_utils import ArrayUtils


class DimensionValue:
    def __init__(self, dv_type:Optional[str]=None, data_1d:Optional[List[str]]=None):
        """
        维度数值，实数
        如：DXV
            24*300
        :param dv_type: 维度数据类型
        :param data_1d:  维度数值数组[]
        """
        self.dv_type = dv_type
        self.data_1d = data_1d
        self.text_format = TextFormat(5, JustifyType.LEFT, ' ', 2, 0)

    @classmethod
    def from_block(cls, block_lines):
        _dv = cls()
        _dv.dv_type = block_lines[0].strip()
        _dv.data_1d = ArrayUtils.lines_to_array_1d(block_lines[1:], int)

        return _dv

    def to_block(self):
        lines = [self.dv_type]
        lines.extend(ArrayUtils.array_1d_to_lines(self.data_1d, self.text_format))
        return lines

    def __str__(self):
        return "\n".join(self.to_block())



if __name__ == '__main__':
    # 示例用法
    _lines = [
        'DXV',
        ' 24*300'
    ]

    dv = DimensionValue.from_block(_lines)
    print(dv)

    _lines = dv.to_block()
    for li in _lines:
        print(li)
