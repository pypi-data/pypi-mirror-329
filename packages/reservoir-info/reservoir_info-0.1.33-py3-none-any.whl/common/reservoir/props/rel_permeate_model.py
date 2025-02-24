from typing import List, Optional

from mag_tools.utils.common.list_utils import ListUtils

from mag_common.reservoir.props.pvdg import PvdgSet
from mag_common.reservoir.props.pvto import PvtoSet
from mag_common.model.reservoir.module_type import ModuleType
from mag_common.model.reservoir.rel_permeate_type import RelPermeateType


class RelPermeateModel:
    def __init__(self, pvdgs : Optional[PvdgSet]= None, pvtos : Optional[PvtoSet] = None, model_type : Optional[RelPermeateType] = None):
        self.pvdgs = pvdgs if pvdgs is not None else []
        self.pvtos = pvtos if pvtos is not None else []
        self.model_type = model_type if model_type is not None else RelPermeateType.SEGR

    @classmethod
    def from_block(cls, block_lines : List[str], module_type : ModuleType= None)-> 'RelPermeateModel' or None:
        if not block_lines:
            return None

        block_lines = ListUtils.trim(block_lines)

        model_type_line = block_lines[0].strip()
        model_type = RelPermeateType[model_type_line] if model_type_line else RelPermeateType.SEGR if module_type == ModuleType.OILWATER else RelPermeateType.STONEII
        blocks = ListUtils.split_by_keywords(block_lines[1:], ['PVDG', "PVTO"])
        pvdg_block = blocks['PVDG']
        pvto_block = blocks['PVTO']
        values = {"model_type": model_type,
                  "pvdgs": PvdgSet.from_block(pvdg_block),
                  "pvtos": PvtoSet.from_block(pvto_block)}
        return cls(**values)

    def to_block(self):
        lines = [self.model_type.name]
        lines.extend(self.pvdgs.to_block())
        lines.extend(self.pvtos.to_block())
        return lines

    def __str__(self):
        return "\n".join(self.to_block())

if __name__ == "__main__":
    text = '''
    STONEII
PVDG
#       Pres        Bg       Vis 
         400    5.4777     0.013
         800    2.7392    0.0135
        1200    1.8198     0.014
        1600    1.3648    0.0145
        2000    1.0957     0.015
        2400    0.9099    0.0155
        2800    0.7799     0.016
        3200    0.6871    0.0165
        3600    0.6035     0.017
        4000    0.5432    0.0175
PVTO
#        Rssat      Pres        Bo      Vis
         0.165       400     1.012      1.17 /
         0.335       800    1.0255      1.14 /
           0.5      1200     1.038      1.11 /
         0.665      1600     1.051      1.08 /
         0.828      2000     1.063      1.06 /
         0.985      2400     1.075      1.03 /
          1.13      2800     1.087         1 /
          1.27      3200    1.0985      0.98 /
          1.39      3600      1.11      0.95 /
           1.5      4000      1.12      0.94
                    5000    1.1189      0.94 /
/
    '''
    _lines = text.split('\n')
    model = RelPermeateModel.from_block(_lines)
    print(model)

