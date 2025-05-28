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
            "commands": {
                "create": {
                    "help": "Create an user",
                    "args": [
                        ("--id", dict(help="The user ID")),
                    ],
                },
                "delete": {
                    "help": "Delete an user",
                    "args": [
                        ("--id", dict(help="The user ID")),
                    ],
                },
            },
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
parser = argparse.ArgumentParser(description="Example with commands 2 level")

parsers = create_parser(parser, args_dict)

import sys

# Store the original sys.argv
original_argv = sys.argv

def test_users_create_command():
    sys.argv = ['test_Tools_2.py', 'users', 'create', '--id', '3']
    args = parser.parse_args()
    assert args.command1 == "users"
    assert args.command2 == "create"
    assert args.id == "3"
    assert args.debug == False # Default value

def test_debug_users_delete_command():
    sys.argv = ['test_Tools_2.py', '--debug', 'users', 'delete', '--id', '4']
    args = parser.parse_args()
    assert args.debug == True
    assert args.command1 == "users"
    assert args.command2 == "delete"
    assert args.id == "4"

def test_profiles_command():
    sys.argv = ['test_Tools_2.py', 'profiles', '--id', '5', '--name', 'anotherprofile']
    args = parser.parse_args()
    assert args.command1 == "profiles"
    assert args.id == "5"
    assert args.name == "anotherprofile"
    assert args.debug == False # Default value
    # Ensure command2 is not set for profiles
    assert not hasattr(args, 'command2')


# Run tests
test_users_create_command()
test_debug_users_delete_command()
test_profiles_command()

# Restore original sys.argv
sys.argv = original_argv

print("test_Tools_2.py tests passed!")

