from typing import Optional

class CompleteWellData:
    def __init__(self, open_shut: Optional[str] = None, os: Optional[int] = None, wi: Optional[float] = None, tf: Optional[float] = None,
                 hx: Optional[float] = None, hy: Optional[float] = None, hz: Optional[float] = None, req: Optional[float] = None,
                 kh: Optional[float] = None, skin: Optional[float] = None, wpimult: Optional[float] = None, icd_os: Optional[int] = None):
        """
        初始化 CompleteWellData 对象

        :param open_shut: 控制射孔开/关
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
        """
        self.open_shut = open_shut
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

    def __str__(self):
        return f"CompleteWellData(open_shut={self.open_shut}, os={self.os}, wi={self.wi}, tf={self.tf}, hx={self.hx}, hy={self.hy}, hz={self.hz}, req={self.req}, kh={self.kh}, skin={self.skin}, wpimult={self.wpimult}, icd_os={self.icd_os})"

if __name__ == '__main__':
    # 示例数据
    well_data = CompleteWellData(open_shut="OPEN", os=7, wi=10.0, tf=20.0, hx=5.0, hy=5.0, hz=5.0, req=1.0, kh=100.0, skin=0.1, wpimult=0.5, icd_os=1)
    print(well_data)
