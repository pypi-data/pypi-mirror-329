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
from reservoir_info.bean.simulate.comp.model_params import ModelParams
from reservoir_info.bean.simulate.comp.omp_thread import OmpThread
from reservoir_info.bean.simulate.comp.performance_statistics import PerformanceStatistics
from reservoir_info.bean.simulate.comp.primary_params import PrimaryParams
from reservoir_info.bean.simulate.stage import Stage


@dataclass
class CompLog:
    BOUNDARY = '----------------------------------------------------------------------'
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
    stages: List[Stage] = field(init=False, default_factory=list, metadata={'description': '模拟阶段列表'})
    performance_statistics: Optional[PerformanceStatistics] = field(init=False, default=None, metadata={'description': '性能统计信息'})

    @property
    def simulate_params(self) -> dict[str, Any]:
        params_map = {'model_params': JsonParser.from_bean(self.model_params)}
        params_map.update(self.primary_params.to_block())

        return params_map

    def set_id(self, uuid: str):
        if self.model_params:
            self.model_params.uuid = uuid
        if self.primary_params:
            self.primary_params.uuid = uuid
        if self.init_model:
            self.init_model.uuid = uuid
        if self.performance_statistics:
            self.performance_statistics.uuid = uuid

        for stage in self.stages:
            stage.uuid = uuid

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
        head_block = ListUtils.pick_block(block_lines, CompLog.BOUNDARY, 'Simulation starts at:')
        log.__from_head_block(head_block)

        # 解析参数
        params_block = ListUtils.pick_block(block_lines, 'MODELTYPE', '')
        log.model_params = ModelParams.from_block(params_block)

        # 解析预处理
        pre_processing_block = ListUtils.pick_block(block_lines, 'PRE-PROCESSING', CompLog.BOUNDARY)
        log.primary_params = PrimaryParams.from_block(pre_processing_block)

        # 解析初始化
        init_model_block = ListUtils.pick_block(block_lines, 'INIT ', CompLog.BOUNDARY)
        log.init_model = InitModel.from_block(init_model_block)

        # 解析OMP块
        omp_thread_block = ListUtils.pick_block(block_lines, 'OMP threads', 'Writting reservoir grid info')
        log.omp_thread = OmpThread.from_block(omp_thread_block)

        # 解析模拟步骤数据块
        stages_lines = ListUtils.pick_block(block_lines, 'Percent', 'Tecplot stream is closed with returned value')
        if len(stages_lines) >= 10:
            stages_lines.pop()  # 去掉最后两行
            stages_lines.pop()
            stages_lines = ListUtils.remove_keyword(stages_lines, 'Writing frame')  # 移除‘Writing frame ’信息行

            stages_str = '\n'.join(stages_lines).replace('\n\n\n', '\n\n').strip()
            stages_lines = stages_str.split('\n')

            stage_blocks = ListUtils.split_by_keyword(stages_lines, '')
            for stage_block in stage_blocks:
                stage = Stage.from_block(stage_block)
                log.stages.append(stage)

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

        for stage in self.stages:
            lines.extend(stage.to_block())
            lines.append('')

        lines.extend(self.performance_statistics.to_block())
        lines.append(f"-- Simulation of case '{self.case_file}' complete --")

        return lines

    def __from_head_block(self, head_block_lines):
        if len(head_block_lines) > 5:
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

    def __to_head_block(self) -> list[str]:
        if self.case_file is None:
            return []

        return [CompLog.BOUNDARY,
                 StringFormat.pad_value(f'HiSimComp Version {self.version}, {self.bits}bit', len(CompLog.BOUNDARY), JustifyType.CENTER),
                 StringFormat.pad_value(f'Compiled on {self.compile_date}', len(CompLog.BOUNDARY), JustifyType.CENTER),
                 StringFormat.pad_value(f'by {self.corp_name}', len(CompLog.BOUNDARY), JustifyType.CENTER),
                 CompLog.BOUNDARY,
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
        log_ = CompLog.from_block(lines_)
        print('\n'.join(log_.to_block()))