from reservoir_info.model.user_time_type import UserTimeType


class Schedule:
    def __init__(self, use_time_type=UserTimeType.USEENDTIME):
        """
        井口控制，井产率限制，井射孔控制，油藏参数随时间变化，以及文件输出控制
        """
        self.use_time_type = use_time_type