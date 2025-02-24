from dataclasses import dataclass

from mag_tools.bean.base_data import BaseData
from mag_tools.utils.data.list_utils import ListUtils


@dataclass
class Dimension(BaseData):
    def __init__(self, nx=None, ny=None, nz=None, ngrid=None, description=None):
        """
        使用结构网格时，三个整数：NX，NY，NZ
        使用非结构网格时，一个整数：Ngrid
        :param nx: X 网格行数
        :param ny: Y 网格列数
        :param nz: 网格层数
        :param ngrid: 总网格数
        :param description: 描述
        """
        super().__init__()
        self.nx = nx
        self.ny = ny
        self.nz = nz
        self.ngrid = ngrid
        self.description = description

    @classmethod
    def from_block(cls, block_lines):
        dimens = cls()

        block_lines = ListUtils.trim(block_lines)

        dimens_items = block_lines[0].split('#')
        dimens.description = dimens_items[1] if len(dimens_items) > 1 else None

        items = block_lines[1].split()
        dimens.nx = int(items[0]) if len(items) == 3 else None
        dimens.ny = int(items[1]) if len(items) == 3 else None
        dimens.nz = int(items[2]) if len(items) == 3 else None
        dimens.ngrid = int(items[0]) if len(items) == 1 else None
        return dimens

    def to_block(self):
        lines = [f'DIMENS #{self.description}'] if self.description else ['DIMENS']
        if self.nx and self.ny and self.nz:
            lines.append(self.get_text(['nx', 'ny', 'nz']))
        elif self.ngrid:
            lines.append(f'{self.ngrid}')
        return lines

    def __str__(self):
        return "\n".join(self.to_block())


