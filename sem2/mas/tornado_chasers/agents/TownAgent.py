from agents.BaseAgent import BaseAgent
from actions.actions import EvadeAction, ObserveAction
from Common.enums import Performative

class TownAgent(BaseAgent):
    def __init__(self, model, name):
        super().__init__(model, name)
        self.evacuated = False
        self.impacted = False

    def step(self, percept):
        tick = percept.current_tick
        self.inbox = percept.received_messages
        action_to_take = ObserveAction(self.unique_id, timestamp=tick, priority=1)

        for msg in self.inbox:
            if msg.performative == Performative.WARN and not self.evacuated:
                action_to_take = EvadeAction(self.unique_id, timestamp=tick, priority=10)
        self.inbox.clear()

        return action_to_take