from typing import Any
from Common.enums import Performative

class Message:
    def __init__(self, sender: str, receiver: str, performative: Performative, content: Any, priority: int = 0, conversation_id: str = "", timestamp: int = 0):
        self.sender = sender
        self.receiver = receiver
        self.performative = performative
        self.content = content
        self.priority = priority
        self.conversation_id = conversation_id
        self.timestamp = timestamp

    def __repr__(self):
        return f"[{self.performative.value}] {self.sender} -> {self.receiver}: {self.content}"