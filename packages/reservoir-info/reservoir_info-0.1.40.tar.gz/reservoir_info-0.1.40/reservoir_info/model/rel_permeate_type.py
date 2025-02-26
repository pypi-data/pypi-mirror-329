
from mag_tools.model.base_enum import BaseEnum


class RelPermeateType(BaseEnum):
    """
    相对渗透率类型枚举
    枚举值为相对渗透率模型的名称，如：RelPermeateType.STONEI
    """
    STONEI = ('Stonei', 'STONE II 模型')  # STONE II 模型
    STONEII = ('Stoneii', 'STONE I 模型')  # STONE I 模型
    SEGR = ('Segr', '分离模型')  # 分离模型

if __name__ == '__main__':
    # 示例用法
    print(RelPermeateType.STONEI.code)  # 输出: ('Stonei', 'STONE II 模型')
    print(RelPermeateType.STONEII.code)  # 输出: ('Stoneii', 'STONE I 模型')
    print(RelPermeateType.SEGR.desc)  # 输出: ('Segr', '分离模型')
