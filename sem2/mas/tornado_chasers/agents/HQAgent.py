import math
from typing import Dict, Tuple, List
from agents.BaseAgent import BaseAgent
from message.Message import Message
from Common.enums import Performative
from actions.actions import ObserveAction, AssignAction, WarnAction

class HQAgent(BaseAgent):
    def __init__(self, model, name="HQ"):
        super().__init__(model, name)
        self.threatMap: Dict[int, Tuple[int, int]] = {}
        self.townRegistry = [] 
        self.activeChasers: List[int] = [] 
        self.historyTracks: Dict[int, List[Tuple[int, int]]] = {}
        self.assignments: Dict[int, str] = {}

    def processSighting(self, msg: Message):
        t_id = msg.content["tornado_id"]
        t_pos = msg.content["pos"]
        self.threatMap[t_id] = t_pos
        
        if t_id not in self.historyTracks:
            self.historyTracks[t_id] = []
        self.historyTracks[t_id].append(t_pos)

    def assignChaser(self, chaser_id: int, tick: int) -> AssignAction:
        return AssignAction(self.unique_id, timestamp=tick, priority=3)

    def monitorTowns(self, tick: int) -> ObserveAction:
        return ObserveAction(self.unique_id, timestamp=tick, priority=1)

    def issueWarning(self, town, tick: int) -> WarnAction:
        msg = Message(
            sender=self.name, 
            receiver=town.name, 
            performative=Performative.WARN, 
            content="EVACUATE",
            timestamp=tick,
            priority=10
        )
        self.model.msg_orchestrator.send_message(msg)
        return WarnAction(self.unique_id, town.name, timestamp=tick, priority=10)

    def step(self, percept):
        tick = percept.current_tick
        self.inbox = percept.received_messages
        new_sightings = False
        
        for msg in self.inbox:
            if msg.performative == Performative.INFORM and msg.content.get("type") == "sighting":
                self.processSighting(msg)
                new_sightings = True
        self.inbox.clear()

        for t_id, tornado_pos in self.threatMap.items():
            for agent in self.model.agents:
                if type(agent).__name__ == "TownAgent":
                    dist = max(abs(agent.pos[0] - tornado_pos[0]), abs(agent.pos[1] - tornado_pos[1]))
                    if dist <= 4 and not getattr(agent, 'evacuated', False):
                        return self.issueWarning(agent, tick)

        if new_sightings:
            monitored = set(self.assignments.keys())
            unmonitored = [t for t in self.threatMap if t not in monitored]
            available = [a for a in self.model.agents if type(a).__name__ == "ChaserAgent" and a.active and getattr(a, 'targetTornado', None) is None]

            for t_id in unmonitored:
                if available:
                    tornado_pos = self.threatMap[t_id]
                    chaser = min(available, key=lambda c: math.dist(c.pos, tornado_pos) if c.pos else float('inf'))
                    available.remove(chaser)
                    self.assignments[t_id] = chaser.name

                    msg = Message(
                        sender=self.name, 
                        receiver=chaser.name, 
                        performative=Performative.REQUEST, 
                        content={"tornado_id": t_id},
                        timestamp=tick,
                        priority=3
                    )
                    self.model.msg_orchestrator.send_message(msg)
                    return self.assignChaser(chaser.unique_id, tick)

        return self.monitorTowns(tick)