from typing import Optional

from mag_tools.model.common.unit_system import UnitSystem

from reservoir_info.model.model_type import ModelType

class ModuleControl:
    def __init__(self, module_type:Optional[ModelType]=None, unit_system:Optional[UnitSystem]=None, solnt:Optional[int]=None,
                 miscible:bool=False, diffuse:bool=False,
                 gravdr:bool=False, newton_chop:bool=False, description:Optional[str]=None):
        self.module_type = module_type
        self.unit_system = unit_system
        self.solnt = solnt
        self.miscible = miscible    # 打开混相相对渗透率模型
        self.diffuse = diffuse      # 启用组分扩散模型
        self.gravdr = gravdr        # 开启 gravity drainage 效应
        self.newton_chop = newton_chop  # 开启牛顿迭代截断
        self.description = description if description else []

    @classmethod
    def from_block(cls, block_lines):
        ctl = cls()
        for line in block_lines:
            line = line.strip()
            if line.startswith('#'):
                ctl.description.append(line[1:].strip())
            elif line.startswith("MODELTYPE"):
                ctl.module_type = ModelType[line.split()[1].upper()]
            elif line in {"METRIC", "FIELD", "LAB", "MESO"}:
                ctl.unit_system = UnitSystem[line]
            elif line.startswith("SOLNT"):
                ctl.solnt = int(line.split()[1])
            elif line.upper() == "MISCIBLE":
                ctl.miscible = True
            elif line.upper() == "DIFFUSE":
                ctl.diffuse = True
            elif line.upper() == "GRAVDR":
                ctl.gravdr = True
            elif line.upper() == "NEWTONCHOP":
                ctl.newton_chop = True

        return ctl

    def to_block(self):
        block_lines = [f'# {desc}' for desc in self.description]

        if len(block_lines) > 0:
            block_lines.append('')

        if self.module_type:
            block_lines.append(f'MODELTYPE {self.module_type.code}')
        if self.unit_system:
            block_lines.append(self.unit_system.name)
        if self.solnt is not None:
            block_lines.append(f'SOLNT {self.solnt}')
        if self.miscible:
            block_lines.append('MISCIBLE'.lower())
        if self.diffuse:
            block_lines.append('DIFFUSE')
        if self.gravdr:
            block_lines.append('GRAVDR')
        if self.newton_chop:
            block_lines.append('NEWTONCHOP')

        block_lines.append('')

        return block_lines

    def __str__(self):
        return "\n".join(self.to_block())
