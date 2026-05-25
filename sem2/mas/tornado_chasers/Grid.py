import random

class Grid:
    def __init__(self, width, height, torus=True):
        self.width = width
        self.height = height
        self.torus = torus
        self.cells = {}

    def place_agent(self, agent, pos):
        agent.pos = pos
        self.cells.setdefault(pos, []).append(agent)

    def move_agent(self, agent, new_pos):
        old_pos = agent.pos

        if old_pos in self.cells:
            self.cells[old_pos].remove(agent)

        agent.pos = self.normalize(new_pos)
        self.cells.setdefault(agent.pos, []).append(agent)

    def remove_agent(self, agent):
        if agent.pos in self.cells:
            if agent in self.cells[agent.pos]:
                self.cells[agent.pos].remove(agent)

    def normalize(self, pos):
        x, y = pos

        if self.torus:
            x %= self.width
            y %= self.height

        return x, y

    def get_neighbors(self, pos, radius=1):
        x, y = pos
        neighbors = []

        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if dx == 0 and dy == 0:
                    continue

                nx, ny = self.normalize((x + dx, y + dy))
                neighbors.extend(self.cells.get((nx, ny), []))

        return neighbors

    def get_neighborhood(self, pos):
        x, y = pos
        positions = []

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                positions.append(
                    self.normalize((x + dx, y + dy))
                )

        return positions

    def get_cell_contents(self, pos):
        return self.cells.get(pos, [])