from typing import List
import random
from actions.Percept import Percept
from simulation.State import State
from simulation.Town import Town
from Common.enums import TownStatus
from actions.actions import *

class Environment:
    def __init__(self, grid_cells, model):
        self.state: State = State(grid_cells)
        self.model = model
        self.msg_orchestrator = model.msg_orchestrator
        self.towns: List[Town] = []
        self.active_tornadoes: List[int] = []

    def get_percept(self, agent, state: State) -> Percept:
        return Percept(state, agent)

    def resolve_actions(self, actions: List[Action]):
        move_intents = {}
        for action in actions:
            if isinstance(action, MoveAction):
                move_intents.setdefault(action.target_pos, []).append(action)

        for target_pos, intent_list in move_intents.items():
            if len(intent_list) == 1:
                agent = self.model.get_agent_by_id(intent_list[0].agent_id)
                self.update_state(agent, intent_list[0])
            else:
                winner_action = random.choice(intent_list)
                agent = self.model.get_agent_by_id(winner_action.agent_id)
                self.update_state(agent, winner_action)

        for action in actions:
            if not isinstance(action, MoveAction):
                agent = self.model.get_agent_by_id(action.agent_id)
                if agent:
                    self.update_state(agent, action)

    def update_state(self, agent, action: Action):
        if isinstance(action, MoveAction):
            self.model.grid.move_agent(agent, action.target_pos)
            self.state.update_positions(agent, action.target_pos)

        elif isinstance(action, DissipateAction):
            agent.active = False
            self.model.grid.remove_agent(agent)
            
            if type(agent).__name__ == "TornadoAgent":
                if agent.unique_id in self.active_tornadoes:
                    self.active_tornadoes.remove(agent.unique_id)
                self.model.log_event(f"{agent.name} dissipated.")
            elif type(agent).__name__ == "ChaserAgent":
                self.model.chaser_deaths += 1
                self.model.log_event(f"{agent.name} destroyed.")

        elif isinstance(action, DocumentAction):
            target = self.model.get_agent_by_id(action.target_tornado_id)
            if target and not getattr(target, 'documented', False):
                target.documented = True
                self.model.tornadoes_documented += 1
                self.model.log_event(f"{target.name} documented.")

        elif isinstance(action, ImpactAction):
            town_agent = next((a for a in self.model.agents if a.name == action.target_town_name), None)
            
            if town_agent:
                town_agent.impacted = True
                town_obj = next((t for t in self.towns if t.name == town_agent.name), None)
                new_status = TownStatus.DESTROYED if not town_agent.evacuated else TownStatus.IMPACTED
                
                if town_obj:
                    town_obj.update_status(new_status)
                self.state.update_town_state(town_agent.name, new_status)

                if not town_agent.evacuated:
                    self.model.civilian_casualties += 1
                    self.model.log_event(f"{town_agent.name} hit by {agent.name} without evacuation.")
                else:
                    self.model.log_event(f"{town_agent.name} safely evacuated but took structural damage from {agent.name}.")

        elif isinstance(action, EvadeAction):
            agent.evacuated = True
            self.model.log_event(f"{agent.name} evacuated.")

            town_obj = next((t for t in self.towns if t.name == agent.name), None)
            if town_obj:
                town_obj.update_status(TownStatus.EVACUATING)
            self.state.update_town_state(agent.name, TownStatus.EVACUATING)

    def set_initial_state(self, state: State):
        self.state = state

    def current_state(self) -> State:
        return self.state

    def advance_time(self):
        self.state.current_tick += 1

    def spawn_tornado(self):
        pass