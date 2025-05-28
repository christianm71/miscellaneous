# Dynamic Argparse Parser Generator

## Description

This repository contains `Tools.py`, a Python script that provides a utility function called `create_parser`. This function dynamically builds an `argparse.ArgumentParser` (including subparsers for commands) from a dictionary configuration. This approach allows for an easy and declarative way to define complex command-line interfaces with multiple levels of subcommands.

## `args_dict` Structure

The `create_parser` function takes a main parser instance and a dictionary (commonly named `args_dict`) that defines the arguments and commands. The main keys for this dictionary are:

*   `args`: (Optional) A list of tuples defining arguments for the current parser level (top-level or a specific subcommand). Each tuple consists of:
    *   `arg_name_or_flags`: A string or tuple of strings for the argument (e.g., `"name"`, `("--id", "-i")`).
    *   `options_dict`: A dictionary of keyword arguments to pass to `parser.add_argument()` (e.g., `dict(help="The item ID", type=int)`).
    Example:
    ```python
    "args": [
        ("--debug", dict(help="Enable debug mode", action="store_true", default=False)),
        ("filename", dict(help="The file to process"))
    ]
    ```

*   `commands`: (Optional) A dictionary where each key is a subcommand name (e.g., `"users"`, `"process"`). The value for each subcommand is another dictionary that defines that subcommand. This nested dictionary can contain:
    *   `help`: (Optional) A string describing the subcommand for the help message.
    *   `args`: (Optional) A list of arguments specific to this subcommand, following the same structure as the top-level `args`.
    *   `commands`: (Optional) Another nested `commands` dictionary for defining sub-subcommands, allowing for multiple levels of command hierarchy.

Example of a `commands` dictionary:
```python
"commands": {
    "users": {
        "help": "Manage users",
        "args": [
            ("--id", dict(help="The user ID", type=int)),
        ],
        "commands": {
            "create": {
                "help": "Create a new user",
                "args": [
                    ("--name", dict(help="Name of the user", required=True))
                ]
            }
        }
    }
}
```

## Basic Usage Example

Here's a minimal Python script demonstrating how to use `create_parser`:

```python
import argparse
from Tools import create_parser # Assuming Tools.py is in the same directory or PYTHONPATH

# Define command structure
my_commands_config = {
    "args": [
        ("--verbose", dict(action="store_true", help="Enable verbose output"))
    ],
    "commands": {
        "greet": {
            "help": "Greets someone",
            "args": [
                ("name", dict(help="Name of the person to greet"))
            ]
        }
    }
}

# Create the main parser
main_parser = argparse.ArgumentParser(description="My CLI Tool")

# Generate parsers from the dictionary configuration
# The 'generated_parsers' dict can be used to access specific subparsers later if needed,
# for example, to set default functions for them.
generated_parsers = create_parser(main_parser, my_commands_config)

# Parse arguments
# Note: For this example, sys.argv is implicitly used by parse_args().
# In test scripts, sys.argv might be manipulated for specific test cases.
args = main_parser.parse_args()

# Example logic to handle parsed arguments
# The 'create_parser' function creates destinations like 'command1', 'command2', etc.
# for chosen subcommands at each level.

if hasattr(args, 'command1') and args.command1 == "greet":
    greeting = f"Hello, {args.name}!"
    if args.verbose:
        print(f"Verbose mode: {greeting}")
    else:
        print(greeting)
elif args.verbose:
    print("Verbose mode enabled, but no command was specified.")
else:
    # If no command or known arguments are given, argparse usually prints help.
    # You might add more specific logic here if needed, or if only global options
    # like --verbose are passed without a command.
    if not vars(args): # A simple check if no arguments were stored
        main_parser.print_help()
    elif not hasattr(args, 'command1') and not args.verbose: # If no command and not verbose
        main_parser.print_help()

```
To run this example, save it as `my_tool.py` and then execute from your terminal:
`python my_tool.py greet --name "Alice"`
`python my_tool.py --verbose greet --name "Bob"`

## Running Examples/Tests

The repository includes `test_Tools_1.py` and `test_Tools_2.py`. These scripts:
*   Serve as more complex examples of how to define command structures.
*   Act as automated tests to verify the `create_parser` functionality.
*   Demonstrate single-level (`test_Tools_1.py`) and multi-level (`test_Tools_2.py`) subcommand definitions.

You can run these scripts directly (e.g., `python test_Tools_1.py` or `python test_Tools_2.py`). After recent modifications, they perform assertions to check correctness and will print a "tests passed" message if successful, rather than echoing the parsed arguments for each test case. To see the parser in action with specific arguments, you can temporarily modify them to print `args` or test commands like `python test_Tools_1.py users --id 1 --name test`.
```
