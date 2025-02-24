from dataclasses import dataclass, field
from typing import Optional

from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.string_format import StringFormat
from mag_tools.utils.data.string_utils import StringUtils


@dataclass
class InitCompModel:
    BOUNDARY = '----------------------------------------------------------------------'

    building_matrix_costs: Optional[float] = field(init=False, default=None, metadata={'description': '创建矩阵花费时间，单位：毫秒'})
    partition_grid_costs: Optional[float] = field(init=False, default=None, metadata={'description': '分区网格花费时间，单位：毫秒'})
    eos_region: Optional[int] = field(init=False, default=None, metadata={'description': 'EOS区编号'})
    eql_region: Optional[int] = field(init=False, default=None, metadata={'description': 'EQL区编号'})
    tc_exact: Optional[float] = field(init=False, default=None, metadata={'description': 'TC Exact'})
    tc_estimate: Optional[float] = field(init=False, default=None, metadata={'description': 'TC Estimate'})
    vc_exact: Optional[float] = field(init=False, default=None, metadata={'description': 'TC Exact'})
    vc_estimate: Optional[float] = field(init=False, default=None, metadata={'description': 'VC Estimate'})
    sat_reg: Optional[int] = field(init=False, default=None, metadata={'description': '饱和区'})
    eql_reg: Optional[int] = field(init=False, default=None, metadata={'description': '平衡区'})
    pvt_reg: Optional[int] = field(init=False, default=None, metadata={'description': 'PVT'})
    eos_reg: Optional[int] = field(init=False, default=None, metadata={'description': 'EOS'})

    @classmethod
    def from_block(cls, block_lines: list[str]):
        init_model = cls()

        if len(block_lines) >= 4:
            matrix_cost_line = ListUtils.pick_line(block_lines, 'Building matrix costs')
            init_model.building_matrix_costs = StringUtils.pick_number(matrix_cost_line)

            part_grid_line = ListUtils.pick_line(block_lines, 'Partition grid costs')
            init_model.partition_grid_costs = StringUtils.pick_number(part_grid_line)

            contact_line = ListUtils.pick_line(block_lines, 'At gas-oil contact')
            contact_numbers = StringUtils.pick_numbers(contact_line)
            init_model.eos_region = contact_numbers[0]
            init_model.eql_region = contact_numbers[1]

            tc_line = ListUtils.pick_line(block_lines, 'Tc_exact')
            tc_numbers = StringUtils.pick_numbers(tc_line)
            init_model.tc_exact = tc_numbers[0]
            init_model.vc_exact = tc_numbers[1]

            vc_line = ListUtils.pick_line(block_lines, 'Vc_exact')
            vc_numbers = StringUtils.pick_numbers(vc_line)
            init_model.vc_exact = vc_numbers[0]
            init_model.eql_exact = vc_numbers[1]

            status_line = ListUtils.pick_line(block_lines, 'Reservoir status INIT')
            status_numbers = StringUtils.pick_numbers(status_line)
            init_model.sat_reg = status_numbers[0]
            init_model.eql_reg = status_numbers[1]
            init_model.vc_reg = status_numbers[2]
            init_model.sat_reg = status_numbers[3]


        return init_model

    def to_block(self):
        lines = [InitCompModel.BOUNDARY,
                 StringFormat.pad_value('INIT OIL-WATER MODEL', len(InitCompModel.BOUNDARY), JustifyType.CENTER),
                 '',
                 f' Building matrix costs {self.building_matrix_costs}ms',
                 f' Partition grid costs {self.partition_grid_costs}ms',
                 f' At gas-oil contact of EOS region {self.eos_region}, EQL region {self.eql_region}:',
                 f' Tc_exact = {self.tc_exact}, Tc_estimate = {self.tc_estimate}ms',
                 f' Vc_exact = {self.vc_exact}, Vc_estimate = {self.vc_estimate}ms',
                 f' Reservoir status INIT in SAT_REG {self.sat_reg} EQL_REG {self.eql_reg} complete',
                 InitCompModel.BOUNDARY]

        return lines

if __name__ == '__main__':
    source_str = '''
----------------------------------------------------------------------
                        INIT COMPOSITION MODEL

 Building matrix costs 0.2001ms
 Partition grid costs 0.2842ms
 At gas-oil contact of EOS region 1, EQL region 1:
 Tc_exact = 1145.15, Tc_estimate = 1103.78
 Vc_exact = 7.04359, Vc_estimate = 5.93077
 Reservoir status INIT in SAT_REG 1 EQL_REG 1 PVT_REG 1 EOS_REG 1 complete
----------------------------------------------------------------------
'''
    init_ow_model = InitCompModel.from_block(source_str.split('\n'))

    block_ = init_ow_model.to_block()
    print('\n'.join(block_))
