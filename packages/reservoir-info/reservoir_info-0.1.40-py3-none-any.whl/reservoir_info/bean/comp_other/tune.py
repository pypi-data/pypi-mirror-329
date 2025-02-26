from datetime import datetime
from typing import Optional, List

class Tune:
    def __init__(self, tstart: Optional[datetime] = None, tend: Optional[datetime] = None, maxitr: Optional[int] = 10,
                 stepcut: Optional[float] = 1.0, mindt: Optional[float] = 0.1, maxdt: Optional[float] = 31.0, dtinc: Optional[float] = 2.0,
                 dtcut: Optional[float] = 0.5, checkdx: Optional[bool] = False, maxdp: Optional[float] = 200.0, maxds: Optional[float] = 0.0,
                 maxdc: Optional[float] = 0.0, mbepc: Optional[float] = 1e-4, mbeavg: Optional[float] = 1e-6, solver: Optional[int] = 1034,
                 inistol: Optional[int] = 1, amgset: Optional[int] = 1, wsol: Optional[int] = 0):
        """
        时间步控制，求解器选择，收敛判据
        格式：字符串+数据，参数没有先后顺序

        :param tstart: 开始时间
        :param tend: 结束时间
        :param maxitr: 最大迭代次数
        :param stepcut: 步长缩减
        :param mindt: 最小时间步长
        :param maxdt: 最大时间步长
        :param dtinc: 时间步长增加
        :param dtcut: 时间步长减少
        :param checkdx: 是否检查 dx
        :param maxdp: 最大 dp
        :param maxds: 最大 ds
        :param maxdc: 最大 dc
        :param mbepc: 最大误差百分比
        :param mbeavg: 平均误差
        :param solver: 求解器
        :param inistol: 初始容差
        :param amgset: AMG 设置
        :param wsol: Wsol 设置
        """
        self.tstart = tstart
        self.tend = tend
        self.maxitr = maxitr
        self.stepcut = stepcut
        self.mindt = mindt
        self.maxdt = maxdt
        self.dtinc = dtinc
        self.dtcut = dtcut
        self.checkdx = checkdx
        self.maxdp = maxdp
        self.maxds = maxds
        self.maxdc = maxdc
        self.mbepc = mbepc
        self.mbeavg = mbeavg
        self.solver = solver
        self.inistol = inistol
        self.amgset = amgset
        self.wsol = wsol

    @classmethod
    def from_block(cls, block_lines: str):
        """
        从块字符串中解析参数并创建 Tune 对象

        :param block_lines: 包含参数的块字符串
        :return: Tune 对象
        """
        params = block_lines.split()
        kwargs = {}
        i = 0
        while i < len(params):
            if params[i] == 'TSTART':
                kwargs['tstart'] = datetime.strptime(params[i+1], '%Y-%m-%d')
                i += 2
            elif params[i] in ['MINDT', 'MAXDT', 'DTINC', 'DTCUT', 'MAXDP', 'MAXDS', 'MAXDC', 'MBEPC', 'MBEAVG']:
                kwargs[params[i].lower()] = float(params[i+1])
                i += 2
            elif params[i] == 'CHECKDX':
                kwargs['checkdx'] = True
                i += 1
            elif params[i] == 'SOLVER':
                kwargs['solver'] = int(params[i+1])
                i += 2
            else:
                i += 1
        return cls(**kwargs)

    def to_block(self) -> List[str]:
        """
        将 Tune 对象转换为块字符串列表

        :return: 包含参数的块字符串列表
        """
        block_lines = [
            "TUNE",
            f"TSTART {self.tstart.strftime('%Y-%m-%d') if self.tstart else ''}",
            f"MINDT {self.mindt} MAXDT {self.maxdt} DTINC {self.dtinc} DTCUT {self.dtcut} CHECKDX" if self.checkdx else "",
            f"MAXDP {self.maxdp} MAXDS {self.maxds} MAXDC {self.maxdc} MBEPC {self.mbepc} MBEAVG {self.mbeavg}",
            f"SOLVER {self.solver}"
        ]
        return block_lines

    def __str__(self):
        return '\n'.join(self.to_block())

if __name__ == '__main__':
    # 示例数据
    _block_lines = """
    TUNE
    TSTART  1990-01-01 
    MINDT  0.1  MAXDT  31  DTINC  2.0  DTCUT  0.5  CHECKDX  
    MAXDP  200  MAXDS  0  MAXDC  0  MBEPC  1E-4  MBEAVG  1E-6   
    SOLVER  1034
    """
    _tune = Tune.from_block(_block_lines)

    print(_tune)
