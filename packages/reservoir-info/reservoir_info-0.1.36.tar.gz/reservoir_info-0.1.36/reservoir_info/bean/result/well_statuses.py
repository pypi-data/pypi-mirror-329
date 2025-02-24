import os

from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.string_utils import StringUtils

from reservoir_info.bean.result.wel_status import WellStatus


class WellStatuses:
    def __init__(self, name, x_coord_base, y_coord_base, well_statuses_total):
        self.name = name
        self.suffix = '_wstu.out'
        self.x_coord_base = x_coord_base
        self.y_coord_base = y_coord_base
        self.well_statuses_total = well_statuses_total   # 全部井的状态信息的map，key为日期，value为WellStatus

    @classmethod
    def load_from_file(cls, file_path):
        name = os.path.basename(file_path).replace('_wstu.out', '')

        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]

        coord_map = StringUtils.parse_strings_to_map(lines[0:2])
        x_coord_base = coord_map['XCOORD0']
        y_coord_base = coord_map['YCOORD0']

        well_statuses_total = {}
        date_blocks = ListUtils.split_by_keyword(lines[3:], 'Date ')
        for date_block in date_blocks:
            date = date_block[0]

            well_statuses_of_day = []
            well_blocks = ListUtils.split_by_keyword(date_block[1:])
            for well_block in well_blocks:
                well_status = WellStatus.from_block(date, well_block)
                well_statuses_of_day.append(well_status)

            well_statuses_total[date] = well_statuses_of_day

        return WellStatuses(name, x_coord_base, y_coord_base, well_statuses_total)

    def to_lines(self):
        lines = [f'XCOORD0 {self.x_coord_base}', f'YCOORD0 {self.y_coord_base}', '']

        for date, well_status_of_day in self.well_statuses_total.items():
            lines.append(f'Date {date}')
            for well_status in well_status_of_day:
                date_block = well_status.to_block(13)
                lines.extend(date_block)
        return lines

    def save_to_file(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            lines = self.to_lines()
            for line in lines:
                file.write(line)

if __name__ == '__main__':
    _file_path = r'D:\HiSimPack\examples\Comp\spe9\SPE9_wstu.out'
    statuses = WellStatuses.load_from_file(_file_path)

    for _line in statuses.to_lines():
        print(_line)

    statuses.save_to_file(r'D:\HiSimPack\examples\Comp\spe9\SPE9_bak_wstu.out')




