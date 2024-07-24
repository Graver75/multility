import os

def getModules():
    modules = []
    for moduleDir in os.listdir("modules"):
        if os.path.isdir(os.path.join("modules", moduleDir)):
            modules.append(moduleDir)
    return modules


def getModuleStates(module):
    states = []
    for moduleDir in os.listdir("modules/" + module):
        if os.path.isdir(os.path.join("modules/" + module, moduleDir)):
            states.append(moduleDir)
    return states

