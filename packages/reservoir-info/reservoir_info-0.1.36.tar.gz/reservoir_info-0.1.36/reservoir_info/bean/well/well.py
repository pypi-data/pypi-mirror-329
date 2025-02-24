from mag_tools.utils.data.list_utils import ListUtils

from reservoir_info.bean.well.template import Template
from reservoir_info.bean.well.well_specs import WellSpecs


class Well:
    def __init__(self, template=None, well_specs_set=None):
        """
        井资料，支持正交网格、角点网格、GPG 网格
        表格，含抬头和行数据。抬头部分定义井名和区域名，行数据每一行定义一组井段（well segment）。
        :params well_name: 井名
        :params well_segments: 井段数组
        """
        self.template = template
        self.well_specs_set = well_specs_set if well_specs_set else []

    @classmethod
    def from_block(cls, block_lines):
        """
        从文本块中得到WellSpecs
        """
        specs_set = Well()

        # 首两行是 WELL+############的分隔符; 末尾是 #WELL END############结束行
        block_lines = [line for line in block_lines if not (line.startswith("WELL") or line.startswith("#WELL") or line.startswith("###"))]
        #之后是空行则过滤
        block_lines = block_lines[1:] if block_lines[0] == '' else block_lines

        specs_set.template = Template.from_block(block_lines[:2])

        specs_blocks = ListUtils.split_by_keyword(block_lines[3:], 'NAME ')
        for specs_block in specs_blocks:
            specs = WellSpecs.from_block(specs_block, specs_set.template)
            specs_set.well_specs_set.append(specs)

        return specs_set

    def to_block(self):
        lines = ['WELL', '##################################################','']
        lines.extend(self.template.to_block())
        lines.append('WELSPECS')
        for specs in self.well_specs_set:
            lines.extend(specs.to_block())
            lines.append('')
        lines.append('#WELL END#########################################')
        return lines

    def __str__(self):
        return "\n".join(self.to_block())


if __name__ == '__main__':
    well_lines = ["WELL",
         "##################################################",
         "",
         "TEMPLATE",
         "'MARKER' 'I' 'J' 'K1' 'K2' 'OUTLET' 'WI' 'OS' 'SATMAP' 'HX' 'HY' 'HZ' 'REQ' 'SKIN' 'LENGTH' 'RW' 'DEV' 'ROUGH' 'DCJ' 'DCN' 'XNJ' 'YNJ' /",
         "NAME 'INJE1'",
         "''  24  25  11  11  NA  NA  SHUT  NA  0  0  0  NA  NA  NA  0.5  NA  NA  NA  1268.16  NA  NA",
         "''  24  25  11  15  NA  NA  OPEN  NA  0  0  DZ  NA  NA  NA  0.5  NA  NA  NA  0  NA  NA",
         "",
         "NAME 'PROD2'",
         "''  5  1  2  2  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA",
         "''  5  1  3  3  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA",
         "''  5  1  4  4  NA  NA  OPEN  NA  0  0  DZ  NA  0  NA  0.5  0  0  NA  NA  NA  NA",
         "#WELL END#########################################"]
    well = Well.from_block(well_lines)
    print(well)