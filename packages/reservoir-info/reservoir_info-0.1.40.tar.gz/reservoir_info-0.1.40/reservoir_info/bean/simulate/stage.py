from typing import Optional

from dataclasses import dataclass, field
from mag_tools.bean.common.base_data import BaseData
from mag_tools.utils.data.list_utils import ListUtils

from reservoir_info.bean.simulate.blk.stage_blk import StageBlk
from reservoir_info.bean.simulate.comp.stage_comp import StageComp

@dataclass
class Stage(BaseData):
    stage_blk: Optional[StageBlk]= field(default=None, metadata={"description": "黑油模型"})
    stage_comp: Optional[StageComp] = field(default=None, metadata={"description": "组分模型"})

    @classmethod
    def from_block(cls, block_lines):
        stage = cls()

        # 组分模型
        ListUtils.trim(block_lines)
        if len(block_lines) >= 4:
            stage.stage_comp = StageComp.from_block(block_lines)
        elif len(block_lines) >= 3:
            stage.stage_blk = StageBlk.from_block(block_lines)

        return stage

    def to_block(self) -> list[str]:
        if self.stage_blk:
            return self.stage_blk.to_block()
        elif self.stage_comp:
            return self.stage_comp.to_block()

if __name__ == '__main__':
    str_blk = '''
    ---  TIME =      2.000 DAYS
      TIMESTEP =      1.000 DAYS           2 NEWTON ITERATIONS
      MATERIAL BALANCES : OIL  1.00  WATER 10.00  GAS  1.00'''
    blk = Stage.from_block(str_blk.split('\n'))
    print('\n'.join(blk.to_block()))

    str_comp = '''
    Percent   0.15%  Time 3 DAY  DT 0.7 DAY  TStep 14
    NRStep        MAXMBE        AVGMBE        MSWMBE   Lin_itr
        61      0.493904   0.000893267   0.000413943         8
        62       3.23041    0.00028123    0.00260284         7
        63      0.718315   3.05874e-05   1.05274e-05         6
        64      0.648658   1.46931e-06   3.41263e-07         6
        65     0.0176386   6.34713e-08    5.2575e-08         5
        66    0.00248242   1.21076e-08   9.09077e-09         5
              0.00130985   5.09723e-09   1.50634e-09
    DP=274.738 DS=0.099191 DC=0 CFL=220.947'''

    comp = StageComp.from_block(str_comp.split('\n'))
    print('\n'.join(comp.to_block()))
