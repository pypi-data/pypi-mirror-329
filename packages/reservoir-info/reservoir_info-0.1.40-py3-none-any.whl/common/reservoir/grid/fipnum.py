from mag_tools.bean.common.text_format import TextFormat
from mag_tools.model.common.data_type import DataType
from mag_tools.model.common.justify_type import JustifyType
from mag_tools.utils.common.array_utils import ArrayUtils
from mag_tools.utils.common.value_utils import ValueUtils


class FipNum:
    def __init__(self, nx, ny, nz):
        """
        网格的 FIP 区域编号数组，整形
        :param nx: 行数
        :param ny: 列数
        :param nz: 层数
        """
        self.text_format = TextFormat(5, JustifyType.LEFT, '')
        self.data_3d = ArrayUtils.init_array_3d(nz, nx, ny)

    @classmethod
    def from_block(cls, block_lines, nx, ny, nz):
        """
        从一个文本块中生成 FipNum
        :param nx: 网络的行数
        :param ny: 网络的列数
        :param nz: 网络的层数
        :param block_lines: 文本块
        :return:
        """
        fip_num = FipNum(nx, ny, nz)
        fip_num.data_3d = ValueUtils.lines_to_array_3d(block_lines[1:], nx, ny, nz, DataType.INTEGER)

        return fip_num

    def to_block(self):
        lines = ['FIPNUM']
        lines.extend(ValueUtils.array_3d_to_lines(self.data_3d, self.text_format))
        return lines

    def __str__(self):
        return "\n".join(self.to_block())

if __name__ == '__main__':
    _str = "FIPNUM\n201 202 203\n204 205 206"
    _lines = _str.split('\n')
    p = FipNum.from_block(_lines, 2, 3, 1)
    print(p)