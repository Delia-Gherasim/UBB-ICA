from typing import List, Tuple, Dict
from Common.enums import TownStatus
from simulation.GridCell import GridCell
from agents.BaseAgent import BaseAgent

class State:
    def __init__(self, grid_cells: List[List[GridCell]]):
        self.grid: List[List[GridCell]] = grid_cells
        self.current_tick = 0
        self.tornado_positions: Dict[int, Tuple[int, int]] = {}  
        self.chaser_positions: Dict[int, Tuple[int, int]] = {}   
        self.town_states: Dict[str, TownStatus] = {}

    def display(self):
        print(f"State at Tick {self.current_tick}")
        print(f"Active Tornadoes: {len(self.tornado_positions)}")
        print(f"Active Chasers: {len(self.chaser_positions)}")

    def get_information(self) -> Dict:
        return {
            "tick": self.current_tick,
            "tornadoes": self.tornado_positions,
            "chasers": self.chaser_positions,
            "towns": self.town_states
        }

    def update_positions(self, agent: BaseAgent, point: Tuple[int, int]):
        if type(agent).__name__ == "TornadoAgent":
            self.tornado_positions[agent.unique_id] = point
        elif type(agent).__name__ == "ChaserAgent":
            self.chaser_positions[agent.unique_id] = point

    def update_town_state(self, town_name: str, status: TownStatus):
        self.town_states[town_name] = status