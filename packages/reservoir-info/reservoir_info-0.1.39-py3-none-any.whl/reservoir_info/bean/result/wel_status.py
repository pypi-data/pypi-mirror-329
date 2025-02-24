from reservoir_info.bean.common.array_info import ArrayInfo
from reservoir_info.bean.common.array_head import ArrayHeader


class WellStatus:
    def __init__(self, date, well_id, well_name, node_number, product_system, product_infos):
        self.date = date
        self.id = well_id   # 井号
        self.name = well_name   # 井名
        self.node_number = node_number  # 井节点数目
        self.product_system = product_system    # 生产制度
        self.product_infos = product_infos    # 生产数据，为静态和动态数组,Array[]

    @classmethod
    def from_block(cls, date, block_lines):
        # 解析井信息行
        items = block_lines[0].split(' ')
        _id,name,node_number,product_system = items[1], items[2].replace("'",""), items[3], f"{items[4]} {items[5]}".replace("'","")

        # 解析数据块，每行为一个数组，由若干数组组成
        product_infos = []
        for line in block_lines[1:]:
            items = line.split()
            if items[0] in {'XCOORD', 'YCOORD', 'DEPTH'}:
                array_type = 'd'
            else:
                array_type = 'i'

            head = ArrayHeader(None, array_type, items[0], items[1])
            data = [float(value) if array_type == 'd' else int(value) for value in items[2:]]
            product_infos.append(ArrayInfo(head, data))

        return WellStatus(date, _id, name, node_number, product_system, product_infos)

    def to_block(self, pad_length):
        block_lines = [f"WELL {self.id} '{self.name}' {self.node_number} '{self.product_system}'"]
        for info in self.product_infos:
            block_lines.append(info.format_str('\t', pad_length))
        block_lines.append('')
        return block_lines

