from mag_tools.model.base_enum import BaseEnum

class PerforationType(BaseEnum):
    """
    穿孔类型枚举
    枚举值为不包含前缀的穿孔类型名，如：PerforationType.PERF
    """
    PERF = ('Perforation', '穿孔')  # 穿孔
    SEG = ('Segmentation', '分段')  # 分段
    STAGE = ('Stage', '阶段')  # 阶段

if __name__ == '__main__':
    # 示例用法
    print(PerforationType.PERF.code)  # 输出: Perforation
    print(PerforationType.PERF.desc)  # 输出: 穿孔
    print(PerforationType.of_desc("分段"))  # 输出: PerforationType.SEG
