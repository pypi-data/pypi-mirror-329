from mag_tools.utils.data.list_utils import ListUtils

from reservoir_info.bean.common.box import Box
from reservoir_info.bean.common.copy_grid import CopyGrid
from reservoir_info.bean.common.dimension import Dimension
from reservoir_info.bean.grid.dimension_value import DimensionValue
from reservoir_info.bean.grid.fipnum import FipNum
from reservoir_info.bean.grid.perm import Perm
from reservoir_info.bean.grid.poro import Poro
from reservoir_info.bean.grid.tops import Tops
from reservoir_info.model.perm_type import PermType


class Grid:
    def __init__(self, dimens=None, fip_num = None, permx =None, permy=None,permz = None, poro = None, tops = None,
                 dxv = None, dyv = None,dzv = None,):
        """
        :param dimens: 维度参数，包括：nx,ny,nz,ngrid等
        :param fip_num: FIP 区域编号
        :param permx: 油藏网格 x 方向渗透率
        :param permy: 油藏网格 y 方向渗透率
        :param permz: 油藏网格 z 方向渗透率
        :param poro: 下地层的孔隙度，𝜙0
        :param tops: 第一层网格的顶面深度
        :param dxv: 指定网格 x 方向的长度
        :param dyv: 指定网格 y 方向的长度
        :param dzv: 指定网格 z 方向的长度
        """
        self.dimens = dimens
        self.fip_num = fip_num
        self.permx = permx
        self.permy = permy
        self.permz = permz
        self.poro = poro
        self.tops = tops
        self.dxv = dxv
        self.dyv = dyv
        self.dzv = dzv

    @classmethod
    def from_block(cls, block_lines):
        grid = cls()

        element_blocks = ListUtils.split_by_keyword(block_lines[2:])
        if element_blocks[0][0].startswith('DIMENS'):
            grid.dimens = Dimension.from_block(element_blocks[0])
            element_blocks = element_blocks[1:]

        grid.fip_num = FipNum(grid.dimens.nx, grid.dimens.ny, grid.dimens.nz)
        grid.permx = Perm(PermType.PERM_X, grid.dimens.nx, grid.dimens.ny, grid.dimens.nz)
        grid.permy = Perm(PermType.PERM_Y, grid.dimens.nx, grid.dimens.ny, grid.dimens.nz)
        grid.permz = Perm(PermType.PERM_Z, grid.dimens.nx, grid.dimens.ny, grid.dimens.nz)

        for element_block in element_blocks:
            first_line = element_block[0]
            if first_line.startswith('BOX'):
                for line in element_block:
                    box = Box.from_text(line)
                    box.calculate(grid)
            elif first_line.startswith('PERM'):
                perm = Perm.from_block(element_block, grid.dimens.nx, grid.dimens.ny, grid.dimens.nz)
                if perm.perm_type == 'PERMX':
                    grid.permx = perm
                elif perm.perm_type == 'PERMY':
                    grid.permy = perm
                elif perm.perm_type == 'PERMZ':
                    grid.permz = perm
            elif first_line.startswith('COPY'):
                for line in element_block:
                    copy = CopyGrid.from_text(line)
                    copy.calculate(grid)
            elif first_line.startswith('PORO'):
                grid.poro = Poro.from_block(element_block, grid.dimens.nx, grid.dimens.ny, grid.dimens.nz)
            elif first_line.startswith('TOPS'):
                grid.tops = Tops.from_text(element_block[0], grid.dimens.nx, grid.dimens.ny)
            elif first_line.startswith('DXV'):
                grid.dxv = DimensionValue.from_block(element_block)
            elif first_line.startswith('DYV'):
                grid.dyv = DimensionValue.from_block(element_block)
            elif first_line.startswith('DZV'):
                grid.dzv = DimensionValue.from_block(element_block)
        return grid

    def to_block(self):
        lines = ['GRID','##################################################']
        lines.extend(self.dimens.to_block())
        lines.append("")

        if self.permx:
            lines.extend(self.permx.to_block(5))
            lines.append("")

        if self.permy:
            lines.extend(self.permy.to_block(5))
            lines.append("")

        if self.permz:
            lines.extend(self.permz.to_block(5))
            lines.append("")

        if self.poro:
            lines.extend(self.poro.to_block())
            lines.append("")

        if self.tops:
            lines.append(self.tops.to_text())
            lines.append("")

        if self.dxv:
            lines.extend(self.dxv.to_block())
            lines.append("")

        if self.dyv:
            lines.extend(self.dyv.to_block())
            lines.append("")

        if self.dzv:
            lines.extend(self.dzv.to_block())
            lines.append("")

        lines.append('#GRID END#########################################')
        return lines

    def __str__(self):
        return "\n".join(self.to_block())

    def get_array(self, var_type):
        _var = None
        if var_type == 'PERMX':
            _var = self.permx.data_3d
        elif var_type == 'PERMY':
            _var = self.permy.data_3d
        elif var_type == 'PERMZ':
            _var = self.permz.data_3d
        elif var_type == 'FIPNUM':
            _var = self.fip_num.data_3d
        elif var_type == 'TOPS':
            _var = self.tops.data_2d
        return _var

    def set_array(self, var_type, value):
        if var_type == 'PERMX':
            self.permx.data_3d = value
        elif var_type == 'PERMY':
            self.permy.data_3d = value
        elif var_type == 'PERMZ':
            self.permz.data_3d = value
        elif var_type == 'FIPNUM':
            self.fip_num = value
        elif var_type == 'TOPS':
            self.tops.data_2d = value