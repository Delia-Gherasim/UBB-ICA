import sys
from TornadoModel import TornadoModel

MODEL_PARAMS = {
    "width": 20,
    "height": 20,
    "num_chasers": 3,
    "num_tornadoes": 5,
    "num_towns": 4,
    "tornado_movement": "random",
    "max_steps": 200
}
  

if __name__ == "__main__":
    # model = TornadoModel(**MODEL_PARAMS)

    # while model.running:
    #     model.step()
    model = TornadoModel(**MODEL_PARAMS)
    model.grid.run_gui(model)
    print("FINAL SIMULATION REPORT")
    print(f"Steps: {model.steps}")
    print(f"Tornadoes Documented: {model.tornadoes_documented} / {model.total_tornadoes}")