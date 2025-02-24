from mag_tools.utils.common.array_utils import ArrayUtils


class CopyGrid:
    def __init__(self, source_name, target_name, i1, i2, j1, j2, k1, k2, min_val=float('-inf'), max_val=float('inf'), c=1.0, d=0.0):
        self.source_name = source_name  # 源数组 A 的名字
        self.target_name = target_name  # 目标数组 B 的名字
        self.i1 = i1
        self.i2 = i2
        self.j1 = j1
        self.j2 = j2
        self.k1 = k1
        self.k2 = k2
        self.min_val = min_val  # 最小值
        self.max_val = max_val  # 最大值
        self.c = c  # 缩放因子
        self.d = d  # 增加值

    @classmethod
    def from_text(cls, text):
        items = text.split()
        source = items[1]
        target = items[2]
        i1 = int(items[3])
        i2 = int(items[4])
        j1 = int(items[5])
        j2 = int(items[6])
        k1 = int(items[7])
        k2 = int(items[8])
        min_val = float(items[9]) if len(items) > 9 and items[9] != 'NA' else float('-inf')
        max_val = float(items[10]) if len(items) > 10 and items[10] != 'NA' else float('inf')
        c = float(items[11]) if len(items) > 11 else 1.0
        d = float(items[12]) if len(items) > 12 else 0.0

        return cls(source, target, i1, i2, j1, j2, k1, k2, min_val, max_val, c, d)

    def to_text(self):
        min_val_str = 'NA' if self.min_val == float('-inf') else str(self.min_val)
        max_val_str = 'NA' if self.max_val == float('inf') else str(self.max_val)

        line = f"COPY {self.source_name} {self.target_name} {self.i1} {self.i2} {self.j1} {self.j2} {self.k1} {self.k2}"
        if self.min_val != float('-inf') or self.max_val != float('inf') or self.c != 1.0 or self.d != 0.0:
            line += f" {min_val_str} {max_val_str} {self.c} {self.d}"

        return line

    def calculate(self, grid):
        source_array = grid.get_array(self.source_name)
        target_array = grid.get_array(self.target_name)

        ArrayUtils.copy_array_3d(source_array, target_array, self.k1-1, self.k2-1, self.i1-1, self.i2-1, self.j1-1, self.j2-1)
        grid.set_array(self.target_name, target_array)