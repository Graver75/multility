import importlib
import os

def get_modules():
    modules = []
    for moduleDir in os.listdir("modules"):
        if os.path.isdir(os.path.join("modules", moduleDir)):
            modules.append(moduleDir)
    return modules


def get_module_states(module):
    states_path = f"modules.{module}.states"
    states = importlib.import_module(states_path)
    return states.states


def get_module_start(module):
    module_path = f"modules.{module}.states.start"
    try:
        start_module = importlib.import_module(module_path)
        return start_module.start
    except ModuleNotFoundError:
        return None