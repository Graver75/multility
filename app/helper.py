import importlib
import os

def get_modules():
    modules = []
    for moduleDir in os.listdir("modules"):
        if os.path.isdir(os.path.join("modules", moduleDir)):
            modules.append(moduleDir)
    return modules


def get_module_states(module):
    states = []
    for moduleDir in os.listdir("modules/" + module):
        if os.path.isdir(os.path.join("modules/" + module, moduleDir)):
            states.append(moduleDir)
    return states


def get_module_start(module):
    module_path = f"modules.{module}.states.start"
    try:
        start_module = importlib.import_module(module_path)
        return start_module.start
    except ModuleNotFoundError:
        return None