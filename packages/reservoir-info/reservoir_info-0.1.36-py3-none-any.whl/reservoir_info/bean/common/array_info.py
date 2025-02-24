import struct

from mag_tools.bean.data_format import DataFormat
from mag_tools.utils.data.string_format import StringFormat

from reservoir_info.bean.common.array_head import ArrayHeader


class ArrayInfo:
    def __init__(self, header, data):
        self.header = header
        self.data = data    # 数据，为一个[]，数组元素为整数或浮点数

    @staticmethod
    def from_bytes(header, array_type, array_bytes):
        data = []
        if array_type == 'd':  # 如果类型为 'd'，则读取 double 数组
            array_format = 'd' * (len(array_bytes) // 8)
            data = struct.unpack(array_format, array_bytes)
        elif array_type == 'i':  # 否则读取 int 数组
            array_format = 'i' * (len(array_bytes) // 4)
            data = struct.unpack(array_format, array_bytes)

        return ArrayInfo(header, data)

    def to_bytes(self):
        #
        """
        将数组转换为字节数组，包括：数组长度、头信息、数组信息
        :return: byte[]
        """
        # 将头信息转为字节数组
        header_bytes = self.header.to_bytes()

        # 将数据转换为字节数组
        if self.header.array_type == 'd':
            array_format = 'd' * len(self.data)
        elif self.header.array_type == 'i':
            array_format = 'i' * len(self.data)
        else:
            raise ValueError("Unsupported array type")
        array_bytes = struct.pack(array_format, *self.data)

        # 将头信息和数组数据总长度转为字节数组
        total_len = len(array_bytes) + len(header_bytes)
        total_len_bytes = struct.pack('q', total_len)

        return total_len_bytes + header_bytes + array_bytes

    def format_str(self, seperator, pad_length, decimal_places=5):
        text = self.header.format_str()
        for item in self.data:
            text += StringFormat.pad_value(StringFormat.format_number(item, DataFormat(decimal_places=decimal_places)), pad_length) + seperator

        return text

    @classmethod
    def load_bin_file(cls, bin_file_path):
        """
        bin_file_path 二进制结果文件
            BIN文件中，多个数组连续排列，所有数组都按同样的二进制格式存储。
            每个数组的第 1 至第 8 字节存储数组长度“len”,不含这8个字节；
            第 8 至第 273 字节存储数组的 header 信息；
            第 274 至第(len+8)字节存储数组本身。
            其中，header信息包括：
                8字节的时间或日期（double格式）
                1字节的数组类型标识
                128字节的数组名
                64字节的的单位名
                8字节的最大值(double)
                8字节的最小值（double）
                8字节的均值
                1字节的时间类型
                39字节保留
        :return: Array[]
        """
        data = []
        with open(bin_file_path, 'rb') as f:
            while True:
                # 读取数组字节长度，包含Header和数组本身的byte数
                len_bytes = f.read(8)
                if not len_bytes:
                    break
                array_len = struct.unpack('Q', len_bytes)[0] - 265

                # 读取 header 信息
                header_bytes = f.read(265)

                # 读取数组本身
                array_bytes = f.read(array_len)

                _header = ArrayHeader.from_bytes(header_bytes)
                _array = ArrayInfo.from_bytes(_header, _header.array_type, array_bytes)
                data.append(_array)
        return data