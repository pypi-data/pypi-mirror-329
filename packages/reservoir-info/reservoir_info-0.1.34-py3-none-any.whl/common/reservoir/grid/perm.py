
from mag_tools.bean.common.base_data import BaseData
from mag_tools.bean.common.text_format import TextFormat
from mag_tools.model.common.data_type import DataType
from mag_tools.model.common.justify_type import JustifyType
from mag_tools.utils.common.array_utils import ArrayUtils
from mag_tools.utils.common.list_utils import ListUtils
from mag_tools.utils.common.value_utils import ValueUtils

from mag_common.model.reservoir.perm_type import PermType


class Perm(BaseData):
    def __init__(self, perm_type:PermType, nx:int, ny:int, nz:int):
        """
            油藏网格xyz方向渗透率，实数
            :param nx: 行数
            :param ny: 列数
            :param nz: 层数
            """
        super().__init__()
        self.perm_type = perm_type
        self._text_format = TextFormat(5, JustifyType.LEFT, '', 5, 1)
        self.data_3d = ArrayUtils.init_array_3d(nz, nx, ny)

    @classmethod
    def from_block(cls, block_lines, nx, ny, nz):
        block_lines = ListUtils.trim(block_lines)
        perm_type = PermType.get_by_code(block_lines[0].strip())
        perm = cls(perm_type, nx, ny, nz)
        perm.data_3d = ValueUtils.lines_to_array_3d(block_lines[1:], nx, ny, nz, DataType.FLOAT)

        return perm

    def to_block(self):
        lines = [self.perm_type.code]
        lines.extend(ValueUtils.array_3d_to_lines(self.data_3d, self._text_format))

        return lines

    def __str__(self):
        return "\n".join(self.to_block())

# 示例用法
if __name__ == '__main__':
    _lines = [
        'PERMX',
        '121*1.0 121*2.0 121*3.0 121*4.0 121*5.0',
        '',
        'PERMY',
        '49.29276 162.25308 438.45926 492.32336 791.32867',
        '704.17102 752.34912 622.96875 542.24493 471.45953',
        '246.12650 82.07828 82.87408 101.65224 57.53632',
        '47.73741 55.07134 24.33975 41.06571 76.64680',
        '158.22012 84.31137 98.32045 67.18009',
        '59.36459 32.75453 48.89822 78.56290 152.85838',
        '48.61450 45.90883 49.59706 87.95659 63.36467',
        '36.76624 22.82411 12.88787 7.30505 7.74248',
        '11.78211 23.77054 123.28667 618.79059 535.32922',
        '264.58759 387.70538 682.85431 823.64056',
        '390.34323 143.02039 110.37493 66.40274 26.82064',
        '41.63234 45.19296 44.07080 37.41025 25.15281',
        '42.34485 93.56773 142.41193 71.54111 66.90506',
        '100.64468 101.82140 50.54851 68.30826 103.03153',
        '120.99303 71.92981 59.36126 38.84483',
        '82.61102 86.39167 126.21329 36.41510 18.88533',
        '12.30760 10.19921 12.95491 14.53931 111.54144',
        '302.40686 343.12231 271.43484 319.10641 428.27557',
        '438.34317 161.91951 40.33082 51.97308 35.82761',
        '18.24838 30.81277 49.74974 42.04483',
        '39.99637 55.71049 63.62318 67.26822 73.98063',
        '45.19595 42.91018 75.42314 92.84066 123.21178',
        '104.16100 131.49677 77.80956 60.96303 34.25750',
        '34.32304 70.02726 74.91326 75.89129 57.44796',
        '18.24838 30.81277 49.74974 42.04483'
    ]

    blocks = ListUtils.split_by_keyword(_lines)
    _permx= Perm.from_block(blocks[0], 11,11,5)
    _permy =  Perm.from_block(blocks[1], 4,6,5)

    print(_permx)
    print(_permy)

