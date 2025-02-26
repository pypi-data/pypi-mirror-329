from dataclasses import dataclass, field
from typing import Any, List, Optional


from mag_tools.utils.data.list_utils import ListUtils

from reservoir_info.bean.simulate.blk.blk_log import BlkLog

from reservoir_info.bean.simulate.comp.comp_log import CompLog
from reservoir_info.model.simulate_type import SimulateType


@dataclass
class SimulateLog:
    simulate_type: SimulateType = field(default=None, metadata={"description": "模拟方式"})
    uuid: Optional[str] = field(default=None, metadata={"description": "模拟标识"})
    computer_id: Optional[str] = field(default=None, metadata={"description": "计算机标识"})
    blk_log: Optional[BlkLog] = field(default=None, metadata={"description": "黑油模型日志"})
    comp_log: Optional[BlkLog] = field(default=None, metadata={"description": "组分模型日志"})

    def set_id(self, computer_id: str, uuid: str):
        self.computer_id = computer_id
        self.uuid = uuid

        if self.comp_log:
            self.comp_log.set_id(uuid)

    @classmethod
    def from_block(cls, block_lines):
        if ListUtils.find(block_lines, 'HiSimComp Version'):
            return CompLog.from_block(block_lines)
        else:
            return BlkLog.from_block(block_lines)

    def to_block(self) ->list[str]:
        if self.comp_log:
            return self.comp_log.to_block()
        elif self.blk_log:
            return self.blk_log.to_block()

if __name__ == '__main__':
    data_file = 'D:\\HiSimPack\\data\\comp.log'
    with open(data_file, 'r') as f:
        lines_ = [line.strip() for line in f.readlines()]
        log_ = SimulateLog.from_block(lines_)
        print('\n'.join(log_.to_block()))