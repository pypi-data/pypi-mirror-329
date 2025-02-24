from typing import Optional

from mag_tools.model.common.justify_type import JustifyType
from mag_tools.utils.common.list_utils import ListUtils
from mag_tools.utils.common.string_format import StringFormat


class Equilpar:
    """
    Equilpar 类用于表示油藏模拟中的 EQUILPAR 数据块。

    属性:
        ref_dep (float): 参考深度，单位：m(米制)，feet(英制)，cm(lab)，ms(MESO)。
        ref_p (float): 参考深度的压力，单位：bar(米制)，psi(英制)，atm(lab)，Pa(MESO)。
        owc (float): 油水界面深度，在气水模型中是气水界面深度 GWC，单位：m(米制)，feet(英制)，cm(lab)，um(MESO)。
        pcowc (float): 油水界面处的毛管力，在气水模型中是气水界面处的毛管力 pcgwc，单位：bar(米制)，psi(英制)，atm(lab)，Pa(MESO)。
        dh (float): 初始化时的深度步长，单位：m(米制)，feet(英制)，cm(lab)，um(MESO)。
        goc (float): 油气界面深度，单位：m(米制)，feet(英制)，cm(lab)，um(MESO)。
        pcgoc (float): 油气界面处的毛管力，单位：bar(米制)，psi(英制)，atm(lab)，Pa(MESO)。
    """

    def __init__(self, ref_dep:Optional[float]=None, ref_p:Optional[float]=None, gwc_owc:Optional[float]=None,
                 gwcpc_owcpc:Optional[float]=None, dh:Optional[float]=None, goc:Optional[float]=None, goc_pc:Optional[float]=None):
        """
        初始化 Equilpar 实例。

        :param ref_dep: 参考深度。
        :param ref_p: 参考深度的压力。
        :param gwc_owc: 气水或油水界面深度
        :param gwcpc_owcpc: 气水或油水界面处的毛管力。
        :param dh: 初始化时的深度步长。
        :param goc: 油气界面深度。
        :param goc_pc: 油气界面处的毛管力。
        """
        self.ref_dep = ref_dep
        self.ref_p = ref_p
        self.gwc_owc = gwc_owc
        self.gwcpc_owcpc = gwcpc_owcpc
        self.dh = dh
        self.goc = goc
        self.goc_pc = goc_pc


    @classmethod
    def from_block(cls, block_lines):
        """
        从块数据创建 Equilpar 实例。

        :param block_lines: 包含 EQUILPAR 数据块的行列表。
        :return: 创建的 Equilpar 实例。
        """
        block_lines = ListUtils.trim(block_lines)
        description_line = block_lines[1].strip("# ").split() + block_lines[3].strip("# ").split()
        data_line = list(map(float, block_lines[2].split())) + list(map(float, block_lines[4].split()))
        data_dict = dict(zip(description_line, data_line))

        return cls(
            ref_dep=data_dict.get("Ref_dep", 0.0),
            ref_p=data_dict.get("Ref_p", 0.0),
            gwc_owc=data_dict.get("GWC/OWC", 0.0),
            gwcpc_owcpc=data_dict.get("GWC_pc/OWC_pc", 0.0),
            dh=data_dict.get("dh", 0.0),
            goc=data_dict.get("GOC", 0.0),
            goc_pc=data_dict.get("GOC_pc", 0.0)
        )

    def to_block(self):
        """
        将 Equilpar 实例转换为块数据。

        :return: 包含 EQUILPAR 数据块的行列表。
        """
        pad_length = max(len(str(param)) for param in
                   [self.ref_dep, self.ref_p, self.gwc_owc, self.gwcpc_owcpc, self.dh, self.goc, self.goc_pc] if
                   param is not None)
        if pad_length <= 13: pad_length = 15

        title_items_1 = ["Ref_dep", "Ref_p", "GWC/OWC", "GWC_pc/OWC_pc", "dh"]
        title_items_2 = ["goc", "goc_pc"]
        values_1 = [self.ref_dep, self.ref_p, self.gwc_owc, self.gwcpc_owcpc, self.dh]
        values_2 = [self.goc, self.goc_pc]

        return ['EQUILPAR',
                f"# {StringFormat.pad_values(title_items_1, pad_length, JustifyType.LEFT)}",
                f"  {StringFormat.pad_values(values_1, pad_length, JustifyType.LEFT)}",
                f"# {StringFormat.pad_values(title_items_2, pad_length, JustifyType.LEFT)}",
                f"  {StringFormat.pad_values(values_2, pad_length, JustifyType.LEFT)}",]

    def __str__(self):
        """
        返回 Equilpar 实例的字符串表示。

        :return: Equilpar 实例的字符串表示。
        """
        return "\n".join(self.to_block())

if __name__ == "__main__":
    txt = """
    EQUILPAR
# Ref_dep    Ref_p    GWC/OWC  GWC_pc/OWC_pc   dh
  9035       3600      9950        0.0         2
# GOC       GOC_pc
  8800        0.0 
    """
    _eq = Equilpar.from_block(txt.split("\n"))
    print(_eq)