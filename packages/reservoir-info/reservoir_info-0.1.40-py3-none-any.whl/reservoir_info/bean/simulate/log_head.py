from dataclasses import dataclass, field

from mag_tools.model.justify_type import JustifyType
from mag_tools.utils.data.string_format import StringFormat
from mag_tools.utils.data.string_utils import StringUtils

@dataclass
class LogHead:
    BOUNDARY = '----------------------------------------------------------------------'

    version: str = field(init=False, default=2023.1, metadata={'description': '程序版本'})
    bits: str = field(init=False, default=2023.1, metadata={'description': '程序位数'})
    compile_date: str = field(init=False, default='Oct 16 2024', metadata={'description': '编译日期'})
    corp_name: str = field(init=False, default='Ennosoft company of China', metadata={'description': '公司名称'})





if __name__ == '__main__':
    head_str = '''
----------------------------------------------------------------------
                   HiSimComp Version 2023.1, 64bit
                       Compiled on Oct 16 2024
                     by Ennosoft company of China                     
----------------------------------------------------------------------    
    '''
    head_blk = head_str.split('\n')
    head = LogHead.from_block(head_blk)
    print('\n'.join(head.to_block()))