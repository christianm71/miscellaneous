import argparse

from Tools import create_parser

# ----- dictionary of arguments -----
args_dict = {
    "args": [
        ("--debug", dict(help="Enable debug mode", action="store_true", default=False)),
    ],
    "commands": {
        "users": {
            "help": "Manage users",
            "args": [
                ("--id", dict(help="The user ID")),
                ("--name", dict(help="The user name")),
            ],
        },
        "profiles": {
            "help": "Manage profiles",
            "args": [
                ("--id", dict(help="The profile ID")),
                ("--name", dict(help="The user name")),
            ],
        },
    }
}

# ----- main -----
parser = argparse.ArgumentParser(description="Example with commands 1 level")

parsers = create_parser(parser, args_dict)

args = parser.parse_args()

if args.command1 == "users":
    print(f"command1 = {args.command1}")
elif args.command1 == "profiles":
    print(f"command1 = {args.command1}")
else:
    parser.print_help()

