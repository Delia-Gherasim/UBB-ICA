import itertools
from typing import List
from message.Message import Message
from actions.actions import Action


class BaseAgent:
    _id_counter = itertools.count()

    def __init__(self, model, name: str):
        self.unique_id = next(BaseAgent._id_counter)
        self.model = model
        self.name = name
        self.pos = None
        self.inbox: List[Message] = []

    def step(self, percept) -> 'Action':
        pass

    def receive_message(self, msg: Message):
        self.inbox.append(msg)