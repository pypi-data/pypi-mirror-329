
from mag_tools.model.base_enum import BaseEnum


class WellGroupModel(BaseEnum):
    """
    井组模型枚举
    枚举值为井组模型的名称，如：WellGroupModel.GROUPP
    """
    GROUPP = ('Groupp', '生产井')  # 生产井
    GROUPI = ('Groupi', '注入井')  # 注入井
    FIXED = ('Fixed', '混合井')  # 混合井

if __name__ == '__main__':
    # 示例用法
    print(WellGroupModel.GROUPP.code)  # 输出: ('Groupp', '生产井')
    print(WellGroupModel.GROUPI.code)  # 输出: ('Groupi', '注入井')
    print(WellGroupModel.FIXED.code)  # 输出: ('Fixed', '混合井')
