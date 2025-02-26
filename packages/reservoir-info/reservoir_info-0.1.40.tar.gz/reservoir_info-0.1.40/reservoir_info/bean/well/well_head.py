from mag_tools.bean.text_format import TextFormat

from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.string_format import StringFormat
from mag_tools.utils.data.string_utils import StringUtils


class WellHead:
    def __init__(self):
        """
        井头文件包含井名、井头 X 坐标、井头 Y 坐标、总深（TMD）、补心海拔（KB）五列数据
        """
        self.well_name = None
        self.x_coord = None
        self.y_coord = None
        self.tmd = None
        self.kb = None
        self.max_length = 0
        self.text_format = TextFormat(1, JustifyType.RIGHT, '', 3, 0)

    @classmethod
    def from_text(cls, text):
        head = cls()
        items = text.split()
        head.max_length = len(max(items, key=len))

        head.well_name = items[0]
        head.x_coord = StringUtils.to_value(items[1], float)
        head.y_coord = StringUtils.to_value(items[2], float)
        head.tmd = StringUtils.to_value(items[3], float)
        head.kb = StringUtils.to_value(items[4], float)
        return head

    def to_text(self, max_length=None):
        if max_length is None:
            max_length = self.max_length

        x_coord_text = StringFormat.format_number(self.x_coord, self.text_format.get_data_format(self.x_coord))
        y_coord_text = StringFormat.format_number(self.y_coord, self.text_format.get_data_format(self.y_coord))
        tmd_text = StringFormat.format_number(self.tmd, self.text_format.get_data_format(self.tmd))
        kb_text = StringFormat.format_number(self.kb, self.text_format.get_data_format(self.kb))

        text = StringFormat.pad_values([x_coord_text, y_coord_text, tmd_text, kb_text], max_length, JustifyType.RIGHT)
        return f'{self.well_name} {text}'

    def __str__(self):
        return self.to_text()

if __name__ == '__main__':
    line = 'YYH1-1 18594037.720 3282025.234 4115 421'
    wh = WellHead.from_text(line)
    print(wh)