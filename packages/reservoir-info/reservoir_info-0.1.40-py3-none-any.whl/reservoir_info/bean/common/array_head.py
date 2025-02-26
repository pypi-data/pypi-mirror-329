import struct

from mag_tools.utils.data.string_format import StringFormat


class ArrayHeader:
    def __init__(self, datetime, array_type, array_name, unit_name, max_value=None, min_value=None, mean_value=None, time_type='d', reserve=None):
        self.datetime = datetime    # 日期或时间，浮点数。类型为d时,整数部分为8位日期，小数部分为0.x天; 类型为i时，就是浮点数时间
        self.array_type = array_type    # 数据类型，i: 整型；d：双精度
        self.array_name = array_name    # 数组名
        self.unit_name = unit_name      # 单位名
        self.max_value = max_value      # 最大值
        self.min_value = min_value      # 最小值
        self.mean_value = mean_value    # 均值
        self.time_type = time_type      # 时间类型，d: “YYYYMMDD.x”，t: 浮点时间
        self.reserve = reserve

    @staticmethod
    def from_bytes(header_bytes):
        datetime,array_type,array_name,unit_name,max_value,min_value,mean_value,time_type = struct.unpack(
            '=d1s128s64sddd1s39x', header_bytes)

        return ArrayHeader(datetime=datetime, array_type=array_type.decode('utf-8'),
                           array_name=array_name.decode('utf-8').strip('\x00'),
                           unit_name=unit_name.decode('utf-8').strip('\x00'),
                           max_value=max_value, min_value=min_value,
                           mean_value=mean_value, time_type=time_type.decode('utf-8'))

    def to_bytes(self):
        header_bytes = struct.pack(
            '=dB128s64sdddB39x',
            self.datetime,
            ord(self.array_type),
            self.array_name.encode('utf-8'),
            self.unit_name.encode('utf-8'),
            self.max_value,
            self.min_value,
            self.mean_value,
            ord(self.time_type)
        )

        return header_bytes

    def format_str(self):
        text = ''
        attrs = [ (self.datetime, 12), (self.array_name, 10), (self.unit_name, 8), (self.max_value, 12), (self.min_value, 12), (self.mean_value, 12) ]
        for attr, length in attrs:
            if attr:
               text += StringFormat.pad_value(attr, length)
        return text

    def __repr__(self):
        return (f"Header(time_or_date={self.datetime}, array_type={self.array_type}, "
                f"array_name='{self.array_name}', unit_name='{self.unit_name}', "
                f"max_value={self.max_value}, min_value={self.min_value}, "
                f"mean_value={self.mean_value}, time_type={self.time_type})")