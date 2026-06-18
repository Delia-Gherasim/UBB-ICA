from agents.BaseAgent import BaseAgent
from actions.actions import MoveAction, DissipateAction, ImpactAction
import random

class TornadoAgent(BaseAgent):
    def __init__(self, model, name: str, lifetime: int, movement_mode="random", intensity: int = 5, dissipation_rate: float = 1.0):
        super().__init__(model, name)
        self.lifetime = lifetime
        self.intensity = intensity
        self.dissipationRate = dissipation_rate
        self.active = True
        self.documented = False
        self.movement_mode = movement_mode
        self.driftVector = (random.choice([-1, 0, 1]), random.choice([-1, 0, 1]))
        self.dx, self.dy = self.driftVector

    def move(self, percept, tick) -> MoveAction:
        if self.movement_mode == "drift" and self.pos:
            x, y = self.pos
            new_pos = self.model.grid.normalize((x + self.dx, y + self.dy)) 
            return MoveAction(self.unique_id, new_pos, timestamp=tick, priority=2)
        else:
            if percept.valid_moves:
                return MoveAction(self.unique_id, random.choice(percept.valid_moves), timestamp=tick, priority=2)
        return None

    def dissipate(self, tick) -> DissipateAction:
        return DissipateAction(self.unique_id, timestamp=tick, priority=10)

    def impact(self, town, tick) -> ImpactAction:
        return ImpactAction(self.unique_id, town.name, timestamp=tick, priority=10)

    def step(self, percept):
        if not self.active:
            return None

        tick = percept.current_tick
        self.lifetime -= self.dissipationRate
        
        if self.lifetime <= 0:
            return self.dissipate(tick)

        for agent in percept.cellmates:
            if type(agent).__name__ == "TownAgent" and not getattr(agent, 'impacted', False):
                return self.impact(agent, tick)

        return self.move(percept, tick)