import mesa
import math
from Message import Message, Performative
from TornadoAgent import TornadoAgent


class ChaserAgent(mesa.Agent):
    def __init__(self, model, chaser_name):
        super().__init__(model)
        self.chaser_name = chaser_name
        self.sight_range = 4
        self.safety_distance = 1
        self.beliefs = {}
        self.desires = ["document_tornadoes"]
        self.intentions = []
        self.inbox = []
        self.target_tornado_id = None
        self.documentation_progress = 0
        self.required_doc_time = 3

        self.active = True

    def step(self):

        if not self.active:
            return

        self._process_inbox()
        visible_agents = self.model.grid.get_neighbors(
            self.pos,
            moore=True,
            include_center=False,
            radius=self.sight_range
        )
        visible_tornadoes = [
            a for a in visible_agents
            if isinstance(a, TornadoAgent) and a.active
        ]

        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        if any(isinstance(a, TornadoAgent) for a in cellmates):
            self.active = False
            self.model.chaser_deaths += 1
            self.model.log_event(
                f"{self.chaser_name} was destroyed by a tornado."
            )
            self.model.grid.remove_agent(self)
            self.remove()
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
                            f"{self.chaser_name} successfully "
                            f"documented {target.tornado_name}."
                        )
                        doc_msg = Message(
                            self.chaser_name,
                            "HQ",
                            Performative.INFORM,
                            {
                                "type": "documented",
                                "tornado_id": target.unique_id
                            }
                        )
                        self.model.send_message(doc_msg)
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
                self.intentions = [
                    f"Track {self.target_tornado_id}"
                ]
                self.model.log_event(
                    f"{self.chaser_name} assigned to "
                    f"{self.target_tornado_id}."
                )
        self.inbox.clear()

    def _move_towards(self, target_pos):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        safe_steps = []
        for step in possible_steps:
            dist = max(
                abs(step[0] - target_pos[0]),
                abs(step[1] - target_pos[1])
            )
            if dist > self.safety_distance:
                safe_steps.append(step)

        if safe_steps:
            best_step = min(
                safe_steps,
                key=lambda p: math.dist(p, target_pos)
            )
            self.model.grid.move_agent(self, best_step)

    def _move_randomly(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        self.model.grid.move_agent(
            self,
            self.random.choice(possible_steps)
        )