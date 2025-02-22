import argparse
import json
import sys

from .inventory import load_inventory
from .playbook import load_playbook, execute_playbook
from .output_handler import print_output


def main():
    parser = argparse.ArgumentParser(description="Net Command CLI")
    parser.add_argument(
        "-i", "--inventory", required=True, help="Path to inventory file"
    )
    parser.add_argument("playbook", nargs="?", help="Path to playbook file")
    parser.add_argument("--list", action="store_true", help="List inventory as JSON")

    args = parser.parse_args()

    inventory = load_inventory(args.inventory)

    if args.list:
        print(json.dumps(inventory, indent=2))
        sys.exit(0)

    if args.playbook:
        playbook = load_playbook(args.playbook)
        results = execute_playbook(inventory, playbook)
        print_output(results)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
