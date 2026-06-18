from typing import List
from agents.BaseAgent import BaseAgent
from State import State
from simulation.Environment import Environment

class Simulation:
    def __init__(self, agents: List['BaseAgent'], environment: Environment):
        self.agents = agents
        self.environment = environment
        self.is_running = False
        self.current_tick = 0
        self.max_ticks = 100

    def start(self, state: State):
        self.environment.set_initial_state(state)
        self.is_running = True

    def stop(self):
        self.is_running = False

    def is_complete(self) -> bool:
        return self.current_tick >= self.max_ticks or not self.is_running

    def run_loop(self):
        while not self.is_complete():
            self.current_tick += 1
            self.environment.advance_time()