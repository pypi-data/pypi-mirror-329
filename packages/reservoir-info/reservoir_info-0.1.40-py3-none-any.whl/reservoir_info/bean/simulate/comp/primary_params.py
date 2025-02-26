import re
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from mag_tools.bean.base_data import BaseData
from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.string_format import StringFormat


@dataclass
class PrimaryParams(BaseData):
    uuid: Optional[str] = field(default=None, metadata={"description": "模拟标识"})
    number_of_grid: Optional[int] = field(init=False, default=None, metadata={'description': '网络数'})
    max_poro_vol: Optional[float] = field(init=False, default=None, metadata={'description': '最大poro值'})
    min_poro_vol: Optional[float] = field(init=False, default=None, metadata={'description': '最小poro值'})
    number_of_active_grid: Optional[int] = field(init=False, default=None, metadata={'description': '活动的网格数'})
    number_of_permeable_grid: Optional[int] = field(init=False, default=None, metadata={'description': '透水网络数'})
    length_of_tpfa_connection: Optional[int] = field(init=False, default=None, metadata={'description': 'TPFA连接表大小'})
    cost_of_tpfa_connection: Optional[int] = field(init=False, default=None, metadata={'description': 'TPFA连接表构建时间'})
    number_of_wells: Optional[int] = field(init=False, default=None, metadata={'description': '井数'})
    number_of_branches: Optional[int] = field(init=False, default=None, metadata={'description': '分支数'})
    total_segments: Optional[int] = field(init=False, default=None, metadata={'description': '总井段数'})
    number_of_well_reservoir_connections : Optional[int] = field(init=False, default=None, metadata={'description': '油井到油藏连接数'})

    @classmethod
    def from_block(cls, block_lines: List[str]):
        clazz = cls()

        if len(block_lines) >= 6:
            map_ = cls.__block_to_map(block_lines)

            tpfa_value = map_.pop('length')
            if tpfa_value:
                length, cost = cls.__get_tpfa(tpfa_value)
                map_['length_of_tpfa_connection'] = length
                map_['spent_of_tpfa_connection'] = cost

            for key, value in map_.items():
                if hasattr(clazz, key):
                    field_type = cls.__annotations__[key]
                    value = int(value) if field_type == Optional[int] or field_type == int else float(value)
                    setattr(clazz, key, value)

        return clazz

    def to_block(self):
        attribute_map = self.to_map
        if 'length_of_tpfa_connection_list' in attribute_map:
            attribute_map['Build TPFA connection list for Cartesian grid, length'] = attribute_map.pop('length_of_tpfa_connection_list')

        boundary = '----------------------------------------------------------------------'
        lines = [boundary,
                 StringFormat.pad_value('PRE-PROCESSING', len(boundary), JustifyType.CENTER),
                 f' Number of grid = {self.number_of_grid}; max poro vol = {self.max_poro_vol}; min poro vol = {self.min_poro_vol}',
                 f' Number of active grid = {self.number_of_active_grid}; number of permeable grid = {self.number_of_permeable_grid}',
                 f' Build TPFA connection list for Cartesian grid, length = {self.length_of_tpfa_connection} ({self.cost_of_tpfa_connection} ms)',
                 f' Number of wells = {self.number_of_wells}, number of branches = {self.number_of_branches}, total segments = {self.total_segments}',
                 f' Number of well-to-reservoir connections = {self.number_of_well_reservoir_connections}',
                 boundary]

        return lines


    @classmethod
    def __block_to_map(cls, block: List[str]):
        map_ = {}
        for line in block:
            if '----------------' not in line and 'PRE-PROCESSING' not in line:
                items = re.split(r'[;,]', line)
                for item in items:
                    if '=' in item:
                        key, value = item.split('=')
                        key = key.strip().replace(' ', '_').replace('-', '_').lower()
                        map_[key] = value.strip()
        return map_

    @classmethod
    def __get_tpfa(cls, s: str) -> Tuple[Optional[int], Optional[float]]:
        match = re.match(r"(\d+)\s*\(([\d.]+)\s*ms\)", s)
        if match:
            integer_part = int(match.group(1))
            float_part = float(match.group(2)) if match.group(2) else None
            return integer_part, float_part
        else:
            return None, None

    def __to_tpfa(self):
        return f'{self.length_of_tpfa_connection} ({self.cost_of_tpfa_connection if self.cost_of_tpfa_connection else ''})'


if __name__ == '__main__':
    source_str = '''
----------------------------------------------------------------------
                            PRE-PROCESSING                            
 Number of grid = 1122000; max poro vol = 35.6215; min poro vol = 7.1243e-05
 Number of active grid = 1094421; number of permeable grid = 1094421
 Build TPFA connection list for Cartesian grid, length = 3191860 (39.8693 ms)
 Number of wells = 5, number of branches = 5, total segments = 425
 Number of well-to-reservoir connections = 414
----------------------------------------------------------------------
'''
    pre_processing = PrimaryParams.from_block(source_str.split('\n'))

    block_ = pre_processing.to_block()
    print('\n'.join(block_))