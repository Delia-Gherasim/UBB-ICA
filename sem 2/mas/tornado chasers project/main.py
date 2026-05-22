import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from TornadoAgent import TornadoAgent
from TownAgent import TownAgent
from ChaserAgent import ChaserAgent
from HQAgent import HQAgent
from TornadoModel import TornadoModel

model_params = {
    "width": 20,
    "height": 20,
    "num_chasers": 5,
    "num_tornadoes": 3,
    "num_towns": 4
}

def run_terminal_sim():
    print("Start simulation (terminal mode)...")

    model = TornadoModel(**model_params, tornado_movement="random", max_steps=100)

    while model.running:
        model.step()

    df = model.datacollector.get_model_vars_dataframe()
    final_stats = df.iloc[-1]

    print("\n================================================")
    print("FINAL SIMULATION REPORT")
    print("================================================")
    print(f"Simulation Steps: {model.steps}")
    print(f"Tornadoes Documented: {final_stats['Documented']} / {model.total_tornadoes}")
    print(f"Chaser Survival Rate: {final_stats['Survival_Rate'] * 100:.1f}%")
    print(f"Civilian Casualties: {final_stats['Civilian_Casualties']}")
    print(f"Messages Exchanged: {len(model.communication_log)}")

    print("\nEVENT LOG")
    for event in model.event_log:
        print(event)

def run_gui_sim():
    print("Starting Matplotlib visualization window...")
    
    model = TornadoModel(**model_params, tornado_movement="random", max_steps=100)
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.canvas.manager.set_window_title('SP2 Tornado Hunters MAS')

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
        ax.grid(color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
        ax.set_title(f"Tornado Hunters | Step: {model.steps} | Documented: {model.tornadoes_documented}/{model.total_tornadoes}")

        for agent in model.agents:
            if not hasattr(agent, "pos") or agent.pos is None:
                continue
                
            x, y = agent.pos

            if isinstance(agent, TornadoAgent):
                ax.plot(x, y, marker='X', color='red', markersize=14, linestyle='None', zorder=4)
            
            elif isinstance(agent, ChaserAgent):
                ax.plot(x, y, marker='o', color='blue', markersize=10, linestyle='None', zorder=3)
            
            elif isinstance(agent, TownAgent):
                color = "green"
                if agent.impacted:
                    color = "black"
                elif agent.evacuated:
                    color = "gold"
                ax.plot(x, y, marker='s', color=color, markersize=18, linestyle='None', zorder=2)
            
            elif isinstance(agent, HQAgent):
                ax.plot(x, y, marker='*', color='purple', markersize=22, linestyle='None', zorder=5)

    ani = animation.FuncAnimation(
        fig, update, interval=500, repeat=False, cache_frame_data=False
    )
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        run_terminal_sim()
    else:
        run_gui_sim()