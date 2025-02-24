
def circularDependenciesError(logs: dict, logs_path: tuple):
    logs["run"] += 1
    logs["error"] = "循环依赖"
    logs["data"] = logs_path
