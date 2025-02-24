import os
from typing import Any

from mag_tools.utils.data.list_utils import ListUtils

from reservoir_info.bean.props.props import Props
from reservoir_info.bean.grid.grid import Grid
from reservoir_info.bean.comp_module.module_control import ModuleControl
from reservoir_info.bean.well.well import Well


class CompModule:
    keyword_map = {
        "BASE": (None, None),
        "GRID": (
        "##################################################", "#GRID END#########################################"),
        "WELL": (
        "##################################################", "#WELL END#########################################"),
        "PROPS": (
        "##################################################", "#PROPS END########################################"),
        "SOLUTION": (
        "##################################################", "#SOLUTION END######################################"),
        "TUNE": (None, None)
    }

    def __init__(self, name = None, control=None, grid=None, well = None, props = None, solution = None, tune = None):
        self.name = name
        self.control = control
        self.grid = grid
        self.well = well
        self.props = props
        self.solution = solution
        self.tune = tune

    @classmethod
    def load_from_file(cls, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line.strip() for line in file.readlines()]
            module = cls.from_block(lines)
            module.name = os.path.basename(file_path).replace('.dat', '')

        return module

    def save_to_file(self, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            for line in self.to_block():
                file.write(line)
                file.write("\n")

    @classmethod
    def from_block(cls, block_lines):
        module = cls()

        block_lines.insert(0, "BASE")
        segments = ListUtils.split_by_boundary(block_lines, cls.keyword_map)

        module.control = ModuleControl.from_block(segments["FIRST"])
        module.grid = Grid.from_block(segments["GRID"])
        module.well = Well.from_block(segments["WELL"])
        module.props = Props.from_block(segments["PROPS"])
        # module.solution = Solution.from_block(segments["SOLUTION"])
        # module.other = segments["TUNE"]


        return module

    def to_block(self):
        lines = self.control.to_block()
        grid_lines = self.grid.to_block()
        lines.extend(grid_lines)
        return lines

    @property
    def key_parameter(self) -> dict[str, Any]:
        return {}

    def __str__(self):
        lines = self.to_block()
        return "\n".join(lines)

if __name__ == '__main__':
    # 示例用法
    data = """MODELTYPE BlackOil
FIELD

GRID
##################################################
DIMENS
 5 2 1

BOX FIPNUM 1 5 1 2 1 1 = 2

PERMX
49.29276      162.25308      438.45926      492.32336      791.32867
704.17102      752.34912      622.96875      542.24493      471.45953

COPY PERMX  PERMY  1 5 1 2 1 1 
COPY PERMX  PERMZ  1 5 1 2 1 1

BOX  PERMZ  1 5 1 2 1 1  '*' 0.01

PORO
 5*0.087
 5*0.097

TOPS 10*9000.00

BOX TOPS   1  1  1 2  1  1  '='  9000.00
BOX TOPS   2  2  1 2  1  1  '='  9052.90

DXV
 5*300.0

DYV
 2*300.0

DZV
 20

#GRID END#########################################

WELL
##################################################

TEMPLATE
'MARKER' 'I' 'J' 'K1' 'K2' 'OUTLET' 'WI' 'OS' 'SATMAP' 'HX' 'HY' 'HZ' 'REQ' 'SKIN' 'LENGTH' 'RW' 'DEV' 'ROUGH' 'DCJ' 'DCN' 'XNJ' 'YNJ' /
WELSPECS
NAME 'INJE1'
''  24  25  11  11  NA  NA  SHUT  NA  0  0  0  NA  NA  NA  0.5  NA  NA  NA  1268.16  NA  NA  
''  24  25  11  15  NA  NA  OPEN  NA  0  0  DZ  NA  NA  NA  0.5  NA  NA  NA  0  NA  NA  

NAME 'PROD2'
''  5  1  2  2  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA  
''  5  1  3  3  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA  
''  5  1  4  4  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA 
#WELL END#########################################

PROPS
##################################################
SWOF
#           Sw         Krw       Krow       Pcow(=Po-Pw)
       0.15109           0           1         400
       0.15123           0     0.99997      359.19
       0.15174           0     0.99993      257.92

#PROPS END########################################

SOLUTION
##################################################

EQUILPAR
# Ref_dep    Ref_p    GWC/OWC  GWC_pc/OWC_pc   dh
  9035       3600      9950        0.0         2
# GOC       GOC_pc
  8800        0.0    
PBVD
   5000        3600
   9000        3600

#SOLUTION END######################################

TUNE
TSTART  1990-01-01 
MINDT  0.1  MAXDT  31  DTINC  2.0  DTCUT  0.5  CHECKDX  
MAXDP  200  MAXDS  0  MAXDC  0  MBEPC  1E-4  MBEAVG  1E-6   
SOLVER  1034


RESTART

RPTSCHED
BINOUT SEPARATE NETONLY GEOM RPTONLY RSTBIN SOLVD 
POIL SOIL SGAS SWAT RS NOSTU  TECPLOT 
 /

RPTSUM
POIL 1 2 1 /
POIL AVG Reg 2 /
"""

    # mod = CompModule.load_from_file(r"D:\HiSimPack\examples\Comp\spe9\SPE9.dat")
    _lines = data.split("\n")
    mod = CompModule.from_block(_lines)
    print(mod)
