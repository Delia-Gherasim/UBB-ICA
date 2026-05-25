import random

from Grid import Grid
from TornadoAgent import TornadoAgent
from TownAgent import TownAgent
from ChaserAgent import ChaserAgent
from HQAgent import HQAgent


class TornadoModel:
    def __init__(
        self,
        width=20,
        height=20,
        num_chasers=5,
        num_tornadoes=3,
        num_towns=4,
        tornado_movement="random",
        max_steps=100
    ):

        self.grid = Grid(width, height, torus=True)

        self.max_steps = max_steps
        self.running = True
        self.steps = 0

        self.agents = []

        self.event_log = []
        self.communication_log = []

        self.total_tornadoes = num_tornadoes
        self.tornadoes_documented = 0
        self.chaser_deaths = 0
        self.civilian_casualties = 0

        self.hq = HQAgent(self)
        self.add_agent(self.hq, (0, 0))

        for i in range(num_towns):
            town = TownAgent(self, f"Town_{i}")

            self.add_agent(
                town,
                (
                    random.randrange(width),
                    random.randrange(height)
                )
            )

        for i in range(num_chasers):
            chaser = ChaserAgent(self, f"Chaser_{i}")

            self.add_agent(
                chaser,
                (
                    random.randrange(width),
                    random.randrange(height)
                )
            )

        for i in range(num_tornadoes):
            tornado = TornadoAgent(
                self,
                f"Tornado_{i}",
                random.randint(15, 30),
                tornado_movement
            )

            self.add_agent(
                tornado,
                (
                    random.randrange(width),
                    random.randrange(height)
                )
            )

    def add_agent(self, agent, pos):
        self.agents.append(agent)
        self.grid.place_agent(agent, pos)

    def remove_agent(self, agent):
        if agent in self.agents:
            self.agents.remove(agent)

    def send_message(self, msg):
        self.communication_log.append(msg)

        if msg.receiver_id == "HQ":
            self.hq.inbox.append(msg)

    def log_event(self, text):
        entry = f"[Step {self.steps}] {text}"

        self.event_log.append(entry)

        print(entry)

    def step(self):
        random.shuffle(self.agents)

        for agent in self.agents[:]:
            agent.step()

        self.steps += 1

        active_tornadoes = [
            a for a in self.agents
            if isinstance(a, TornadoAgent)
            and a.active
        ]

        if (
            len(active_tornadoes) == 0
            or self.steps >= self.max_steps
        ):
            self.running = False