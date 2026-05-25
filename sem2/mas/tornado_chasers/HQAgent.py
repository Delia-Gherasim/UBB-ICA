import math

from BaseAgent import BaseAgent
from TownAgent import TownAgent
from ChaserAgent import ChaserAgent
from Message import Message, Performative


class HQAgent(BaseAgent):
    def __init__(self, model):
        super().__init__(model)

        self.inbox = []
        self.threat_map = {}
        self.assignments = {}

    def step(self):
        for msg in self.inbox:

            if msg.performative == Performative.INFORM:

                if msg.content["type"] == "sighting":

                    t_id = msg.content["tornado_id"]
                    t_pos = msg.content["pos"]

                    self.threat_map[t_id] = t_pos

                    self.model.log_event(
                        f"HQ received sighting."
                    )

                    self._check_town_proximity(t_pos)

        self.inbox.clear()

        self._delegate_tasks()

    def _check_town_proximity(self, tornado_pos):
        for agent in self.model.agents:

            if isinstance(agent, TownAgent):

                dist = max(
                    abs(agent.pos[0] - tornado_pos[0]),
                    abs(agent.pos[1] - tornado_pos[1])
                )

                if dist <= 4 and not agent.evacuated:

                    warn = Message(
                        "HQ",
                        agent.name,
                        Performative.WARN,
                        "EVACUATE"
                    )

                    agent.inbox.append(warn)

                    self.model.log_event(
                        f"HQ warned {agent.name}"
                    )

    def _delegate_tasks(self):
        monitored = set(self.assignments.keys())

        unmonitored = [
            t for t in self.threat_map
            if t not in monitored
        ]

        available = [
            a for a in self.model.agents
            if isinstance(a, ChaserAgent)
            and a.active
            and a.target_tornado_id is None
        ]

        for t_id in unmonitored:

            if available:

                tornado_pos = self.threat_map[t_id]

                chaser = min(
                    available,
                    key=lambda c: math.dist(
                        c.pos,
                        tornado_pos
                    )
                )

                available.remove(chaser)

                self.assignments[t_id] = chaser.chaser_name

                msg = Message(
                    "HQ",
                    chaser.chaser_name,
                    Performative.REQUEST,
                    {
                        "tornado_id": t_id
                    }
                )

                chaser.inbox.append(msg)

                self.model.log_event(
                    f"HQ assigned {chaser.chaser_name}"
                )