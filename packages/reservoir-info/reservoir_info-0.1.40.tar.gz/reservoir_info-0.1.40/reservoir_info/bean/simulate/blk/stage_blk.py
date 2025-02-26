from dataclasses import dataclass, field

from mag_tools.bean.base_data import BaseData
from mag_tools.utils.data.string_utils import StringUtils
from mag_tools.utils.data.list_utils import ListUtils


@dataclass
class StageBlk(BaseData):
    time: float = field(default=None, metadata={"description": "时间"})
    timestep: float = field(default=None, metadata={"description": "时间步长"})
    interation: int = field(default=None, metadata={"description": "牛顿迭代次数"})
    oil: float = field(default=None, metadata={"description": "油压"})
    water: float = field(default=None, metadata={"description": "水压"})
    gas: float = field(default=None, metadata={"description": "气压"})

    @classmethod
    def from_block(cls, block_lines):
        stage = cls()
        time_line = ListUtils.pick_line(block_lines, 'TIME =')
        stage.time = StringUtils.pick_number(time_line)

        timestep_line = ListUtils.pick_line(block_lines, 'TIMESTEP =')
        numbers = StringUtils.pick_numbers(timestep_line)
        stage.timestep = numbers[0]
        stage.interation = numbers[1]

        balance_line = ListUtils.pick_line(block_lines, 'MATERIAL BALANCE')
        numbers = StringUtils.pick_numbers(balance_line)
        stage.oil = numbers[0]
        stage.water = numbers[1]
        stage.gas = numbers[2]

        return stage

    def to_block(self) -> list[str]:
        lines = list()
        lines.append(f'---  TIME =      {self.time} DAYS')
        lines.append(f'      TIMESTEP =      {self.timestep} DAYS           {self.interation} NEWTON ITERATIONS')
        lines.append(f'      MATERIAL BALANCES : OIL  {self.oil}  WATER  {self.water}  GAS  {self.gas}')

        return lines

if __name__ == '__main__':
    str_ = """
---  TIME =      2.000 DAYS
  TIMESTEP =      1.000 DAYS           2 NEWTON ITERATIONS
  MATERIAL BALANCES : OIL  1.00  WATER 10.00  GAS  1.00"""

    stage_ = StageBlk.from_block(str_.split('\n'))
    print("\n".join(stage_.to_block()))