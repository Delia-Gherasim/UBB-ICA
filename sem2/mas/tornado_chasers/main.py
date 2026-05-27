from agents.ChaserAgent import ChaserAgent
from agents.HQAgent import HQAgent
from agents.TornadoAgent import TornadoAgent
from agents.TownAgent import TownAgent

from TornadoModel import TornadoModel
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys


MODEL_PARAMS = {
    "width": 20,
    "height": 20,
    "num_chasers": 5,
    "num_tornadoes": 3,
    "num_towns": 4
}

def run_terminal_sim():
    print("Starting simulation (terminal mode)...\n")
    model = TornadoModel(**MODEL_PARAMS, tornado_movement="random", max_steps=100)

    while model.running:
        model.step()

    print("FINAL SIMULATION REPORT")
    print(f"Steps: {model.steps}")
    print(f"Tornadoes Documented: {model.tornadoes_documented} / {model.total_tornadoes}")

    survival_rate = ((MODEL_PARAMS["num_chasers"] - model.chaser_deaths) / MODEL_PARAMS["num_chasers"]) * 100
    print(f"Chaser Survival Rate: {survival_rate:.1f}%")
    print(f"Civilian Casualties: {model.civilian_casualties}")

def run_gui_sim():
    print("Matplotlib window")
    model = TornadoModel(**MODEL_PARAMS, tornado_movement="random", max_steps=100)

    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.manager.set_window_title("Standalone Tornado Hunters MAS")

    def update(frame):
        if not model.running:
            ani.event_source.stop()
            return
        model.step()
        ax.clear()

        ax.set_xlim(-0.5, model.grid.width - 0.5)
        ax.set_ylim(-0.5, model.grid.height - 0.5)
        ax.set_xticks(range(model.grid.width))
        ax.set_yticks(range(model.grid.height))
        ax.grid(color="gray", linestyle="--", linewidth=0.5, alpha=0.5)
        ax.set_title(f"Tornado Hunters | Step: {model.steps} | Documented: {model.tornadoes_documented}/{model.total_tornadoes}")

        for agent in model.agents:
            if agent.pos is None:
                continue
            x, y = agent.pos

            if isinstance(agent, TornadoAgent):
                ax.plot(x, y, marker="X", color="red", markersize=14, linestyle="None", zorder=4)
            elif isinstance(agent, ChaserAgent):
                ax.plot(x, y, marker="o", color="blue", markersize=10, linestyle="None", zorder=3)
            elif isinstance(agent, TownAgent):
                color = "black" if agent.impacted else "gold" if agent.evacuated else "green"
                ax.plot(x, y, marker="s", color=color, markersize=18, linestyle="None", zorder=2)
            elif isinstance(agent, HQAgent):
                ax.plot(x, y, marker="*", color="purple", markersize=22, linestyle="None", zorder=5)

    ani = animation.FuncAnimation(fig, update, interval=500, repeat=False, cache_frame_data=False)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run_terminal_sim()
    else:
        run_gui_sim()