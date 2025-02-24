from mag_tools.model.base_enum import BaseEnum


class PermType(BaseEnum):
    PERM_X=('PERMX', '油藏网格 x 方向渗透率')
    PERM_Y=('PERMY', '油藏网格 y 方向渗透率')
    PERM_Z=('PERMZ', '油藏网格 z 方向渗透率')