import mesa
import random

class TornadoAgent(mesa.Agent):
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
            self.remove()
            return
        if self.movement_mode == "drift":
            self._drift_move()
        else:
            self._random_move()

    def _random_move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    def _drift_move(self):
        x, y = self.pos
        new_x = (x + self.dx) % self.model.grid.width
        new_y = (y + self.dy) % self.model.grid.height
        self.model.grid.move_agent(self, (new_x, new_y))