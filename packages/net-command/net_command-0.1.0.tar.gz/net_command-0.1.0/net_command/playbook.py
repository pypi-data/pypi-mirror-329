import re

import yaml

from .parallel_executor import run_tasks


def load_playbook(file_path):
    with open(file_path, "r") as file:
        playbook = yaml.safe_load(file)
    return playbook


def replace_placeholders(text, variables):
    pattern = re.compile(r"{{\s*(\w+)\s*}}")
    if isinstance(text, str):
        return pattern.sub(
            lambda match: str(variables.get(match.group(1), match.group(0))), text
        )
    elif isinstance(text, list):
        return [replace_placeholders(item, variables) for item in text]
    elif isinstance(text, dict):
        return {k: replace_placeholders(v, variables) for k, v in text.items()}
    return text


def execute_playbook(inventory, playbook):
    results = {}
    for task in playbook:
        task_name = task["name"]
        hosts = task["hosts"]
        task_vars = task.get("vars", {})
        devices = []
        for host in inventory[hosts]["hosts"]:
            host_vars = inventory["_meta"]["hostvars"][host]
            if eval(task["tasks"][0]["when"], {}, host_vars):
                host_vars["host"] = host
                device = {
                    "device_type": host_vars["vendor"],
                    "host": host,
                    "username": host_vars["user"],
                    "password": host_vars["password"],
                    "port": int(host_vars["port"]),
                }
                device.update(replace_placeholders(task_vars, host_vars))
                devices.append(device)
        if devices:
            command = replace_placeholders(task["tasks"][0]["commands"], host_vars)
            task_results = run_tasks(devices, command, task.get("num_processes", 4))
            results[task_name] = task_results
    return results
