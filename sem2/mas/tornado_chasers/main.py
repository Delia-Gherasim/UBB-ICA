# ============================================================
# main.py
# Standalone Tornado Hunter Simulation
# Keeps original Matplotlib visualization
# ============================================================

import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from TornadoModel import TornadoModel
from TornadoAgent import TornadoAgent
from TownAgent import TownAgent
from ChaserAgent import ChaserAgent
from HQAgent import HQAgent


MODEL_PARAMS = {
    "width": 20,
    "height": 20,
    "num_chasers": 5,
    "num_tornadoes": 3,
    "num_towns": 4
}


def run_terminal_sim():
    print("Starting simulation (terminal mode)...\n")

    model = TornadoModel(
        **MODEL_PARAMS,
        tornado_movement="random",
        max_steps=100
    )

    while model.running:
        model.step()

    print("\n================================================")
    print("FINAL SIMULATION REPORT")
    print("================================================")

    print(f"Simulation Steps: {model.steps}")

    print(
        f"Tornadoes Documented: "
        f"{model.tornadoes_documented} / "
        f"{model.total_tornadoes}"
    )

    survival_rate = (
        (
            MODEL_PARAMS["num_chasers"]
            - model.chaser_deaths
        )
        / MODEL_PARAMS["num_chasers"]
    ) * 100

    print(f"Chaser Survival Rate: {survival_rate:.1f}%")
    print(f"Civilian Casualties: {model.civilian_casualties}")
    print(f"Messages Exchanged: {len(model.communication_log)}")

    print("\nEVENT LOG")

    for event in model.event_log:
        print(event)


def run_gui_sim():
    print("Starting Matplotlib visualization window...")

    model = TornadoModel(
        **MODEL_PARAMS,
        tornado_movement="random",
        max_steps=100
    )

    fig, ax = plt.subplots(figsize=(8, 8))

    fig.canvas.manager.set_window_title(
        "Standalone Tornado Hunters MAS"
    )

    def update(frame):

        if not model.running:
            ani.event_source.stop()
            return

        model.step()

        ax.clear()

        # Grid setup
        ax.set_xlim(-0.5, model.grid.width - 0.5)
        ax.set_ylim(-0.5, model.grid.height - 0.5)

        ax.set_xticks(range(model.grid.width))
        ax.set_yticks(range(model.grid.height))

        ax.grid(
            color="gray",
            linestyle="--",
            linewidth=0.5,
            alpha=0.5
        )

        ax.set_title(
            "Tornado Hunters | "
            f"Step: {model.steps} | "
            f"Documented: "
            f"{model.tornadoes_documented}/"
            f"{model.total_tornadoes}"
        )

        # Draw agents
        for agent in model.agents:

            if agent.pos is None:
                continue

            x, y = agent.pos

            # Tornado
            if isinstance(agent, TornadoAgent):

                ax.plot(
                    x,
                    y,
                    marker="X",
                    color="red",
                    markersize=14,
                    linestyle="None",
                    zorder=4
                )

            # Chaser
            elif isinstance(agent, ChaserAgent):

                ax.plot(
                    x,
                    y,
                    marker="o",
                    color="blue",
                    markersize=10,
                    linestyle="None",
                    zorder=3
                )

            # Town
            elif isinstance(agent, TownAgent):

                color = "green"

                if agent.impacted:
                    color = "black"

                elif agent.evacuated:
                    color = "gold"

                ax.plot(
                    x,
                    y,
                    marker="s",
                    color=color,
                    markersize=18,
                    linestyle="None",
                    zorder=2
                )

            # HQ
            elif isinstance(agent, HQAgent):

                ax.plot(
                    x,
                    y,
                    marker="*",
                    color="purple",
                    markersize=22,
                    linestyle="None",
                    zorder=5
                )

    ani = animation.FuncAnimation(
        fig,
        update,
        interval=500,
        repeat=False,
        cache_frame_data=False
    )

    plt.show()

if __name__ == "__main__":

    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run_terminal_sim()
    else:
        run_gui_sim()