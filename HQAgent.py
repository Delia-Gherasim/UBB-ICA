import mesa
import math
from Message import Message, Performative
from TownAgent import TownAgent
from ChaserAgent import ChaserAgent


class HQAgent(mesa.Agent):
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
                        f"HQ received sighting of "
                        f"{msg.content['tornado_name']} "
                        f"from {msg.sender_id}."
                    )
                    self._check_town_proximity(t_pos)

                elif msg.content["type"] == "documented":
                    t_id = msg.content["tornado_id"]
                    if t_id in self.threat_map:
                        del self.threat_map[t_id]
                    if t_id in self.assignments:
                        del self.assignments[t_id]
                    self.model.log_event(
                        f"HQ confirmed documentation of {t_id}."
                    )
        self.inbox.clear()
        self._delegate_tasks()

    def _check_town_proximity(self, tornado_pos):
        for agent in self.model.agents:
            if isinstance(agent, TownAgent):
                if agent.evacuated:
                    continue
                dist = max(
                    abs(agent.pos[0] - tornado_pos[0]),
                    abs(agent.pos[1] - tornado_pos[1])
                )

                if dist <= 4:
                    warn_msg = Message(
                        "HQ",
                        agent.name,
                        Performative.WARN,
                        "EVACUATE"
                    )
                    agent.inbox.append(warn_msg)
                    self.model.communication_log.append(warn_msg)
                    self.model.log_event(
                        f"HQ issued evacuation warning "
                        f"to {agent.name}."
                    )

    def _delegate_tasks(self):
        monitored_tornadoes = set(self.assignments.keys())
        unmonitored = [
            t_id
            for t_id in self.threat_map.keys()
            if t_id not in monitored_tornadoes
        ]
        available_chasers = [
            a for a in self.model.agents
            if (
                isinstance(a, ChaserAgent)
                and a.active
                and a.target_tornado_id is None
            )
        ]

        for t_id in unmonitored:
            if available_chasers:
                tornado_pos = self.threat_map[t_id]
                chaser = min(
                    available_chasers,
                    key=lambda c: math.dist(c.pos, tornado_pos)
                )
                available_chasers.remove(chaser)
                self.assignments[t_id] = chaser.chaser_name
                assign_msg = Message(
                    "HQ",
                    chaser.chaser_name,
                    Performative.REQUEST,
                    {
                        "tornado_id": t_id
                    }
                )
                chaser.inbox.append(assign_msg)
                self.model.communication_log.append(assign_msg)
                self.model.log_event(
                    f"HQ assigned {chaser.chaser_name} "
                    f"to tornado {t_id}."
                )