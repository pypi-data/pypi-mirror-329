from datetime import datetime
from typing import Optional



class Recurrent:
    def __init__(self, start_time:Optional[datetime]=None, end_time:Optional[datetime]=None, well_name=None):
        self.start_time = start_time
        self.end_time = end_time
        self.well_name = well_name
