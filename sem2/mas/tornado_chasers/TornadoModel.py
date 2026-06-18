import random
from Grid import Grid
from message.MessageOrchestrator import MessageOrchestrator
from agents.TornadoAgent import TornadoAgent
from agents.TownAgent import TownAgent
from agents.ChaserAgent import ChaserAgent
from agents.HQAgent import HQAgent
from simulation.Environment import Environment

class TornadoModel:
    def __init__(self, width, height, num_chasers, num_tornadoes, num_towns, tornado_movement, max_steps):
        self.grid = Grid(width, height, torus=True)
        self.max_steps = max_steps
        self.running = True
        self.steps = 0
        self.agents = []
        
        self.event_log = []
        self.msg_orchestrator = MessageOrchestrator()
        
        self.environment = Environment(self.grid, self)

        self.total_tornadoes = num_tornadoes
        self.tornadoes_documented = 0
        self.chaser_deaths = 0
        self.civilian_casualties = 0

        self.hq = HQAgent(self, "HQ")
        self.add_agent(self.hq, (0, 0))

        for i in range(num_towns):
            town = TownAgent(self, f"Town_{i}")
            self.add_agent(town, (random.randrange(width), random.randrange(height)))

        for i in range(num_chasers):
            chaser = ChaserAgent(self, f"Chaser_{i}")
            self.add_agent(chaser, (random.randrange(width), random.randrange(height)))

        for i in range(num_tornadoes):
            tornado = TornadoAgent(self, f"Tornado_{i}", random.randint(10, 100), tornado_movement)
            self.add_agent(tornado, (random.randrange(width), random.randrange(height)))

    def add_agent(self, agent, pos):
        self.agents.append(agent)
        self.grid.place_agent(agent, pos)
        self.msg_orchestrator.register(agent)

    def remove_agent(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)
            self.msg_orchestrator.unregister(agent)

    def get_agent_by_id(self, agent_id: int):
        return next((a for a in self.agents if a.unique_id == agent_id), None)

    def log_event(self, text):
        entry = f"[Step {self.steps}] {text}"
        self.event_log.append(entry)
        print(entry)

    def step(self):
        random.shuffle(self.agents)
        actions = []
        
        for agent in self.agents[:]:
            if agent.pos is None and agent.name != "HQ":
                continue 
                
            percept = self.environment.get_percept(agent, self.environment.state)
            action = agent.step(percept)
            if action:
                actions.append(action)

        self.environment.resolve_actions(actions)
        self.environment.advance_time()
        
        self.steps += 1
        active_tornadoes = [a for a in self.agents if isinstance(a, TornadoAgent) and a.active]

        if len(active_tornadoes) == 0 or self.steps >= self.max_steps:
            self.running = False