import yaml


def load_inventory(file_path):
    with open(file_path, "r") as file:
        inventory = yaml.safe_load(file)

    hostvars = {}
    for group, group_data in inventory.items():
        if group == "all":
            vars = group_data.get("vars", {})
        else:
            for host in group_data.get("hosts", []):
                hostvars[host] = vars

    for host in hostvars:
        hostvars[host].update(vars)

    result = {
        "_meta": {"hostvars": hostvars},
        "all": {"children": list(inventory.keys())},
    }

    for group, group_data in inventory.items():
        if group != "all":
            result[group] = {"hosts": list(group_data.get("hosts", {}).keys())}

    return result
