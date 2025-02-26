from dataclasses import dataclass, field
from typing import Optional

from mag_tools.bean.common.base_data import BaseData

from reservoir_info.model.simulate_type import SimulateType


@dataclass
class RealtimeLog(BaseData):
    simulate_id: str = field(default=None, metadata={"description": "模拟标识"})
    simulate_type: SimulateType = field(default=None, metadata={"description": "模拟方式"})
    case_file: int = field(default=None, metadata={"description": "用户序号"})
    message: str = field(default=None, metadata={"description": "日志消息"})
    user_sn: Optional[int] = field(default=None, metadata={"description": "用户序号"})
