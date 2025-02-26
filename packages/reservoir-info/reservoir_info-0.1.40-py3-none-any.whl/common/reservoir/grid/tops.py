from mag_tools.bean.common.text_format import TextFormat
from mag_tools.model.common.data_type import DataType
from mag_tools.model.common.justify_type import JustifyType
from mag_tools.utils.common.array_utils import ArrayUtils
from mag_tools.utils.common.value_utils import ValueUtils


class Tops:
    def __init__(self, nx, ny):
        """
        第一层网格的顶面深度，用于结构网格
        实数，数据个数等于第一层网格的网格数
        单位：m (米制)，feet (英制)，cm (lab)，um(MESO)

        :param nx: 行数
        :param ny: 列数
        """
        self.text_format = TextFormat(5, JustifyType.RIGHT, ' ', 2, 2)
        self.data_2d = ArrayUtils.init_array_2d(nx, ny)

    @classmethod
    def from_text(cls, text, nx, ny):
        """
        将文本行转为Tops
        :param text: 文本行
        :param nx: 网络行数
        :param ny: 网络列数
        :return: Tops
        """
        tops = cls(nx, ny)
        text = text.replace("TOPS ", "").strip()
        tops.data_2d = ValueUtils.lines_to_array_2d([text], nx, ny, DataType.FLOAT)

        return tops

    def to_text(self):
        lines = ValueUtils.array_2d_to_lines(self.data_2d, self.text_format)
        return "TOPS" + "".join(lines)

    def __str__(self):
        return self.to_text()

if __name__ == "__main__":
    txt = 'TOPS 600*9000.00'
    _tops = Tops.from_text(txt, 20, 30)
    print(_tops)