from reservoir_info.bean.well.template import Template

class WellSegment:
    DEFAULT_VALUES = {
        'marker': None,
        'outlet': None,
        'i': 1,
        'j': 1,
        'k1': 1,
        'wi': 0,
        'req': 0,
        'xnj': 0,
        'ynj': 0,
        'dcn': 0,
        'dcj': 0,
        'rough': 0,
        'dev': 0,
        'skin': 0,
        'tf': 0,
        'hx': 0,
        'hy': 0,
        'hz': 0,
        'kh': 0,
        'up': 0,
        'rw': 0.25,
        'diam': 0.5,
        'icd_ver': 0,
        'icd_os': 1
    }

    def __init__(self, marker=None, outlet=None, i=None, j=None, k1=None, k2=None, wcon=None, wi=None, tf=None, hx=None,
                 hy=None, hz=None, req=None, kh=None, skin=None, satnum=None, os=None, fcd=None, rw=None, diam=None,
                 length=None, dev=None, rough=None, dcj=None, dcn=None, xnj=None, ynj=None, stage=None, up=None,
                 down=None, icd_ver=None, icd_os=None, template=None):
        self.marker = marker
        self.outlet = outlet
        self.i = i
        self.j = j
        self.k1 = k1
        self.k2 = k2
        self.wcon = wcon
        self.wi = wi
        self.tf = tf
        self.hx = hx
        self.hy = hy
        self.hz = hz
        self.req = req
        self.kh = kh
        self.skin = skin
        self.satnum = satnum
        self.os = os
        self.fcd = fcd
        self.rw = rw
        self.diam = diam
        self.length = length
        self.dev = dev
        self.rough = rough
        self.dcj = dcj
        self.dcn = dcn
        self.xnj = xnj
        self.ynj = ynj
        self.stage = stage
        self.up = up
        self.down = down
        self.icd_ver = icd_ver
        self.icd_os = icd_os
        self.template = template

    @classmethod
    def from_text(cls, text, template):
        segment = cls()

        parts = text.split()
        for index, part in enumerate(parts):
            name = template[index].lower()
            if part == 'NA' or part == '':
                setattr(segment, name, cls.DEFAULT_VALUES.get(name, part))
            else:
                setattr(segment, name, part)
        segment.template = template

        return segment

    def to_text(self):
        parts = []
        for index in range(self.template.size()):
            name = self.template[index].lower()
            value = getattr(self, name, "")
            if name in ['marker', 'outlet'] and value is None:
                parts.append("NA")
            elif name in ['i', 'j', 'k1'] and value == 1:
                parts.append("NA")
            elif name in ['wi', 'req', 'xnj', 'ynj', 'dcn', 'dcj', 'rough', 'dev', 'skin', 'tf', 'hx', 'hy', 'hz', 'kh', 'up', 'icd_ver'] and value == 0:
                parts.append("NA")
            elif name == 'rw' and value == 0.25:
                parts.append("NA")
            elif name == 'diam' and value == 0.5:
                parts.append("NA")
            elif name == 'icd_os' and value == 1:
                parts.append("NA")
            else:
                parts.append(str(value))
        return " ".join(parts)

    def __str__(self):
        return self.to_text()

    def __repr__(self):
        return f"WELSPECS(marker={self.marker}, outlet={self.outlet}, i={self.i}, j={self.j}, k1={self.k1}, k2={self.k2}, wcon={self.wcon}, wi={self.wi}, tf={self.tf}, hx={self.hx}, hy={self.hy}, hz={self.hz}, req={self.req}, kh={self.kh}, skin={self.skin}, satnum={self.satnum}, os={self.os}, fcd={self.fcd}, rw={self.rw}, diam={self.diam}, length={self.length}, dev={self.dev}, rough={self.rough}, dcj={self.dcj}, dcn={self.dcn}, xnj={self.xnj}, ynj={self.ynj}, stage={self.stage}, up={self.up}, down={self.down}, icd_ver={self.icd_ver}, icd_os={self.icd_os})"

class WellSpecs:
    def __init__(self, well_name=None, well_segments = None, template=None):
        """
        井资料，支持正交网格、角点网格、GPG 网格
        表格，含抬头和行数据。抬头部分定义井名和区域名，行数据每一行定义一组井段（well segment）。
        """
        self.well_name = well_name
        self.well_segments = well_segments if well_segments is not None else []
        self.template = template

    @classmethod
    def from_block(cls, block_lines, template):
        well_specs = WellSpecs()

        well_specs.well_name = block_lines[0].split()[1].replace("'", "")
        for line in block_lines[1:]:
            if line:
                well_segment = WellSegment.from_text(line.strip(), template)
                well_specs.well_segments.append(well_segment)

        well_specs.template = template

        return well_specs

    def to_block(self):
        lines = [f"NAME '{self.well_name}'"]
        for segment in self.well_segments:
            lines.append(segment.to_text())

        return lines

    def __str__(self):
        return "\n".join(self.to_block())

if __name__ == '__main__':
    temp_lines = ["TEMPLATE",
            "'MARKER' 'I' 'J' 'K1' 'K2' 'OUTLET' 'WI' 'OS' 'SATMAP' 'HX' 'HY' 'HZ' 'REQ' 'SKIN' 'LENGTH' 'RW' 'DEV' 'ROUGH' 'DCJ' 'DCN' 'XNJ' 'YNJ' /"]
    temp = Template.from_block(temp_lines)

    specs_lines =["NAME 'INJE1'",
        "''  24  25  11  11  NA  NA  SHUT  NA  0  0  0  NA  NA  NA  0.5  NA  NA  NA  1268.16  NA  NA",
        "''  24  25  11  15  NA  NA  OPEN  NA  0  0  DZ  NA  NA  NA  0.5  NA  NA  NA  0  NA  NA"]
    specs = WellSpecs.from_block(specs_lines, temp)
    print(specs)
    print("\n".join(specs.to_block()))