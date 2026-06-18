from enum import Enum

class TownStatus(Enum):
    SAFE = "SAFE"
    WARNING = "WARNING"
    IMPACTED = "IMPACTED"
    EVACUATING = "EVACUATING"
    DESTROYED = "DESTROYED"

class Performative(Enum):
    INFORM = "INFORM"
    REQUEST = "REQUEST"
    WARN = "WARN"
    PROPOSE = "PROPOSE"