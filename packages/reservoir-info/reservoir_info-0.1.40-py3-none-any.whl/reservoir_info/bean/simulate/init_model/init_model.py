from dataclasses import dataclass, field
from typing import Optional

from mag_tools.utils.data.list_utils import ListUtils

from reservoir_info.bean.simulate.init_model.init_comp_model import InitCompModel
from reservoir_info.bean.simulate.init_model.init_ow_model import InitOwModel


@dataclass
class InitModel:
    BOUNDARY = '----------------------------------------------------------------------'

    uuid: Optional[str] = field(default=None, metadata={"description": "模拟标识"})
    comp_model: Optional[InitCompModel] = field(default=None, metadata={"description": "组分模拟"})
    ow_model: Optional[InitOwModel] = field(default=None, metadata={"description": "油水模拟"})

    @classmethod
    def from_block(cls, block_lines: list[str]):
        model = cls()

        if len(block_lines) >= 4:
            init_line = ListUtils.pick_line(block_lines, 'INIT')
            if 'COMPOSITION' in init_line:
                model.comp_model = InitCompModel.from_block(block_lines)
            elif 'OIL-WATER' in init_line:
                model.ow_model = InitOwModel.from_block(block_lines)

        return model

    def to_block(self):
        if self.ow_model:
            return self.ow_model.to_block()
        elif self.comp_model:
            return self.comp_model.to_block()
        else:
            return []

if __name__ == '__main__':
    ow_str = '''
----------------------------------------------------------------------
                         INIT OIL-WATER MODEL                         

 Building matrix costs 107.576ms
 Reservoir status INIT in SAT_REG 1 EQL_REG 1 complete
----------------------------------------------------------------------
'''

    comp_str = '''
    ----------------------------------------------------------------------
                            INIT COMPOSITION MODEL

     Building matrix costs 0.2001ms
     Partition grid costs 0.2842ms
     At gas-oil contact of EOS region 1, EQL region 1:
     Tc_exact = 1145.15, Tc_estimate = 1103.78
     Vc_exact = 7.04359, Vc_estimate = 5.93077
     Reservoir status INIT in SAT_REG 1 EQL_REG 1 PVT_REG 1 EOS_REG 1 complete
    ----------------------------------------------------------------------
    '''
    init_model_ = InitModel.from_block(ow_str.split('\n'))
    block_ = init_model_.to_block()
    print('\n'.join(block_))

    init_model_ = InitModel.from_block(comp_str.split('\n'))
    block_ = init_model_.to_block()
    print('\n'.join(block_))
