from dataclasses import dataclass, field
from typing import List, Optional

from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.string_utils import StringUtils

from reservoir_info.bean.simulate.comp.process_step import ProcessStep

@dataclass
class StageComp:
    uuid: Optional[str] = field(default=None, metadata={"description": "模拟标识"})
    t_step: int = field(init=False, default=0, metadata={'description': '时间序号'})
    percent: float = field(init=False, default=0, metadata={'description': '当前阶段的完成率'})
    time: float = field(init=False, default=0, metadata={'description': '当前阶段的时间，单位：天'})
    dt: float = field(init=False, default=0, metadata={'description': '时间步长，单位：天'})
    dp: float = field(init=False, default=0, metadata={'description': '时间步目标压力变化'})
    ds: float = field(init=False, default=0, metadata={'description': '时间步目标饱和度变化量'})
    dc: float = field(init=False, default=0, metadata={'description': '时间步目标溶解气油比、挥发油气比'})
    cfl: float = field(init=False, default=0, metadata={'description': '时间步收敛难易度'})
    steps: List[ProcessStep] = field(init=False, default_factory=list, metadata={'description': '当前阶段的迭代步骤'})
    max_mbe_of_stage: float = field(init=False, default=0, metadata={'description': '当前阶段的最大均方误差'})
    avg_mbe_of_stage: float = field(init=False, default=0, metadata={'description': '当前阶段的平均均方误差'})
    msw_mbe_of_stage: float = field(init=False, default=0, metadata={'description': '当前阶段的MSW均方误差'})

    @classmethod
    def from_block(cls, block_lines):
        stage = cls()

        if len(block_lines) >= 4:
            block_lines = ListUtils.trim(block_lines)

            first_lin_values = StringUtils.pick_numbers(block_lines[0])
            stage.percent = first_lin_values[0]/100
            stage.time = first_lin_values[1]
            stage.dt = first_lin_values[2]
            stage.t_step = first_lin_values[3]

            end_map = {k: v for k, v in (item.split('=') for item in block_lines[-1].strip().split(' '))}
            stage.dp = StringUtils.to_value(end_map['DP'], float)
            stage.ds = StringUtils.to_value(end_map['DS'], float)
            stage.dc = StringUtils.to_value(end_map['DC'], float)
            stage.cfl = StringUtils.to_value(end_map['CFL'], float)

            second_to_last = [item.strip() for item in block_lines[-2].strip().split(' ') if item.strip() != '']
            stage.max_mbe_of_stage = StringUtils.to_value(second_to_last[0], float)
            stage.avg_mbe_of_stage = StringUtils.to_value(second_to_last[1], float)
            stage.msw_mbe_of_stage = StringUtils.to_value(second_to_last[2], float)

            block_lines = block_lines[2:-2]
            for line in block_lines:
                step = ProcessStep.from_text(line)
                stage.steps.append(step)

        return stage

    def to_block(self):
        lines = [f' Percent   {self.percent * 100}%  Time {self.time} DAY  DT {self.dt} DAY  TStep {self.t_step}',
                 ' NRStep        MAXMBE        AVGMBE        MSWMBE   Lin_itr']

        for step in self.steps:
            lines.append(step.to_text())

        lines.append(f'                  {self.max_mbe_of_stage}     {self.avg_mbe_of_stage}   {self.msw_mbe_of_stage}')
        lines.append(f' DP={self.dp} DS={self.ds} DC={self.dc} CFL={self.cfl}')

        return lines

if __name__ == '__main__':
    stage_src = '''
 Percent   0.15%  Time 3 DAY  DT 0.7 DAY  TStep 14
 NRStep        MAXMBE        AVGMBE        MSWMBE   Lin_itr
     61      0.493904   0.000893267   0.000413943         8
     62       3.23041    0.00028123    0.00260284         7
     63      0.718315   3.05874e-05   1.05274e-05         6
     64      0.648658   1.46931e-06   3.41263e-07         6
     65     0.0176386   6.34713e-08    5.2575e-08         5
     66    0.00248242   1.21076e-08   9.09077e-09         5
           0.00130985   5.09723e-09   1.50634e-09
 DP=274.738 DS=0.099191 DC=0 CFL=220.947    
    '''

    stage_ = StageComp.from_block(stage_src.split('\n'))
    print('\n'.join(stage_.to_block()))