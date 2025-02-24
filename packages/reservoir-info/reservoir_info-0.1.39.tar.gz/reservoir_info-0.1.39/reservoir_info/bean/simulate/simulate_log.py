import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, List, Optional

from mag_tools.jsonparser.json_parser import JsonParser
from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.date_utils import DateUtils
from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.string_format import StringFormat
from mag_tools.utils.data.string_utils import StringUtils

from reservoir_info.bean.simulate.init_model.init_model import InitModel
from reservoir_info.bean.simulate.model_params import ModelParams
from reservoir_info.bean.simulate.omp_thread import OmpThread
from reservoir_info.bean.simulate.performance_statistics import PerformanceStatistics
from reservoir_info.bean.simulate.primary_params import PrimaryParams
from reservoir_info.bean.simulate.process_stage import ProcessStage
from reservoir_info.model.simulate_type import SimulateType


@dataclass
class SimulateLog:
    BOUNDARY = '----------------------------------------------------------------------'
    simulate_type: SimulateType = field(default=None, metadata={"description": "模拟方式"})
    uuid: Optional[str] = field(default=None, metadata={"description": "模拟标识"})
    computer_id: Optional[str] = field(default=None, metadata={"description": "计算机标识"})
    version: str = field(init=False, default=2023.1, metadata={'description': '程序版本'})
    bits: str = field(init=False, default=2023.1, metadata={'description': '程序位数'})
    compile_date: str = field(init=False, default='Oct 16 2024', metadata={'description': '编译日期'})
    corp_name: str = field(init=False, default='Ennosoft company of China', metadata={'description': '公司名称'})
    case_file: Optional[str] = field(default=None, metadata={"description": "模型方案文件"})
    console_path: Optional[str] = field(default=None, metadata={"description": "模型模拟程序"})
    start_time: Optional[datetime] = field(default=None, metadata={"description": "模型模拟开始时间"})
    #
    model_params: Optional[ModelParams] = field(init=False, default=None, metadata={'description': '模型参数'})
    primary_params: Optional[PrimaryParams] = field(init=False, default=None, metadata={'description': '预处理信息'})
    init_model: Optional[InitModel] = field(init=False, default=None, metadata={'description': '初始化模型'})
    omp_thread: Optional[OmpThread] = field(init=False, default=None, metadata={'description': 'OMP线程等信息'})
    process_stages: List[ProcessStage] = field(init=False, default_factory=list, metadata={'description': '模拟阶段列表'})
    performance_statistics: Optional[PerformanceStatistics] = field(init=False, default=None, metadata={'description': '性能统计信息'})

    @property
    def simulate_params(self) -> dict[str, Any]:
        params_map = {'model_params': JsonParser.from_bean(self.model_params)}
        params_map.update(self.primary_params.to_block())

        return params_map

    def set_id(self, computer_id: str, uuid: str):
        self.computer_id = computer_id

        self.uuid = uuid
        if self.model_params:
            self.model_params.uuid = uuid
        if self.primary_params:
            self.primary_params.uuid = uuid
        if self.init_model:
            self.init_model.uuid = uuid
        if self.performance_statistics:
            self.performance_statistics.uuid = uuid

        for process_stage in self.process_stages:
            process_stage.uuid = uuid

    @classmethod
    def from_block(cls, block_lines):
        log = cls()

        # 清除消息
        block_lines = ListUtils.remove_keyword(block_lines, 'Writing frame')
        block_lines = ListUtils.remove_keyword(block_lines, 'Message:')

        block_lines = ListUtils.pick_tail(block_lines, '--')
        if len(block_lines) == 0:
            return log

        # 解析标题
        head_block = ListUtils.pick_block(block_lines, SimulateLog.BOUNDARY, 'Simulation starts at:')
        log.__from_head_block(head_block)

        # 解析参数
        params_block = ListUtils.pick_block(block_lines, 'MODELTYPE', '')
        log.model_params = ModelParams.from_block(params_block)

        # 解析预处理
        pre_processing_block = ListUtils.pick_block(block_lines, 'PRE-PROCESSING', SimulateLog.BOUNDARY)
        log.primary_params = PrimaryParams.from_block(pre_processing_block)

        # 解析初始化
        init_model_block = ListUtils.pick_block(block_lines, 'INIT ', SimulateLog.BOUNDARY)
        log.init_model = InitModel.from_block(init_model_block)

        # 解析OMP块
        omp_thread_block = ListUtils.pick_block(block_lines, 'OMP threads', 'Writting reservoir grid info')
        log.omp_thread = OmpThread.from_block(omp_thread_block)

        # 解析模拟步骤数据块
        process_stages_lines = ListUtils.pick_block(block_lines, 'Percent', 'Tecplot stream is closed with returned value')
        if len(process_stages_lines) >= 10:
            process_stages_lines.pop()  # 去掉最后两行
            process_stages_lines.pop()
            process_stages_lines = ListUtils.remove_keyword(process_stages_lines, 'Writing frame')  # 移除‘Writing frame ’信息行

            process_stages_str = '\n'.join(process_stages_lines).replace('\n\n\n', '\n\n').strip()
            process_stages_lines = process_stages_str.split('\n')

            process_stage_blocks = ListUtils.split_by_keyword(process_stages_lines, '')
            for stage_blocks in process_stage_blocks:
                process_stage = ProcessStage.from_block(stage_blocks)
                log.process_stages.append(process_stage)

        performance_statistics_block = ListUtils.pick_tail(block_lines, '-------------------- Performance Statistics --------------------------')
        log.performance_statistics = PerformanceStatistics.from_block(performance_statistics_block)

        return log

    def to_block(self) ->list[str]:
        lines = list()
        lines.extend(self.__to_head_block())
        lines.append('')
        # 添加参数块，待补充
        lines.extend(self.primary_params.to_block())
        lines.extend(self.init_model.to_block())

        for process_stage in self.process_stages:
            lines.extend(process_stage.to_block())
            lines.append('')

        lines.extend(self.performance_statistics.to_block())
        lines.append(f"-- Simulation of case '{self.case_file}' complete --")

        return lines

    def __from_head_block(self, head_block_lines):
        block_lines = [line.strip() for line in head_block_lines if len(line.strip()) > 0 and '--' not in line]
        version_nums = StringUtils.pick_numbers(block_lines[0])
        self.version = str(version_nums[0])
        self.bits = str(version_nums[1])
        self.compile_date = StringUtils.pick_tail(block_lines[1], 'on').strip()
        self.corp_name = StringUtils.pick_tail(block_lines[2], 'by').strip()

        block_lines = ListUtils.pick_tail(block_lines, 'Console path')
        block_lines = ListUtils.remove_keyword(block_lines, 'Message:')
        block_str = ';'.join(block_lines).replace(':;', '=').replace(': ', '=')
        block_map = dict(item.split('=') for item in block_str.split(';'))
        block_map = {k.strip(): v.strip() for k,v in block_map.items()}
        self.console_path = block_map['Console path']
        self.case_file = block_map['Case file']
        self.start_time = DateUtils.to_datetime(block_map['Simulation starts at'])

    def __to_head_block(self):
        return [SimulateLog.BOUNDARY,
                 StringFormat.pad_value(f'HiSimComp Version {self.version}, {self.bits}bit', len(SimulateLog.BOUNDARY), JustifyType.CENTER),
                 StringFormat.pad_value(f'Compiled on {self.compile_date}', len(SimulateLog.BOUNDARY), JustifyType.CENTER),
                 StringFormat.pad_value(f'by {self.corp_name}', len(SimulateLog.BOUNDARY), JustifyType.CENTER),
                 SimulateLog.BOUNDARY,
                 '',
                 ' Console path:',
                 self.console_path,
                 ' Case file:',
                 self.case_file,
                 f" Simulation starts at: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}"]

if __name__ == '__main__':
    data_file = 'D:\\HiSimPack\\data\\comp.log'
    with open(data_file, 'r') as f:
        lines_ = [line.strip() for line in f.readlines()]
        log_ = SimulateLog.from_block(lines_)
        print('\n'.join(log_.to_block()))