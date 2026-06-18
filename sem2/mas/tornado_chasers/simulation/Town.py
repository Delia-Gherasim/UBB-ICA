from typing import Tuple
from Common.enums import TownStatus


class Town:
    def __init__(self, name: str, location: Tuple[int, int]):
        self.name = name
        self.location = location
        self.status = TownStatus.SAFE

    def update_status(self, status: TownStatus):
        self.status = status