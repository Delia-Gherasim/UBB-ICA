import random
from BaseAgent import BaseAgent


class TornadoAgent(BaseAgent):
    def __init__(
        self,
        model,
        tornado_name,
        life_span,
        movement_mode="random"
    ):
        super().__init__(model)

        self.tornado_name = tornado_name
        self.life_span = life_span
        self.active = True
        self.documented = False
        self.movement_mode = movement_mode

        self.dx = random.choice([-1, 0, 1])
        self.dy = random.choice([-1, 0, 1])

    def step(self):
        if not self.active:
            return

        self.life_span -= 1

        if self.life_span <= 0:
            self.active = False
            self.model.log_event(
                f"{self.tornado_name} dissipated."
            )

            self.model.grid.remove_agent(self)
            self.model.remove_agent(self)
            return

        if self.movement_mode == "drift":
            self._drift_move()
        else:
            self._random_move()

    def _random_move(self):
        steps = self.model.grid.get_neighborhood(self.pos)
        new_pos = random.choice(steps)
        self.model.grid.move_agent(self, new_pos)

    def _drift_move(self):
        x, y = self.pos

        new_pos = (
            x + self.dx,
            y + self.dy
        )

        self.model.grid.move_agent(self, new_pos)