
from mag_tools.utils.data.array_utils import ArrayUtils
from mag_tools.utils.data.string_utils import StringUtils


class Box:
    def __init__(self, var_name, i1, i2, j1, j2, k1, k2, operator, value):
        """
        :param var_name: 变量名
        :param i1: 网络行数1
        :param i2: 网络行数2
        :param j1: 网络列数1
        :param j2: 网络列数2
        :param k1: 网络层数1
        :param k2: 网络层数2
        :param operator: 运算符
        :param value: 数值
        """
        self.var_name = var_name    # 变量名
        self.i1 = i1
        self.i2 = i2
        self.j1 = j1
        self.j2 = j2
        self.k1 = k1
        self.k2 = k2
        self.operator = operator    # 操作符（'='，'+'或'*'）
        self.value = value          # 值

    @classmethod
    def from_text(cls, text):
        """
        从文本中得到Box
        :param text: 文本，如：BOX TOPS   1  1  1 25  1  1  '='  9000.00
        :return: Box
        """
        items = text.split()
        var_name = items[1]
        i1 = int(items[2])
        i2 = int(items[3])
        j1 = int(items[4])
        j2 = int(items[5])
        k1 = int(items[6])
        k2 = int(items[7])
        operator = items[8].replace("'", "")
        value = StringUtils.to_value(items[9], float)
        return cls(var_name, i1, i2, j1, j2, k1, k2, operator, value)

    def to_text(self):
        return f"BOX {self.var_name} {self.i1} {self.i2} {self.j1} {self.j2} {self.k1} {self.k2} '{self.operator}' {self.value}"

    def __str__(self):
        return self.to_text()

    def calculate(self, grid):
        array = grid.get_array(self.var_name)

        if self.operator == "=":
            if self.var_name == 'TOPS':
                ArrayUtils.assign_array_2d(array, self.i1-1, self.i2-1, self.j1-1, self.j2-1, self.value-1)
            else:
                ArrayUtils.assign_array_3d(array, self.k1-1, self.k2-1, self.i1-1, self.i2-1, self.j1-1, self.j2-1, self.value)
        elif self.operator == "*":
            if self.var_name == 'TOPS':
                ArrayUtils.multiply_array_2d(array, self.i1-1, self.i2-1, self.j1-1, self.j2-1, self.value)
            else:
                ArrayUtils.multiply_array_3d(array, self.k1-1, self.k2-1, self.i1-1, self.i2-1, self.j1-1, self.j2-1, self.value)
        elif self.operator == "+":
            if self.var_name == 'TOPS':
                ArrayUtils.add_array_2d(array, self.i1-1, self.i2-1, self.j1-1, self.j2-1, self.value)
            else:
                ArrayUtils.add_array_3d(array, self.k1-1, self.k2-1, self.i1-1, self.i2-1, self.j1-1, self.j2-1, self.value)

        return grid.set_array(self.var_name, array)