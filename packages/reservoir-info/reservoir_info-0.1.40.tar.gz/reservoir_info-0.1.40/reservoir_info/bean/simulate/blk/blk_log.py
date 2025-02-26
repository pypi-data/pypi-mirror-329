from dataclasses import dataclass, field
from typing import List

from mag_tools.bean.common.base_data import BaseData
from mag_tools.utils.data.list_utils import ListUtils

from reservoir_info.bean.simulate.blk.stage_blk import StageBlk


@dataclass
class BlkLog(BaseData):
    stages: List[StageBlk] = field(init=False, default_factory=list, metadata={'description': '模拟阶段列表'})

    @classmethod
    def from_block(cls, block_lines):
        log = cls()

        stages_lines = ListUtils.pick_tail(block_lines, '---  TIME =')
        if len(stages_lines) >= 10:
            stage_blocks = ListUtils.split_by_keyword(stages_lines, '')
            for stage_block in stage_blocks:
                stage = StageBlk.from_block(stage_block)
                log.stages.append(stage)

        return log

    def to_block(self) ->list[str]:
        lines = list()
        for stage in self.stages:
            lines.extend(stage.to_block())
            lines.append('')
        return lines

if __name__ == '__main__':
    data_file = 'D:\\HiSimPack\\data\\blk.log'
    with open(data_file, 'r') as f:
        lines_ = [line.strip() for line in f.readlines()]
        log_ = BlkLog.from_block(lines_)
        print('\n'.join(log_.to_block()))