from dataclasses import dataclass, field
from typing import Optional

from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.string_utils import StringUtils


@dataclass
class OmpThread:
    uuid: Optional[str] = field(default=None, metadata={"description": "模拟标识"})
    omp_threads: Optional[int] = field(init=False, default=None, metadata={'description': 'OMP线程数'})
    linear_solver: Optional[str] = field(init=False, default=None, metadata={'description': '线性处理器'})
    nonzero_num: Optional[str] = field(init=False, default=None, metadata={'description': '雅可比矩阵非零个数'})
    fe_data_cost: Optional[str] = field(init=False, default=None, metadata={'description': '产生FE数据花费时间，单位：毫秒'})
    write_grid_cost: Optional[str] = field(init=False, default=None, metadata={'description': '写油藏网络信息花费时间，单位：毫秒'})

    @classmethod
    def from_block(cls, block_lines: list[str]):
        init_model = cls()

        if len(block_lines) > 4:
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
        lines = [f' OMP threads: {self.omp_threads}',
                 f' Linear solver: {self.linear_solver}',
                 f' Nonzeros in Jacobian: {self.nonzero_num}',
                 '',
                 f' Generated FE data for output ({self.fe_data_cost}ms)',
                 f' Writting reservoir grid info (geom file) costs {self.write_grid_cost}ms']

        return lines

if __name__ == '__main__':
    source_str = '''
 OMP threads: 1
 Linear solver: GMRES(30) with ILU1+AMG-3
 Nonzeros in Jacobian: 29928917

 Generated FE data for output (66.8161ms)
 Writting reservoir grid info (geom file) costs 21215ms
'''
    omp_thread = OmpThread.from_block(source_str.split('\n'))

    block_ = omp_thread.to_block()
    print('\n'.join(block_))
