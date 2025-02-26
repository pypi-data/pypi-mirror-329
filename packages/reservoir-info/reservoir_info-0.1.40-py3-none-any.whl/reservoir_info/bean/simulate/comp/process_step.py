from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ProcessStep:
    nr_step: Optional[int] = field(init=False, default=0, metadata={'description': '迭代步数'})
    max_mbe: float = field(init=False, default=0, metadata={'description': '最大均方误差'})
    avg_mbe: float = field(init=False, default=0, metadata={'description': '平均均方误差'})
    msw_mbe: float = field(init=False, default=0, metadata={'description': 'MSW均方误差'})
    lin_itr: Optional[int] = field(init=False, default=0, metadata={'description': '线性求解次数'})

    @classmethod
    def from_text(cls, text: str):
        step = cls()

        items = [item.strip() for item in text.strip().split(' ') if item.strip() != '']
        step.nr_step = int(items[0])
        step.max_mbe = float(items[1])
        step.avg_mbe = float(items[2])
        step.msw_mbe = float(items[3])
        step.lin_itr = int(items[4])

        return step

    def to_text(self) -> str:
        return f'      {self.nr_step}          {self.max_mbe}     {self.avg_mbe}   {self.msw_mbe}         {self.lin_itr}'
