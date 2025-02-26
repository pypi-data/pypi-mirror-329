from dataclasses import dataclass, field
from typing import Optional
import numpy as np

from mag_tools.bean.common.base_data import BaseData
from mag_tools.bean.text_format import TextFormat

from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.array_utils import ArrayUtils


@dataclass
class Tops(BaseData):
    """
    第一层网格的顶面深度，用于结构网格
    实数，数据个数等于第一层网格的网格数
    单位：m (米制)，feet (英制)，cm (lab)，um(MESO)
    """
    nx: Optional[int] = field(init=False, default=None, metadata={'description': '行数'})
    ny: Optional[int] = field(init=False, default=None, metadata={'description': '列数'})

    def __post_init__(self):
        self._text_format = TextFormat(5, JustifyType.RIGHT, ' ', 2, 2)
        self.data_2d = np.zeros((self.nx, self.ny)).tolist()

    @classmethod
    def from_text(cls, text: str, nx: int, ny: int):
        """
        将文本行转为Tops
        :param text: 文本行
        :param nx: 网络行数
        :param ny: 网络列数
        :return: Tops
        """
        tops = cls()
        tops.nx = nx
        tops.ny = ny
        text = text.replace("TOPS ", "").strip()
        tops.data_2d = ArrayUtils.lines_to_array_2d([text], nx, ny, float)

        return tops

    def to_text(self):
        lines = ArrayUtils.array_2d_to_lines(self.data_2d, self._text_format)
        return "TOPS" + "".join(lines)

    def __str__(self):
        return self.to_text()

if __name__ == "__main__":
    txt = 'TOPS 600*9000.00'
    _tops = Tops.from_text(txt, 20, 30)
    print(_tops)