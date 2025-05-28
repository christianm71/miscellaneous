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

import sys

# Store the original sys.argv
original_argv = sys.argv

def test_users_command():
    sys.argv = ['test_Tools_1.py', 'users', '--id', '1', '--name', 'testuser']
    args = parser.parse_args()
    assert args.command1 == "users"
    assert args.id == "1"
    assert args.name == "testuser"
    assert args.debug == False # Default value

def test_profiles_command():
    sys.argv = ['test_Tools_1.py', 'profiles', '--id', '10', '--name', 'profilename']
    args = parser.parse_args()
    assert args.command1 == "profiles"
    assert args.id == "10"
    assert args.name == "profilename"
    assert args.debug == False # Default value

def test_debug_users_command():
    sys.argv = ['test_Tools_1.py', '--debug', 'users', '--id', '1', '--name', 'testuser']
    args = parser.parse_args()
    assert args.debug == True
    assert args.command1 == "users"
    assert args.id == "1"
    assert args.name == "testuser"

def test_debug_profiles_command():
    # Also test debug with profiles for completeness
    sys.argv = ['test_Tools_1.py', '--debug', 'profiles', '--id', '11', '--name', 'debugprofile']
    args = parser.parse_args()
    assert args.debug == True
    assert args.command1 == "profiles"
    assert args.id == "11"
    assert args.name == "debugprofile"

# Run tests
test_users_command()
test_profiles_command()
test_debug_users_command()
test_debug_profiles_command()

# Restore original sys.argv
sys.argv = original_argv

print("test_Tools_1.py tests passed!")

