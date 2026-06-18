from agents.BaseAgent import BaseAgent
from message.Message import Message
from typing import List, Dict

class MessageOrchestrator:
    def __init__(self):
        self.inbox: List[Message] = []
        self.agents: Dict[str, 'BaseAgent'] = {}

    def register(self, agent: 'BaseAgent'):
        self.agents[agent.name] = agent

    def unregister(self, agent: 'BaseAgent'):
        if agent.name in self.agents:
            del self.agents[agent.name]

    def send_message(self, msg: Message):
        self.inbox.append(msg)
        self.receive_message(msg)

    def receive_message(self, msg: Message):
        if msg.receiver in self.agents:
            self.agents[msg.receiver].receive_message(msg)