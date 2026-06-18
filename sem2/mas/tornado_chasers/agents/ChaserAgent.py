from agents.BaseAgent import BaseAgent
from message.Message import Message
from actions.actions import MoveAction, EvadeAction, DocumentAction, ReportAction, ObserveAction
from Common.enums import Performative
import random

class ChaserAgent(BaseAgent):
    def __init__(self, model, name: str, visibility_range=4, safety_distance=1):
        super().__init__(model, name)
        self.visibilityRange = visibility_range
        self.safety_distance = safety_distance
        self.beliefs = {}
        
        self.targetTornado = None
        self.documentationInProgress = False
        self.isSafe = True
        
        self.documentation_progress = 0
        self.required_doc_time = 3
        self.active = True

    def _get_distance(self, pos1, pos2):
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        if getattr(self.model.grid, 'torus', False):
            dx = min(dx, self.model.grid.width - dx)
            dy = min(dy, self.model.grid.height - dy)
        return max(dx, dy)

    def scout(self, valid_moves, tick) -> MoveAction:
        if valid_moves:
            return MoveAction(self.unique_id, random.choice(valid_moves), timestamp=tick, priority=2)
        return ObserveAction(self.unique_id, timestamp=tick, priority=1)

    def document(self, tornado_id: int, tick) -> DocumentAction:
        self.documentationInProgress = True
        return DocumentAction(self.unique_id, tornado_id, timestamp=tick, priority=5)

    def evade(self, tick) -> EvadeAction:
        self.isSafe = False
        return EvadeAction(self.unique_id, timestamp=tick, priority=10)

    def reportSighting(self, tornado_id: int, pos: tuple, tick: int):
        content = {
            "type": "sighting",
            "tornado_id": tornado_id,
            "pos": pos
        }
        msg = Message(
            sender=self.name,
            receiver="HQ",
            performative=Performative.INFORM,
            content=content,
            timestamp=tick,
            priority=3
        )
        self.model.msg_orchestrator.send_message(msg)
        self.model.log_event(f"[{self.name}] SIGHTED Tornado_{tornado_id} at {pos}!")

    def step(self, percept):
        if not self.active:
            return None

        tick = percept.current_tick
        self.inbox = percept.received_messages
        self._process_inbox()

        if any(type(a).__name__ == "TornadoAgent" for a in percept.cellmates):
            return self.evade(tick)

        self.isSafe = True

        for tornado in percept.visible_tornadoes:
            if tornado.unique_id not in self.beliefs or self.beliefs[tornado.unique_id] != tornado.pos:
                self.beliefs[tornado.unique_id] = tornado.pos
                self.reportSighting(tornado.unique_id, tornado.pos, tick)

        if self.targetTornado:
            target = next((t for t in percept.visible_tornadoes if t.unique_id == self.targetTornado), None)
            if target:
                dist = self._get_distance(self.pos, target.pos)
                if dist <= self.safety_distance + 1:
                    self.documentation_progress += 1
                    self.model.log_event(f"{self.name} documenting ({self.documentation_progress}/{self.required_doc_time})")

                    if self.documentation_progress >= self.required_doc_time and not target.documented:
                        doc_target = self.targetTornado
                        self.targetTornado = None
                        self.documentationInProgress = False
                        return self.document(doc_target, tick)
                    return ObserveAction(self.unique_id, timestamp=tick, priority=5)
                else:
                    return self._get_move_towards(target.pos, percept.valid_moves, tick)

        return self.scout(percept.valid_moves, tick)

    def _process_inbox(self):
        for msg in self.inbox:
            if msg.performative == Performative.REQUEST:
                self.targetTornado = msg.content["tornado_id"]
                self.documentation_progress = 0
                self.model.log_event(f"{self.name} assigned to tornado {self.targetTornado}.")
        self.inbox.clear()

    def _get_move_towards(self, target_pos, valid_moves, tick) -> MoveAction:
        safe_steps = []
        for step in valid_moves:
            dist = self._get_distance(step, target_pos)
            if dist > self.safety_distance:
                safe_steps.append(step)

        if safe_steps:
            best = min(safe_steps, key=lambda p: self._get_distance(p, target_pos))
            return MoveAction(self.unique_id, best, timestamp=tick, priority=2)
        return ObserveAction(self.unique_id, timestamp=tick, priority=1)