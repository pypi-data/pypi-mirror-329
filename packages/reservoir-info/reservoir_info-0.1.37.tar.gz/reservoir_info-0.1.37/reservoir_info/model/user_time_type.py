
from mag_tools.model.base_enum import BaseEnum


class UserTimeType(BaseEnum):
    """
    用户时间类型枚举
    枚举值为用户时间的名称，如：UserTimeType.USESTARTTIME
    """
    USESTARTTIME = ('UseStartTime', '开始时间')  # 开始时间
    USEENDTIME = ('UseEndTime', '结束时间')  # 结束时间

if __name__ == '__main__':
    # 示例用法
    print(UserTimeType.USESTARTTIME.code)  # 输出: ('UseStartTime', '开始时间')
    print(UserTimeType.USEENDTIME.code)  # 输出: ('UseEndTime', '结束时间')
