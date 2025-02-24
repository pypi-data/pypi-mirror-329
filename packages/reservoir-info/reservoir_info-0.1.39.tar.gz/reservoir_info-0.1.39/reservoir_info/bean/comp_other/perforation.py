from typing import Optional

from reservoir_info.model.perforation_type import PerforationType


class Perforation:
    def __init__(self, perf_type:Optional[PerforationType]=None, i:Optional[int]=None,j:Optional[int]=None,
                 k1:Optional[int]=None, k2:Optional[int]=None, row1:Optional[int]=None, row2:Optional[int]=None):
        self.perf_type = perf_type
        self.i = i
        self.j = j
        self.k1 = k1
        self.k2 = k2
        self.row1 = row1
        self.row2 = row2

    # def from_text(self, text):
