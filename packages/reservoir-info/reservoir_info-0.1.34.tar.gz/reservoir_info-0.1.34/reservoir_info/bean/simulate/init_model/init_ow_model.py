from dataclasses import dataclass, field
from typing import Optional

from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.string_format import StringFormat
from mag_tools.utils.data.string_utils import StringUtils


@dataclass
class InitOwModel:
    BOUNDARY = '----------------------------------------------------------------------'

    building_matrix_costs: Optional[int] = field(init=False, default=None, metadata={'description': '创建矩阵花费时间，单位：毫秒'})
    sat_reg: Optional[int] = field(init=False, default=None, metadata={'description': '饱和区'})
    eql_reg: Optional[int] = field(init=False, default=None, metadata={'description': '平衡区'})

    @classmethod
    def from_block(cls, block_lines: list[str]):
        init_model = cls()

        if len(block_lines) >= 3:
            matrix_cost_line = ListUtils.pick_line(block_lines, 'Building matrix costs')
            init_model.building_matrix_costs = StringUtils.pick_number(matrix_cost_line)

            reservoir_status_line = ListUtils.pick_line(block_lines, 'Reservoir status INIT')
            numbers = StringUtils.pick_numbers(reservoir_status_line)
            init_model.sat_reg = numbers[0] if numbers and len(numbers) > 0 else None
            init_model.eql_reg = numbers[1] if numbers and len(numbers) > 1 else None
        return init_model

    def to_block(self):
        lines = [InitOwModel.BOUNDARY,
                 StringFormat.pad_value('INIT OIL-WATER MODEL', len(InitOwModel.BOUNDARY), JustifyType.CENTER),
                 '',
                 f' Building matrix costs {self.building_matrix_costs}ms',
                 f' Reservoir status INIT in SAT_REG {self.sat_reg} EQL_REG {self.eql_reg} complete',
                 InitOwModel.BOUNDARY]

        return lines

if __name__ == '__main__':
    source_str = '''
----------------------------------------------------------------------
                         INIT OIL-WATER MODEL                         

 Building matrix costs 107.576ms
 Reservoir status INIT in SAT_REG 1 EQL_REG 1 complete
----------------------------------------------------------------------
'''
    init_ow_model = InitOwModel.from_block(source_str.split('\n'))

    block_ = init_ow_model.to_block()
    print('\n'.join(block_))