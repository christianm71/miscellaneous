
def create_parser(parser, commands_dict):
    # ------ inner function to create recursive parsers for sub commands ------
    def _create_parser(parser, commands_dict, level, _parsers_dict):
        for item in commands_dict.get("args", []):
            arg_name = item[0]
            arg_options = item[1]
            parser.add_argument(arg_name, **arg_options)

        commands = commands_dict.get("commands", [])

        if commands:
            help = commands_dict.get("help")
            dest = f"command{level}"
            subparsers = parser.add_subparsers(dest=dest, help=help)

            for sub_command_name in commands:
                help = commands[sub_command_name].get("help")
                new_parser = subparsers.add_parser(sub_command_name, help=help)
                _parsers_dict[sub_command_name] = {}
                _parsers_dict[sub_command_name]["_parser_"] = new_parser
                _create_parser(new_parser, commands[sub_command_name], level + 1, _parsers_dict[sub_command_name])

    _parsers_dict = {}
    _create_parser(parser, commands_dict, 1, _parsers_dict)
    return _parsers_dict

