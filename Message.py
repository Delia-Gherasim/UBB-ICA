from enum import Enum


class Performative(Enum):
    INFORM = "INFORM"
    REQUEST = "REQUEST"
    WARN = "WARN"
    PROPOSE = "PROPOSE"

class Message:
    def __init__(self, sender_id, receiver_id, performative, content):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.performative = performative
        self.content = content
    def __repr__(self):
        return (
            f"[{self.performative.value}] "
            f"{self.sender_id} -> {self.receiver_id} : {self.content}"
        )