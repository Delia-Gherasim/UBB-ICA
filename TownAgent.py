import mesa
from Message import Performative
from TornadoAgent import TornadoAgent

class TownAgent(mesa.Agent):
    def __init__(self, model, name):
        super().__init__(model)
        self.name = name
        self.evacuated = False
        self.impacted = False
        self.inbox = []

    def step(self):
        for msg in self.inbox:
            if msg.performative == Performative.WARN:
                self.evacuated = True
                self.model.log_event(
                    f"{self.name} received evacuation warning from HQ."
                )
        self.inbox.clear()
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in cellmates:
            if isinstance(agent, TornadoAgent):
                self.impacted = True
                if not self.evacuated:
                    self.model.civilian_casualties += 1
                    self.model.log_event(
                        f"{self.name} was impacted by tornado "
                        f"{agent.tornado_name} WITHOUT evacuation."
                    )
                else:
                    self.model.log_event(
                        f"{self.name} was impacted, "
                        f"but evacuation succeeded."
                    )
                break