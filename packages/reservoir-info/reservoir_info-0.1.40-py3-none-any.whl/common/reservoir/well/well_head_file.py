from mag_tools.utils.common.string_format import StringFormat

from mag_common.reservoir.well.well_head import WellHead



class WellHeadFile:
    def __init__(self):
        self.well_heads = []
        self.max_length = 0

    @classmethod
    def from_text(cls, text):
        well_head_file = cls()
        well_head_file.__load_from_file(text.split()[1].replace("'", ""))
        return well_head_file

    def to_text(self):
        self.__save_to_file()
        return f"WELLHEAD '{self.file_path}'"

    def __str__(self):
        return f"WELLHEAD '{self.file_path}'"

    def __load_from_file(self, file_path):
        with open(file_path, 'r') as f:
            self.file_path = file_path
            lines = f.readlines()

            for line in lines[1:]:
                well_head = WellHead.from_text(line)
                self.well_heads.append(well_head)
                self.max_length = max(self.max_length, well_head.get_max_length)

    def __save_to_file(self):
        with open(self.file_path, 'w', encoding='utf-8') as file:
            for line in self.__to_block_of_file():
                file.write(line)
                file.write('\n')

    def __to_block_of_file(self):
        x_coord_text = StringFormat.pad_value('Xcoord', self.max_length)
        y_coord_text = StringFormat.pad_value('Ycoord', self.max_length)
        tmd_text = StringFormat.pad_value('MD', self.max_length)
        kb_text = StringFormat.pad_value('KB', self.max_length)

        lines = [f'WELL {x_coord_text} {y_coord_text} {tmd_text} {kb_text}']
        for well_head in self.well_heads:
            lines.append(well_head.to_text(self.max_length))

        return lines

if __name__ == '__main__':
    txt = r"WELLHEAD 'D:\HiSimPack\examples\Comp\spe10\YY_whead'"
    head_file = WellHeadFile.from_text(txt)
    print(head_file)

    head_file.to_text()