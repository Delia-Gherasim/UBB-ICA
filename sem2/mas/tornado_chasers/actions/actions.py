class Action:
    def __init__(self, agent_id: int, timestamp: int = 0, priority: int = 0):
        self.agent_id = agent_id
        self.timestamp = timestamp
        self.priority = priority
#tornado actions:
class DissipateAction(Action):
    def __init__(self, agent_id: int, timestamp: int = 0, priority: int = 0):
        super().__init__(agent_id, timestamp, priority)

class ImpactAction(Action):
    def __init__(self, agent_id: int, target_town_name: str, timestamp: int = 0, priority: int = 0):
        super().__init__(agent_id, timestamp, priority)
        self.target_town_name = target_town_name

class DriftActions(Action):
    def __init__(self, agent_id: int, timestamp: int = 0, priority: int = 0):
        super().__init__(agent_id, timestamp, priority)
    
#chaser actions:
class MoveAction(Action):
    def __init__(self, agent_id: int, target_pos: tuple, timestamp: int = 0, priority: int = 0):
        super().__init__(agent_id, timestamp, priority)
        self.target_pos = target_pos


class DocumentAction(Action):
    def __init__(self, agent_id: int, target_tornado_id: int, timestamp: int = 0, priority: int = 0):
        super().__init__(agent_id, timestamp, priority)
        self.target_tornado_id = target_tornado_id

class EvadeAction(Action):
    def __init__(self, agent_id: int, timestamp: int = 0, priority: int = 0):
        super().__init__(agent_id, timestamp, priority)

class ReportAction(Action):
    def __init__(self, agent_id: int, content: dict, timestamp: int = 0, priority: int = 0):
        super().__init__(agent_id, timestamp, priority)
        self.content = content

#hq actions:
class AssignAction(Action):
    def __init__(self, agent_id: int, timestamp: int = 0, priority: int = 0):
        super().__init__(agent_id, timestamp, priority)

class ObserveAction(Action):
    def __init__(self, agent_id: int, timestamp: int = 0, priority: int = 0):
        super().__init__(agent_id, timestamp, priority)

class WarnAction(Action):
    def __init__(self, agent_id: int, target_agent_name: str, timestamp: int = 0, priority: int = 0):
        super().__init__(agent_id, timestamp, priority)
        self.target_agent_name = target_agent_name

class EvacuateAction(Action):
    def __init__(self, agent_id: int, timestamp: int = 0, priority: int = 0):
        super().__init__(agent_id, timestamp, priority)

class RequestAction(Action):
    def __init__(self, agent_id: int, content: dict, timestamp: int = 0, priority: int = 0):
        super().__init__(agent_id, timestamp, priority)
        self.content = content
