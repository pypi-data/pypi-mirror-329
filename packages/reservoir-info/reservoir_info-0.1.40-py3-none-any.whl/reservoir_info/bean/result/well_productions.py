import os

from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.string_utils import StringUtils

from reservoir_info.bean.result.well_production import WellProduction


class WellProductions:
    def __init__(self, name, productions, description=None):
        self.name = name
        self.suffix = '_prd.out'
        self.productions = productions
        self.description = description

    @staticmethod
    def load_from_file(file_path):
        name = os.path.basename(file_path).replace('_prd.out', '')

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]

        header_lines = []
        well_lines = []
        for line in lines:
            line = line.strip()
            if line.startswith('#'):
                header_lines.append(line)
            else:
                well_lines.append(line)

        productions = []
        blocks = ListUtils.split_by_keyword(well_lines)
        for block in blocks:
            productions.append(WellProduction.from_block(block))

        description = WellProductions.__process_header(header_lines)

        return WellProductions(name, productions, description)

    def save_to_file(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in self.to_lines():
                file.write(line)
                file.write('\n')

    def to_lines(self):
        lines = []
        if self.description:
            lines.append(r"#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
            lines.append(f"# {self.description}")
            lines.append(r"#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

        # 写入每个 WellProduction 的 block
        for production in self.productions:
            block_lines = production.to_block()
            lines.extend(block_lines)
            lines.append("\n")  # 每个 block 之间添加一个空行

        return lines

    @staticmethod
    def __process_header(header_lines):
        description = ''
        for line in header_lines:
            line = StringUtils.pick_tail(line, '#').strip()
            if line.startswith('-'):
                continue
            else:
                description = line
        return description

if __name__ == '__main__':
    # 示例用法
    prd_file = r'D:\HiSimPack\examples\Comp\spe9\SPE9_prd.out'
    wp = WellProductions.load_from_file(prd_file)

    for _line in wp.to_lines():
        print(_line)

    prd_bak_file = r'D:\HiSimPack\examples\Comp\spe9\SPE9_bak_prd.out'
    wp.save_to_file(prd_bak_file)

    # for production in wp.productions: