import math
import random

from BaseAgent import BaseAgent
from TornadoAgent import TornadoAgent
from Message import Message, Performative


class ChaserAgent(BaseAgent):
    def __init__(self, model, chaser_name):
        super().__init__(model)

        self.chaser_name = chaser_name

        self.sight_range = 4
        self.safety_distance = 1

        self.beliefs = {}
        self.inbox = []

        self.target_tornado_id = None
        self.documentation_progress = 0
        self.required_doc_time = 3

        self.active = True

    def step(self):
        if not self.active:
            return

        self._process_inbox()

        visible = self.model.grid.get_neighbors(
            self.pos,
            radius=self.sight_range
        )

        visible_tornadoes = [
            a for a in visible
            if isinstance(a, TornadoAgent)
            and a.active
        ]

        cellmates = self.model.grid.get_cell_contents(self.pos)

        if any(isinstance(a, TornadoAgent) for a in cellmates):
            self.active = False

            self.model.chaser_deaths += 1

            self.model.log_event(
                f"{self.chaser_name} destroyed."
            )

            self.model.grid.remove_agent(self)
            self.model.remove_agent(self)
            return

        for tornado in visible_tornadoes:
            self.beliefs[tornado.unique_id] = tornado.pos

            msg = Message(
                self.chaser_name,
                "HQ",
                Performative.INFORM,
                {
                    "type": "sighting",
                    "tornado_id": tornado.unique_id,
                    "tornado_name": tornado.tornado_name,
                    "pos": tornado.pos
                }
            )

            self.model.send_message(msg)

        if self.target_tornado_id:
            target = next(
                (
                    t for t in visible_tornadoes
                    if t.unique_id == self.target_tornado_id
                ),
                None
            )

            if target:
                dist = max(
                    abs(self.pos[0] - target.pos[0]),
                    abs(self.pos[1] - target.pos[1])
                )

                if dist <= self.safety_distance + 1:
                    self.documentation_progress += 1

                    self.model.log_event(
                        f"{self.chaser_name} documenting "
                        f"{target.tornado_name} "
                        f"({self.documentation_progress}/"
                        f"{self.required_doc_time})"
                    )

                    if (
                        self.documentation_progress
                        >= self.required_doc_time
                        and not target.documented
                    ):
                        target.documented = True

                        self.model.tornadoes_documented += 1

                        self.model.log_event(
                            f"{target.tornado_name} documented."
                        )

                        self.target_tornado_id = None

                else:
                    self._move_towards(target.pos)

            else:
                self._move_randomly()

        else:
            self._move_randomly()

    def _process_inbox(self):
        for msg in self.inbox:
            if msg.performative == Performative.REQUEST:
                self.target_tornado_id = msg.content["tornado_id"]
                self.documentation_progress = 0

                self.model.log_event(
                    f"{self.chaser_name} assigned."
                )

        self.inbox.clear()

    def _move_towards(self, target_pos):
        steps = self.model.grid.get_neighborhood(self.pos)

        safe_steps = []

        for step in steps:
            dist = max(
                abs(step[0] - target_pos[0]),
                abs(step[1] - target_pos[1])
            )

            if dist > self.safety_distance:
                safe_steps.append(step)

        if safe_steps:
            best = min(
                safe_steps,
                key=lambda p: math.dist(p, target_pos)
            )

            self.model.grid.move_agent(self, best)

    def _move_randomly(self):
        steps = self.model.grid.get_neighborhood(self.pos)
        self.model.grid.move_agent(
            self,
            random.choice(steps)
        )