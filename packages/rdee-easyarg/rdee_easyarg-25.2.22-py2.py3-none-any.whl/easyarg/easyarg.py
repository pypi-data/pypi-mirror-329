#!/usr/bin/env python3
# coding=utf-8


import sys
import re
import argparse
import functools
import inspect
from typing import Callable, get_args, Optional
import importlib
import textwrap

import argcomplete
import rich


class _MyArgParser(argparse.ArgumentParser):
    def error(self, message):
        print(message)
        print("----------------------------------")
        print()
        self.print_help()
        sys.exit(1)

    def is_subparser(self):
        """
        Specific for this program because the main parser always have subparsers

        Last Update: @2025-02-20 10:08:51
        """
        return self._subparsers is None

    def print_help(self, file=None):
        from rich.panel import Panel
        from rich.table import Table
        from rich.text import Text
        from rich.console import Console

        console = Console()
        width = console.width

        # return super().print_help(file)
        if self.is_subparser():
            assert hasattr(self, "doc")

            usage = f" {self.prog} \[-h, --help] <Arguments>"
            panel_usage = Panel(
                usage,
                title="Usage",
                title_align="left",
                border_style="#aaaaaa",
                padding=(0, 0)              # 调整面板内边距
            )
            rich.print(panel_usage)

            if self.doc:
                panel_doc = Panel(
                    self.doc,
                    title="Docstring",
                    title_align="left",
                    border_style="#aaaaaa",
                    padding=(0, 0)              # 调整面板内边距
                )
                rich.print(panel_doc)

            hmsg = ""
            i_action = 0
            for action in self._actions:
                if action.dest == "help":
                    continue
                # print(action)
                i_action += 1
                options = sorted(action.option_strings, key=lambda x: len(x))
                if action.type is None:
                    if action.default is not None:
                        argType = type(action.default).__name__
                    elif action.const is not None:
                        argType = type(action.const).__name__
                    else:
                        argType = "str"
                else:
                    argType = action.type.__name__

                if action.nargs == 0:
                    assert argType == "bool", f"{argType=}"
                elif action.nargs:
                    argType += action.nargs

                if options[0].startswith("--no-"):
                    hmsg += " ↳ "
                    hmsg += f"[cyan]{', '.join(options):27}[/cyan]   [gold3]{'':10}[/gold3]"
                else:
                    if i_action > 1:
                        hmsg += "[#eeeeee]" + '─' * (width - 2) + "[/#eeeeee]\n"
                    hmsg += f"[cyan]{', '.join(options):30}[/cyan]   [gold3]{argType:10}[/gold3]"

                    if action.default is not None:
                        if action.default == "":
                            _default = '""'
                        else:
                            _default = str(action.default)
                        hmsg += f"   [bright_black]\[default: { _default + ']':10}[/bright_black]"

                    if action.required or action.dest in self.required_bool_pair:
                        hmsg += f"   [red]\[required][/red]"

                if action.help:
                    # print(f"dest: {action.dest}, type: {action.type}")
                    if action.nargs != 0:
                        hmsg += f"\n   ■ {action.help}"
                    elif options[0].startswith("--no-"):
                        hmsg += f"\n   ■ {action.help}"

                hmsg += "\n"
            panel_args = Panel(
                hmsg.rstrip(),
                title="Argument",
                title_align="left",
                border_style="#aaaaaa",
                padding=(0, 0)              # 调整面板内边距
            )

            rich.print(panel_args)

            # return super().print_help()
        else:
            usage = f"{self.prog} \[-h, --help] <command> \[-h, --help] \[arguments]"
            panel_usage = Panel(
                usage,
                title="Usage",
                title_align="left",
                border_style="#aaaaaa",
                padding=(0, 0)              # 调整面板内边距
            )
            rich.print(panel_usage)

            commands = self._subparsers._actions[-1].choices

            table = Table(show_header=False,
                          show_edge=False,  # 移除外边框
                          show_lines=False,  # 移除内部分隔线
                          box=None,         # 移除所有边框线
                          padding=(0, 2))   # 调整左右padding

            table.add_column("Command", style="bold cyan")
            table.add_column("Description", style="bold green")

            rows = []
            rowMap = {}
            i_row = 0
            for k, v in commands.items():
                # table.add_row(k, v.description)
                if v.prog in rowMap:
                    rows[rowMap[v.prog]][0].append(k)
                    continue
                rows.append([[k], v.description])
                rowMap[v.prog] = i_row
                i_row += 1
            for ks, v in rows:
                table.add_row(",".join(sorted(ks, key=lambda x: len(x))), v)

            panel = Panel(
                table,
                title="Commands",
                title_align="left",
                border_style="#aaaaaa",
                padding=(0, 0)              # 调整面板内边距
            )

            rich.print(panel)

        return

    def get_subparser(self, name: str):
        return self._subparsers._group_actions[0].choices[name]

    def parse_args(self, args=None):
        """
        Add check for required no-arg options pair

        e.g., for "def func1(do_it: bool)", the parser will add --do-it and --no-do-it, and you have to use one of them, this wrapper will do the check

        ---------------------------------
        Last Update: @2025-02-21 18:54:02
        """
        args = super().parse_args(args)
        subparser = self.get_subparser(args.command)
        for pn in subparser.required_bool_pair:
            if getattr(args, pn) is None:
                rich.print(f"[red]Error![/red] --{pn} or --no-{pn} is required!")
                sys.exit(101)
        return args


class EasyArg:
    """
    Used to generate subparsers for target functions by decorating `@instance.command()`
    Then, call `instance.parse` to run corresponding function based on CLI command
    """

    def __init__(self, description: str = ""):
        """
        Initialize:
            - argparse.ArgumentParser & its subparsers
            - functions holder

        Last Update: @2024-11-23 14:35:26
        """
        self.parser = _MyArgParser(description=description)
        self.subparsers = self.parser.add_subparsers(dest='command', help='Execute functions from CLI commands directly')
        self.functions = {}

    def command(self, name="", desc="", alias="", defaults: None | dict = None):
        """
        A function decorator, used to generate a subparser and arguments based on the function signature

        :param defaults: Set specific default values for arguments under cmd invoke

        ---------------------------------
        Last Update: @2025-02-22 00:15:34
        """
        def decorator(func: Callable):
            # @ Prepare
            # @ .handle-names
            cmd_name = name if name else func.__name__
            if alias:
                aliases = [alias]
            else:
                aliases = []
            # @ .get-short-description
            if not desc and func.__doc__ is not None:
                desc2 = re.split(r'\n *\n', func.__doc__)[0].strip()  # Use the first paragraph
            else:
                desc2 = desc

            # @ .create-subparser
            parser = self.subparsers.add_parser(cmd_name.replace("_", "-"), aliases=aliases, description=desc2)  # @ exp | Add a subparser with command the same as function name
            parser._main_parser = self.parser
            parser.doc = ""
            parser.required_bool_pair = []

            # @ .refine-long-doc | and save argument information
            argInfos = {}
            if func.__doc__ is not None:
                doc = textwrap.dedent(func.__doc__).strip()
                argLines = re.findall(r":param ([0-9a-zA-Z_]+): (.*)", doc)
                for an, ai in argLines:  # @ exp | arg-name, arg-info
                    argInfos[an] = ai

                doc = re.sub(r':param [0-9a-zA-Z_]+: .*', '', doc)
                doc = re.sub(r':return ?: .*', '', doc)
                doc = re.sub(r'\n+', '\n', doc, flags=re.M)
                doc = doc.strip()
                parser.doc = doc

            # @ Main | Add arguments with proper attributes
            shortname_recorded = set()
            sig = inspect.signature(func)
            for param_name, param in sig.parameters.items():
                # @ .retrieve-type | From annotations, take the first type for the compound types, e.g. get `str`` for `typing.Union[str, float]`
                param_name_opt = param_name.replace("_", "-")
                annotation = param.annotation
                annotations = get_args(annotation)
                if annotations:
                    annotation = annotations[0]  # @ note | Take the first annotation type as the target type in command line interface

                # @ .get-attribute
                required = param.default == inspect._empty
                if isinstance(defaults, dict) and param_name in defaults:
                    default = defaults[param_name]
                else:
                    default = None if required else param.default

                # @ .add-argument | Only support intrinsic types: int, float, str & bool
                # @ - Use the first letter as short-name if no conflict
                if annotation == inspect.Parameter.empty:
                    raise TypeError(f"Parameter '{param_name}' in function '{func.__name__}' missing type hint")

                elif annotation in (int, float, str):
                    short_name = param_name[0]
                    assert short_name.isalpha()
                    if short_name not in shortname_recorded:
                        parser.add_argument(f"--{param_name_opt}", f"-{short_name}", type=annotation, required=required, default=default, help=argInfos.get(param_name, ""))
                        shortname_recorded.add(short_name)
                    else:
                        parser.add_argument(f"--{param_name_opt}", type=annotation, required=required, default=default, help=argInfos.get(param_name, ""))

                elif annotation == bool:
                    # @ ..handle-bool-specifically
                    short_name = param_name[0]
                    assert short_name.isalpha()
                    if required:
                        parser.required_bool_pair.append(param_name)
                    if short_name not in shortname_recorded:
                        parser.add_argument(f"--{param_name_opt}", f"-{short_name}", dest=param_name, action="store_true", default=default, help=argInfos.get(param_name, ""))
                        shortname_recorded.add(short_name)
                    else:
                        parser.add_argument(f"--{param_name_opt}", dest=param_name, action="store_true", default=default, help=argInfos.get(param_name, ""))
                    parser.add_argument(f"--no-{param_name_opt}", dest=param_name, action="store_false", default=None if default is None else not default, help=argInfos.get(param_name, ""))
                else:
                    raise TypeError(f"easyarg only supports types: int, float, str & bool, now is {annotation}")

            # @ Post
            self.functions[cmd_name] = func

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper
        return decorator

    def parse(self, args: Optional[list[str]] = None):
        """
        Last Update: @2024-11-23 14:40:31
        ---------------------------------
        Parse arguments and call corresponding function
        """
        argcomplete.autocomplete(self.parser)
        args = self.parser.parse_args(args)
        kwargs = {key: value for key, value in vars(args).items() if key != 'command' and value is not None}

        if args.command is None:
            self.parser.print_help()
            return

        func = self.functions[args.command]
        func(**kwargs)
