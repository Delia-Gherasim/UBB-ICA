import mesa
from TornadoAgent import TornadoAgent
from TownAgent import TownAgent
from ChaserAgent import ChaserAgent
from HQAgent import HQAgent

class TornadoModel(mesa.Model):
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
        super().__init__()
        self.grid = mesa.space.MultiGrid(
            width,
            height,
            torus=True
        )
        self.max_steps = max_steps
        self.num_chasers = num_chasers
        self.total_tornadoes = num_tornadoes
        self.tornadoes_documented = 0
        self.chaser_deaths = 0
        self.civilian_casualties = 0
        self.event_log = []
        self.communication_log = []
        self.hq = HQAgent(self)
        self.grid.place_agent(self.hq, (0, 0))
        self.running = True

        for i in range(num_towns):
            town = TownAgent(
                self,
                f"Town_{i}"
            )
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(town, (x, y))

        for i in range(num_chasers):
            chaser = ChaserAgent(
                self,
                f"Chaser_{i}"
            )
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(chaser, (x, y))

        for i in range(num_tornadoes):
            tornado = TornadoAgent(
                self,
                tornado_name=f"Tornado_{i}",
                life_span=self.random.randint(15, 30),
                movement_mode=tornado_movement
            )
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(tornado, (x, y))

        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Documented":
                    lambda m: m.tornadoes_documented,
                "Survival_Rate":
                    lambda m: (
                        (
                            m.num_chasers
                            - m.chaser_deaths
                        ) / m.num_chasers
                    ),
                "Civilian_Casualties":
                    lambda m: m.civilian_casualties
            }
        )

    def log_event(self, text):
        entry = f"[Step {self.steps}] {text}"
        self.event_log.append(entry)
        print(entry)

    def send_message(self, msg):
        self.communication_log.append(msg)
        if msg.receiver_id == "HQ":
            self.hq.inbox.append(msg)

    def step(self):
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")
        active_tornadoes = [
            a for a in self.agents
            if isinstance(a, TornadoAgent)
            and a.active
        ]
        if (len(active_tornadoes) == 0 or self.steps >= self.max_steps):
            self.running = False