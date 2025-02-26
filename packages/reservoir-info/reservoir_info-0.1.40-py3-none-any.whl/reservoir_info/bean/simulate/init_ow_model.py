import re
from dataclasses import dataclass, field
from typing import List, Optional

from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.string_format import StringFormat
from mag_tools.utils.data.string_utils import StringUtils
from numpy.matrixlib.defmatrix import matrix


@dataclass
class InitOwModel:
    BOUNDARY = '----------------------------------------------------------------------'

    simulate_id: Optional[str] = field(default=None, metadata={"description": "模拟标识"})
    building_matrix_costs: Optional[int] = field(init=False, default=None, metadata={'description': '创建矩阵花费时间，单位：毫秒'})
    sat_reg: Optional[int] = field(init=False, default=None, metadata={'description': '饱和区'})
    eql_reg: Optional[int] = field(init=False, default=None, metadata={'description': '平衡区'})
    omp_threads: Optional[int] = field(init=False, default=None, metadata={'description': 'OMP线程数'})
    linear_solver: Optional[str] = field(init=False, default=None, metadata={'description': '线性处理器'})
    nonzero_num: Optional[str] = field(init=False, default=None, metadata={'description': '雅可比矩阵非零个数'})
    fe_data_cost: Optional[str] = field(init=False, default=None, metadata={'description': '产生FE数据花费时间，单位：毫秒'})
    write_grid_cost: Optional[str] = field(init=False, default=None, metadata={'description': '写油藏网络信息花费时间，单位：毫秒'})


    @classmethod
    def from_block(cls, block_lines: list[str]):
        init_model = cls()

        if len(block_lines) >= 4:
            matrix_cost_line = ListUtils.pick_line(block_lines, 'Building matrix costs')
            init_model.building_matrix_costs = StringUtils.pick_number(matrix_cost_line)

            reservoir_status_line = ListUtils.pick_line(block_lines, 'Reservoir status INIT')
            numbers = StringUtils.pick_numbers(reservoir_status_line)
            init_model.sat_reg = numbers[0] if numbers and len(numbers) > 0 else None
            init_model.eql_reg = numbers[1] if numbers and len(numbers) > 1 else None

            omp_threads_line = ListUtils.pick_line(block_lines, 'OMP threads')
            init_model.omp_threads = StringUtils.pick_number(omp_threads_line)

            linear_solver_line = ListUtils.pick_line(block_lines, 'Linear solver')
            init_model.linear_solver = StringUtils.pick_number(linear_solver_line)

            nonzero_line = ListUtils.pick_line(block_lines, 'Nonzeros in Jacobian')
            init_model.nonzero_num = StringUtils.pick_number(nonzero_line)

            fe_data_cost_line = ListUtils.pick_line(block_lines, 'Generated FE data')
            init_model.fe_data_cost = StringUtils.pick_number(fe_data_cost_line)

            write_grid_cost_line = ListUtils.pick_line(block_lines, 'Writting reservoir grid info')
            init_model.write_grid_cost = StringUtils.pick_number(write_grid_cost_line)

        return init_model

    def to_block(self):
        lines = [InitOwModel.BOUNDARY,
                 StringFormat.pad_value('INIT OIL-WATER MODEL', len(InitOwModel.BOUNDARY), JustifyType.CENTER),
                 '',
                 f' Building matrix costs {self.building_matrix_costs}ms',
                 f' Reservoir status INIT in SAT_REG {self.sat_reg} EQL_REG {self.eql_reg} complete',
                 InitOwModel.BOUNDARY,
                 ''
                 f' OMP threads: {self.omp_threads}',
                 f' Linear solver: {self.linear_solver}',
                 f' Nonzeros in Jacobian: {self.nonzero_num}',
                 '',
                 f' Generated FE data for output ({self.fe_data_cost}ms)',
                 f' Writting reservoir grid info (geom file) costs {self.write_grid_cost}ms']

        return lines

if __name__ == '__main__':
    source_str = '''
----------------------------------------------------------------------
                         INIT OIL-WATER MODEL                         

 Building matrix costs 107.576ms
 Reservoir status INIT in SAT_REG 1 EQL_REG 1 complete
----------------------------------------------------------------------

 OMP threads: 1
 Linear solver: GMRES(30) with ILU1+AMG-3
 Nonzeros in Jacobian: 29928917

 Generated FE data for output (66.8161ms)
 Writting reservoir grid info (geom file) costs 21215ms
 Writing frame  1 to Tecplot binary file
'''
    init_ow_model = InitOwModel.from_block(source_str.split('\n'))

    block_ = init_ow_model.to_block()
    print('\n'.join(block_))
