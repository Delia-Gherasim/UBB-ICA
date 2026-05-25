from BaseAgent import BaseAgent
from TornadoAgent import TornadoAgent
from Message import Performative


class TownAgent(BaseAgent):
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
                    f"{self.name} evacuated."
                )

        self.inbox.clear()

        cellmates = self.model.grid.get_cell_contents(self.pos)

        for agent in cellmates:
            if isinstance(agent, TornadoAgent):
                self.impacted = True

                if not self.evacuated:
                    self.model.civilian_casualties += 1

                    self.model.log_event(
                        f"{self.name} hit without evacuation."
                    )
                else:
                    self.model.log_event(
                        f"{self.name} safely evacuated."
                    )

                break