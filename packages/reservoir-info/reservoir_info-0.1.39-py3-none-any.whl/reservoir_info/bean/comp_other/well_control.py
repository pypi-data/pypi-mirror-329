from typing import Optional

from reservoir_info.model.perforation_type import PerforationType
from reservoir_info.model.well_control_type import WellControlType
from reservoir_info.model.well_group_model import WellGroupModel
from reservoir_info.model.well_tatio_limit_type import WellRatioLimitType


class WellControl:
    def __init__(self, well_name: Optional[str] = None, control_type: Optional[WellControlType] = None,
                 target: Optional[float] = None, bhp_limit: Optional[float] = None,
                 limit_type: Optional[WellRatioLimitType] = None, threshold: Optional[float] = None,
                 multiplier: Optional[float] = None, wefac: Optional[float] = None,
                 bhp_min_max: Optional[float] = None, thp_min_max: Optional[float] = None,
                 vfp_no: Optional[str] = None, separator: Optional[str] = None, welldraw: Optional[float] = None,
                 group_control_model: Optional[str] = None,
                 perf_type: Optional[PerforationType] = None, os: Optional[int] = None, wi: Optional[float] = None,
                 tf: Optional[float] = None, hx: Optional[float] = None,
                 hy: Optional[float] = None, hz: Optional[float] = None, req: Optional[float] = None,
                 kh: Optional[float] = None, skin: Optional[float] = None,
                 wpimult: Optional[float] = None, icd_os: Optional[int] = None, stream: Optional[str] = None):
        """
        初始化 WellControl 井控制数据

        :param well_name: 井名称
        :param control_type: 控制类型
        :param target: 目标值
        :param bhp_limit: 井底压力限制
        :param limit_type: 比例限制类型
        :param threshold: 阈值
        :param multiplier: 乘数
        :param wefac: 有效工作时间比
        :param bhp_min_max: BHP 下限或上限
        :param thp_min_max: THP 下限或上限
        :param vfp_no: VFP 表编号
        :param separator: 分离器
        :param welldraw: 生产压差上限
        :param group_control_model: 井组控制模式
        :param perf_type: 射孔类型
        :param os: 射孔连接控制
        :param wi: 井指数
        :param tf: 传导率系数
        :param hx: Hx 参数
        :param hy: Hy 参数
        :param hz: Hz 参数
        :param req: 等效泄油半径
        :param kh: 地层产能系数
        :param skin: 表皮系数
        :param wpimult: 井指数缩放系数
        :param icd_os: 控流装置开关
        :param stream: 组分模型注气井气体的组分
        """
        self.well_name = well_name
        self.control_type = control_type
        self.target = target
        self.bhp_limit = bhp_limit
        self.limit_type = limit_type
        self.threshold = threshold
        self.multiplier = multiplier
        self.wefac = wefac

        if group_control_model == WellGroupModel.GROUPP:
            self.bhp_min = bhp_min_max if bhp_min_max is not None else 1.0135
            self.thp_min = thp_min_max
        elif group_control_model == WellGroupModel.GROUPI:
            self.bhp_max = bhp_min_max if bhp_min_max is not None else 1013.5
            self.thp_max = thp_min_max

        self.vfp_no = vfp_no
        self.separator = separator
        self.welldraw = welldraw

        if group_control_model is not None:
            self.group_control_model = group_control_model
        else:
            self.group_control_model = WellGroupModel.GROUPP if self.control_type.is_product() else WellGroupModel.GROUPI

        self.perf_type = perf_type
        self.os = os
        self.wi = wi
        self.tf = tf
        self.hx = hx
        self.hy = hy
        self.hz = hz
        self.req = req
        self.kh = kh
        self.skin = skin
        self.wpimult = wpimult
        self.icd_os = icd_os
        self.stream = stream

    @classmethod
    def from_text(cls, text: str):
        """
        从文本解析参数并创建 WellControl 对象

        :param text: 包含参数的文本
        :return: WellControl 对象
        """
        parts = text.split()
        well_name = parts[1].strip("'")
        control_type = WellControlType.of_code(parts[2])
        target = float(parts[3])
        bhp_limit = float(parts[4]) if len(parts) > 4 and parts[4].replace('.', '', 1).isdigit() else None
        limit_type = WellRatioLimitType[parts[6]] if len(parts) > 6 and 'LIMIT' in parts else None
        threshold = float(parts[7]) if len(parts) > 7 and 'LIMIT' in parts else None
        multiplier = float(parts[8]) if len(parts) > 8 and 'LIMIT' in parts else None
        wefac = float(parts[10]) if len(parts) > 10 and 'WEFAC' in parts else None

        bhp_min = float(parts[12]) if len(parts) > 12 and 'BHP' in parts else 1.0135
        bhp_max = float(parts[14]) if len(parts) > 14 and 'BHP' in parts else 1013.5

        thp_min = float(parts[16]) if len(parts) > 16 and 'THP' in parts else None
        thp_max = float(parts[18]) if len(parts) > 18 and 'THP' in parts else None

        vfp_table = parts[20] if len(parts) > 20 and 'VFP' in parts else None
        separator = parts[22] if len(parts) > 22 and 'SEP' in parts else None
        weldraw = float(parts[24]) if len(parts) > 24 and 'WELDRAW' in parts else None
        group_control_model = WellGroupModel[parts[26]] if len(parts) > 26 and (
                'GRUPP' in parts or 'GRUPI' in parts or 'FIXED' in parts) else None
        perf = parts[28] if len(parts) > 28 and 'PERF' in parts else None
        os = int(parts[30]) if len(parts) > 30 and 'OS' in parts else None
        wi = float(parts[32]) if len(parts) > 32 and 'WI' in parts else None
        tf = float(parts[34]) if len(parts) > 34 and 'TF' in parts else None
        hx = float(parts[36]) if len(parts) > 36 and 'HX' in parts else None
        hy = float(parts[38]) if len(parts) > 38 and 'HY' in parts else None
        hz = float(parts[40]) if len(parts) > 40 and 'HZ' in parts else None
        req = float(parts[42]) if len(parts) > 42 and 'REQ' in parts else None
        kh = float(parts[44]) if len(parts) > 44 and 'KH' in parts else None
        skin = float(parts[46]) if len(parts) > 46 and 'SKIN' in parts else None
        wpimult = float(parts[48]) if len(parts) > 48 and 'WPIMULT' in parts else None
        icd_os = int(parts[50]) if len(parts) > 50 and 'ICD_OS' in parts else None
        stream = parts[52] if len(parts) > 52 and 'STREAM' in parts else None

        bhp_min_max = bhp_min if group_control_model == WellGroupModel.GROUPP else bhp_max
        thp_min_max = thp_min if group_control_model == WellGroupModel.GROUPP else thp_max

        return cls(well_name, control_type, target, bhp_limit, limit_type, threshold, multiplier, wefac, bhp_min_max,
                   thp_min_max, vfp_table, separator, weldraw, group_control_model, perf, os, wi, tf, hx, hy,
                   hz, req, kh, skin, wpimult, icd_os, stream)

    def to_text(self) -> str:
        """
        将 WellControl 对象转换为文本

        :return: 包含参数的文本
        """
        parts = [f"WELL '{self.well_name}'", self.control_type.name, str(self.target)]
        if self.bhp_limit is not None:
            parts.append(str(self.bhp_limit))
        if self.limit_type is not None:
            parts.extend(["LIMIT", self.limit_type.name, str(self.threshold), str(self.multiplier)])
        if self.wefac is not None:
            parts.extend(["WEFAC", str(self.wefac)])
        if self.bhp_min is not None:
            parts.extend(["BHP", str(self.bhp_min)])
        if self.bhp_max is not None:
            parts.extend(["BHP", str(self.bhp_max)])
        if self.thp_min is not None:
            parts.extend(["THP", str(self.thp_min)])
        if self.thp_max is not None:
            parts.extend(["THP", str(self.thp_max)])
        if self.vfp_no is not None:
            parts.extend(["VFP", self.vfp_no])
        if self.separator is not None:
            parts.extend(["SEP", self.separator])
        if self.welldraw is not None:
            parts.extend(["WELDRAW", str(self.welldraw)])
        if self.group_control_model is not None:
            parts.append(self.group_control_model)
        if self.perf_type is not None:
            parts.extend(["PERF", self.perf_type])
        if self.os is not None:
            parts.extend(["OS", str(self.os)])
        if self.wi is not None:
            parts.extend(["WI", str(self.wi)])
        if self.tf is not None:
            parts.extend(["TF", str(self.tf)])
        if self.hx is not None:
            parts.extend(["HX", str(self.hx)])
        if self.hy is not None:
            parts.extend(["HY", str(self.hy)])
        if self.hz is not None:
            parts.extend(["HZ", str(self.hz)])
        if self.req is not None:
            parts.extend(["REQ", str(self.req)])
        if self.kh is not None:
            parts.extend(["KH", str(self.kh)])
        if self.skin is not None:
            parts.extend(["SKIN", str(self.skin)])
        if self.wpimult is not None:
            parts.extend(["WPIMULT", str(self.wpimult)])
        if self.icd_os is not None:
            parts.extend(["ICD_OS", str(self.icd_os)])
        if self.stream is not None:
            parts.extend(["STREAM", self.stream])
        return " ".join(parts)

    def __str__(self):
        return self.to_text()


if __name__ == '__main__':
    # 示例数据
    text1 = "WELL 'INJE1' WIR 5000 4000"
    text2 = "WELL 'W1' ORAT 50 14.7 LIMIT GLR 0.3 0.5 WEFAC 0.25 BHP 1.0135 BHP 1013.5 THP 2000 THP 3000 VFP 1 SEP SEP1 WELDRAW 100 GRUPP"
    text3 = """
 WELL 'INJECT*' GRUPI BHP 420"""
    well_control1 = WellControl.from_text(text1)
    well_control2 = WellControl.from_text(text2)
    well_control3 = WellControl.from_text(text3)

    print(well_control1)
    print(well_control2)
    print(well_control3)
