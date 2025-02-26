import numpy as np

from mag_tools.bean.text_format import TextFormat
from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.array_utils import ArrayUtils


class Poro:
    """

    """
    def __init__(self, nx, ny, nz):
        """
        表示多组网格单元的孔隙度, 实数三维数组
        :param nx: 行数
        :param ny: 列数
        :param nz: 层数
        """
        self.text_format = TextFormat(5, JustifyType.RIGHT, ' ', 3, 1)
        self.data_3d = np.zeros((nz, nx, ny)).tolist()

    @classmethod
    def from_block(cls, block_lines, nx, ny, nz):
        """
        从一个文本块中生成 Poro
        :param nx: 网络的行数
        :param ny: 网络的列数
        :param nz: 网络的层数
        :param block_lines: 文本块，每行为一层的数值列表，如：600*0.087
        :return:
        """
        poro = cls(nx, ny, nz)
        poro.data_3d = ArrayUtils.lines_to_array_3d(block_lines[1:], nx, ny, nz, float)

        return poro

    def to_block(self):
        lines = ['PORO']
        lines.extend(ArrayUtils.array_3d_to_lines(self.data_3d, self.text_format))
        return lines

    def __str__(self):
        return "\n".join(self.to_block())

if __name__ == '__main__':
    _str = "PORO\n8*0.087\n8*0.097\n8*0.111"
    _lines = _str.split('\n')
    p = Poro.from_block(_lines, 2,4, 3)
    print(p)