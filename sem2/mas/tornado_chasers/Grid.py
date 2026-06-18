import matplotlib.pyplot as plt
import matplotlib.animation as animation

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
        agent.pos = None

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
                positions.append(self.normalize((x + dx, y + dy)))
        return positions

    def get_cell_contents(self, pos):
        return self.cells.get(pos, [])

    def run_gui(self, model):
        fig, ax = plt.subplots(figsize=(8, 8))
        fig.canvas.manager.set_window_title("Standalone Tornado Hunters MAS")

        def update(frame):
            if not model.running:
                ani.event_source.stop()
                return
            model.step()
            ax.clear()

            ax.set_xlim(-0.5, self.width - 0.5)
            ax.set_ylim(-0.5, self.height - 0.5)
            ax.set_xticks(range(self.width))
            ax.set_yticks(range(self.height))
            ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)
            ax.set_title(f"Tornado Hunters | Step: {model.steps} | Documented: {model.tornadoes_documented}/{model.total_tornadoes}")

            for agent in model.agents:
                if agent.pos is None:
                    continue
                x, y = agent.pos
                
                agent_type = type(agent).__name__

                if agent_type == "TornadoAgent":
                    is_sighted = agent.unique_id in model.hq.threatMap
                    if getattr(agent, 'documented', False):
                        t_color = "darkred" 
                    elif is_sighted:
                        t_color = "orange"  
                    else:
                        t_color = "red"     
                    ax.plot(x, y, marker="X", color=t_color, markersize=14, linestyle="None", zorder=4)
                elif agent_type == "ChaserAgent":
                    ax.plot(x, y, marker="o", color="blue", markersize=10, linestyle="None", zorder=3)
                elif agent_type == "TownAgent":
                    color = "black" if getattr(agent, 'impacted', False) else "gold" if getattr(agent, 'evacuated', False) else "green"
                    ax.plot(x, y, marker="s", color=color, markersize=18, linestyle="None", zorder=2)
                elif agent_type == "HQAgent":
                    ax.plot(x, y, marker="*", color="purple", markersize=22, linestyle="None", zorder=5)

        ani = animation.FuncAnimation(fig, update, interval=500, repeat=False, cache_frame_data=False)
        plt.show()