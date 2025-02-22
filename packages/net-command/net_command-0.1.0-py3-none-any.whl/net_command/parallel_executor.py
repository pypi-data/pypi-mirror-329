from __future__ import annotations

from multiprocessing import Pool
from typing import List, Union

from netmiko import ConnectHandler


def execute_task(device_command_pair):
    device, command = device_command_pair
    connection = ConnectHandler(**device)
    if isinstance(command, list):
        output = [connection.send_command(cmd) for cmd in command]
    else:
        output = connection.send_command(command)
    connection.disconnect()
    return output


def run_tasks(devices, command, num_processes):
    with Pool(processes=num_processes) as pool:
        results = []
        for i, result in enumerate(
            pool.imap_unordered(execute_task, [(device, command) for device in devices])
        ):
            results.append(result)
            print(f"Progress: {i + 1}/{len(devices)} tasks completed")
    return results
