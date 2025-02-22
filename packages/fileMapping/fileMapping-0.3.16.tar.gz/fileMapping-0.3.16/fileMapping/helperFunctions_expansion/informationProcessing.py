"""
信息处理模块

"""
import re
from collections import defaultdict, deque

from ..information import fileMappingConfig


def get_all(text: str):
    """
    获取文件全部信息

    :param text: 文本内容
    :return: 文件全部信息
    """
    return {
        "__level__": get_file_level(text),
        "__underlying__": get_file_underlying(text),
        "__dependenciesOnPlugins__": get_file_dependencies_on_plugins(text)
    }


def get_file_underlying(text: str):
    """
    获取文件底层信息

    :param text: 文本内容
    :return: 文件底层信息
    """

    match = re.search(pattern["__underlying__"], text)
    return match.group(1) if match else fileMappingConfig.functions["__underlying__"]


def get_file_dependencies_on_plugins(text: str):
    """
    获取文件依赖插件信息

    :param text: 文本内容
    :return: 文件依赖插件信息
    """
    # 使用 re.DOTALL 标志让 . 能匹配换行符
    match = re.search(pattern["__dependenciesOnPlugins__"], text, re.DOTALL)
    if match:
        dependencies_on_plugins = match.group(1)
        dependencies_on_plugins = dependencies_on_plugins.replace("'", "\"")
        dependencies_on_plugins = eval(dependencies_on_plugins)
        return dependencies_on_plugins
    else:
        match = re.search(pattern["__dependenciesOnPluginsList__"], text, re.DOTALL)
        if match:
            dependencies_on_plugins = match.group(1)
            dependencies_on_plugins = dependencies_on_plugins.replace("'", "\"")
            dependencies_on_plugins = eval(dependencies_on_plugins)
            return dependencies_on_plugins
        else:
            return fileMappingConfig.functions["__dependenciesOnPlugins__"]


def get_file_level(text: str):
    """
    获取文件层级信息

    :param text: 文本内容
    :return: 文件层级信息
    """
    match = re.search(pattern["__level__"], text)
    return int(match.group(1)) if match else fileMappingConfig.functions["__level__"]


pattern = {
    "__underlying__": r"__underlying__\s*=\s*(\w+)",
    "__dependenciesOnPlugins__": r"__dependenciesOnPlugins__\s*=\s*(\{.*?\})",
    "__dependenciesOnPluginsList__": r"__dependenciesOnPlugins__\s*=\s*(\[.*?\])",
    "__level__": r"__level__\s*=\s*(\d+)"
}


def sorting_plugin(plugin_dict: dict[str, dict]):
    """
    排序插件
    应该按照插件的层级和依赖关系来排序
    按照任务执行标准来排序

    :param plugin_dict: 插件字典
    :return: 任务执行顺序字典或包含循环依赖插件的列表
    """
    in_degree = {plugin: 0 for plugin in plugin_dict}
    graph = defaultdict(list)
    for plugin, info in plugin_dict.items():
        dependencies = info.get("__dependenciesOnPlugins__", [])
        if isinstance(dependencies, dict):
            dependencies = list(dependencies.keys())
        for dep in dependencies:
            if dep in plugin_dict:
                graph[dep].append(plugin)
                in_degree[plugin] += 1

    queue = deque([plugin for plugin, degree in in_degree.items() if degree == 0])
    sorted_order = []
    while queue:
        plugin = queue.popleft()
        sorted_order.append(plugin)
        for neighbor in graph[plugin]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # 检查是否存在循环依赖
    remaining_nodes = [plugin for plugin, degree in in_degree.items() if degree > 0]
    if remaining_nodes:
        def dfs(node, path, visited):
            if node in path:
                index = path.index(node)
                return path[index:]
            if node in visited:
                return []
            visited.add(node)
            path.append(node)
            for neighbor in graph[node]:
                cycle = dfs(neighbor, path, visited)
                if cycle:
                    return cycle
            path.pop()
            return []

        cycle = []
        for node in remaining_nodes:
            cycle = dfs(node, [], set())
            if cycle:
                break

        return tuple(cycle)

    level_result = defaultdict(list)
    for plugin in sorted_order:
        level = plugin_dict[plugin]["__level__"]
        level_result[level].append(plugin)

    for level in level_result:
        level_result[level].sort(key=lambda x: plugin_dict[x]["__level__"], reverse=True)

    final_result = dict(sorted(level_result.items(), reverse=True))
    return final_result


def get_file_info(file_object: object, info: dict) -> dict:
    """
    获取文件信息
    :param file_object: 文件对象
    :param info: 文件信息字典 {infoName: messageDefaults, ...}
    :return: 文件信息字典 {infoName: message, ...}
    """
    if info is None:  # info 不为空
        return {}

    attribute = dir(file_object)
    return {
        key: getattr(file_object, key)if key in attribute else value for key, value in info.items()
    }
