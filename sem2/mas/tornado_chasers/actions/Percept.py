from typing import List, Dict
from message.Message import Message
from simulation.State import State

class Percept:
    def __init__(self, state: State, agent):
        self.pos = agent.pos
        self.current_tick = state.current_tick
        self.valid_moves = state.grid.get_neighborhood(agent.pos) if agent.pos else []
        self.cellmates = state.grid.get_cell_contents(agent.pos) if agent.pos else []
        self.received_messages: List[Message] = list(agent.inbox)
        
        if hasattr(agent, 'visibilityRange') and agent.pos:
            visible = state.grid.get_neighbors(agent.pos, radius=agent.visibilityRange)
            self.visible_tornadoes = [a for a in visible if type(a).__name__ == "TornadoAgent" and a.active]
            self.visible_agents = [a for a in visible if type(a).__name__ == "ChaserAgent"]
        else:
            self.visible_tornadoes = []
            self.visible_agents = []