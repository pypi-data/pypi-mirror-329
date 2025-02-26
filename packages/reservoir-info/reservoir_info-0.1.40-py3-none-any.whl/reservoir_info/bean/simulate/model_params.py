from dataclasses import dataclass, field
from typing import Optional

from reservoir_info.bean.well.template import Template
from reservoir_info.bean.solution.solution import Solution
from reservoir_info.bean.props.props import Props
from reservoir_info.bean.common.dimension import Dimension
from reservoir_info.model.model_type import ModelType
from reservoir_info.model.unit_type import UnitType

@dataclass
class ModelParams:
    uuid: Optional[str] = field(default=None, metadata={"description": "模拟标识"})
    console_path: Optional[str] = field(init=False, default=None, metadata={'description': '执行程序路径'})
    case_file: Optional[str] = field(init=False, default=None, metadata={'description': '模型方案文件'})
    unit_type: Optional[UnitType] = field(init=False, default=None, metadata={'description': '单位制'})
    model_type: Optional[ModelType] = field(init=False, default=None, metadata={'description': '模型类型'})
    dimens: Optional[Dimension] = field(init=False, default=None, metadata={'description': '油藏网格数'})
    nx: Optional[int] = field(init=False, default=None, metadata={'description': '顶面深度行数'})
    ny: Optional[int] = field(init=False, default=None, metadata={'description': '顶面深度列数'})
    template: Optional[Template] = field(init=False, default=None, metadata={'description': '参数模板'})
    props: Optional[Props] = field(init=False, default=None, metadata={'description': '组分数量'})
    solution: Optional[Solution] = field(init=False, default=None, metadata={'description': '解决方案'})

    @classmethod
    def from_block(cls, block_lines):
        pass

    def to_block(self):
        pass