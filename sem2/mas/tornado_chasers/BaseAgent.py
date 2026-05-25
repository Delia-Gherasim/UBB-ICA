import itertools


class BaseAgent:
    _id_counter = itertools.count()

    def __init__(self, model):
        self.unique_id = next(BaseAgent._id_counter)
        self.model = model
        self.pos = None

    def step(self):
        pass