# Copyright (C) 2024  Max Wiklund
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import difflib
import os
import re
import sys
import textwrap
from dataclasses import dataclass, field
from typing import Any, Callable, List, Tuple, Union

from clap_python.style import Style, _PrivateStyle

try:
    import importlib.metadata

    __version__ = importlib.metadata.version("clap_python")
except ImportError:
    import importlib_metadata

    __version__ = importlib_metadata.version("clap_python")


_ARG_PREFIX_RE = re.compile(r"^(-+)")


def color_text(text: str, style: int = 0, color: int = 37) -> str:
    """Color text with ANSI Escape Code.

    Args:
        text: Text to format.
        style: Text style.
        color: Color to set.

    Returns:
        Colored text.

    """
    if not int(style) and color == 37:
        return text
    return f"\033[{style};{color}m{text}\033[0m"


class ClapPyException(Exception):
    """Exception to raise when parser fail."""

    def __init__(self, msg: str, command: Union[_CommandPrivate, _ArgPrivate]):
        super(ClapPyException, self).__init__(msg)
        self.msg = msg
        self.command = command


def _format_arg(
    arg: Union[Arg, SubCommand, MutuallyExclusiveGroup], style: _PrivateStyle
) -> str:
    """Format arg for help message.

    Args:
        arg: Argument to format.
        style: Style to use when formatting arg.

    Returns:
        Formatted arg as help string.

    """
    if isinstance(arg, MutuallyExclusiveGroup):
        return color_text(" | ".join([_format_arg(g_arg, style) for g_arg in arg]))

    msg = f"{arg.private.long_name}" + (
        f" {arg.private.short_name}" if arg.private.short_name else ""
    )

    msg = color_text(msg, style=style.flags.style, color=style.flags.color)

    if isinstance(arg, SubCommand):
        return msg
    elif arg.private.choices and not arg.private.value_name:
        args = f"{{{','.join(arg.private.choices)}}}"
        if not arg.private.long_name.startswith("-"):
            return args
        msg += f" {args}"
    elif arg.private.multiple_values:
        msg += color_text(
            f" [{arg.private.value_name.upper()} ...]",
            style=style.value_names.style,
            color=style.value_names.color,
        )

    elif arg.private.takes_value:
        msg += color_text(
            f" {arg.private.value_name.upper()}",
            style=style.value_names.style,
            color=style.value_names.color,
        )
    return msg


@dataclass()
class _ArgPrivate:
    """Class to hold business logic for ``Arg`` class."""

    arg: Arg
    long_name: str
    short_name: str = ""
    help_msg: str = ""
    takes_value: bool = True
    multiple_values: bool = False
    required: bool = False
    takes_values: bool = False
    is_help_arg: bool = False
    default_value = None
    value_name: str = ""

    tag: str = "Options"

    group: MutuallyExclusiveGroup = None

    value_parser: Callable[[str], Any] = str
    # fmt: off
    validate_callable: Callable[[Any, ], str] = lambda value: ""
    # fmt: on
    choices = None

    parent: _CommandPrivate = None

    def name(self) -> str:
        """Arg name.

        Returns:
            Long arg name.

        """
        return _ARG_PREFIX_RE.sub("", self.long_name).replace("-", "_")

    def get_style(self) -> _PrivateStyle:
        root = self
        while root.parent:
            root = root.parent
        return root.style

    # pylint: disable=expression-not-assigned
    def parse(
        self,
        argv: List[str],
        visited: List[Union[_ArgPrivate, _CommandPrivate]],
    ) -> dict:
        """Parse values for arg.

        Args:
            argv: Remaining arguments to be parsed by parser.
            visited: List of visited arguments.

        Raises:
            ClapPyException: Parsing failed.

        Returns:
            Dict with parsed values (argument name as key and parsed values
            as values).

        """
        exclusive_args = [
            arg.private.long_name
            for arg in (self.group or [])
            if arg.private in visited
        ]
        if exclusive_args:
            style_class = self.get_style()
            raise ClapPyException(
                (
                    f"argument {color_text(self.long_name, style=style_class.flags.style, color=style_class.flags.color)} "
                    f"not allowed with argument {color_text(exclusive_args[0], style=style_class.error.style, color=style_class.error.color)}"
                ),
                self.parent,
            )

        if not self.takes_value:
            # The arg does not take any value.
            return {self.name(): True}

        arg_names = [_arg.private.long_name for _arg in self.parent.get_arguments()]
        arg_names += [
            _arg.private.short_name
            for _arg in self.parent.get_arguments()
            if _arg.private.short_name
        ]

        # If no arguments are provided raise an exception
        if not argv or argv[0] in arg_names:
            message = (
                "expected at least one argument"
                if self.multiple_values
                else "expected one argument"
            )
            raise ClapPyException(message, self.parent)

        if not self.multiple_values:
            value = self.value_parser(argv.pop(0))
            self._validate_arg(value)
            return {self.name(): value}

        values = []

        while argv and argv[0] not in arg_names:
            values.append(self.value_parser(argv.pop(0)))

        # Validate values.
        [self._validate_arg(value) for value in values]
        return {self.name(): values}

    def _validate_arg(self, value: Any) -> None:
        """Validate argument value.

        Args:
            value: Value to validate.

        Raises:
            ClapPyException: User validation failed.

        """
        error_msg = self.validate_callable(value)
        if error_msg:
            raise ClapPyException(error_msg, self.parent)


class Arg:
    """Argument class to define cli arguments.


    **Example**::

        from clap_python import Arg, App

        args = (
            App()
            .about("Cli to change color space on images.")
            .arg(Arg("images").multiple_values(True))
            .arg(
                Arg("--color-space")
                .help("Color space to convert to.")
                .choices(["Rec.709", "ACEScg"])
                .default("Rec.709")
            )
            .arg(Arg("--output-dir").help("Directory to export converted images to"))
            .arg(Arg("--fast").takes_value(False))
            .parse_args()
        )

    """

    def __init__(self, long_name: str, short_name: str = ""):
        self.private = _ArgPrivate(
            arg=self,
            long_name=long_name,
            short_name=short_name,
            required=not long_name.startswith("-"),
        )
        self.value_name(self.private.name())

    def value_parser(self, parser: Callable[[Any], Any]) -> Arg:
        """Func to convert argument string into value.

        Args:
            parser: Callable object to cast parsed value into new. Default is ``str``.

        Returns:
            Self.

        **Example**::

            from clap_python import App, Arg
            app = App().arg(Arg("--number").value_parser(int))
            print(app.parse_args(["--number", "101"]))
            {"number": 101}

        """
        self.private.value_parser = parser
        return self

    def choices(self, choices: List[Union[float, int, str]]) -> Arg:
        """Specify values that are valid for the argument.

        Args:
            choices: Values that are valid.

        Returns:
            Self

        """
        self.private.choices = choices

        def validate(value: Any) -> str:
            """Validate that ``value`` matches choices.

            Args:
                value: Parsed value to validate.

            Returns:
                Error message if value not in choices else empty string.

            """
            if value in self.private.choices:
                return ""
            options = ", ".join(f"'{opt}'" for opt in self.private.choices)

            similar_values: List[str] = difflib.get_close_matches(
                value, self.private.choices
            )
            error_msg = (
                f"argument {self.private.long_name}: invalid choice: "
                f"'{value}' (choose from {options})"
            )

            style = self.private.get_style()

            if similar_values:
                error_msg += (
                    f"\n\n{color_text('tip:', style=style.tip.style, color=style.tip.color)} "
                    f"a similar value exists: "
                    f"'{color_text(similar_values[0], style=style.tip.style, color=style.tip.color)}'"
                )

            return error_msg

        self.private.validate_callable = validate
        return self

    def validate(self, callable_: Callable[[Any], str]) -> Arg:
        """Set callable object to validate arg value.

        Args:
            callable_: Callable object that returns error message if failed.

        **Example**:

            from typing import Any
            from clap_python import Arg, App

            def validate(value: str) -> str:
                if value != "hello":
                    return "Invalid arg... 'hello' is only allowed."
                return ""
            args = App().arg(Arg("--abc").validate(validate)).parse_args()

        Returns:
            Self.

        """
        self.private.validate_callable = callable_
        return self

    def default(self, value: Any) -> Arg:
        """Default value for arg. If specified argument is not required.

        Args:
            value: Default value.

        Returns:
            Self.

        """
        self.private.default_value = value
        return self

    def value_name(self, text: str) -> Arg:
        """Set argument value name.

        Args:
            text: Argument value name.

        Returns:
            Self.

        """
        self.private.value_name = text
        return self

    def help(self, text: str) -> Arg:
        """Add help text to argument.

        Args:
            text: Description what the arg does.

        Returns:
            Self.

        """
        self.private.help_msg = text
        return self

    def takes_value(self, value: bool) -> Arg:
        """Configure whether arg requires value to be passed.

        Args:
            value: True if argument takes value else False.

        Returns:
            Self.

        """
        self.private.takes_value = value
        return self

    def multiple_values(self, value: bool) -> Arg:
        """Set if arg takes multiple values.

        Args:
            value:
                If True arg can consume multiple values and result of arg is
                list.

        Returns:
            Self.

        """
        self.private.multiple_values = value
        return self

    def required(self, value: bool) -> Arg:
        """Set enabled and not passed parser will fail.

        Args:
            value: If True and arg is missing parser will fail and exit.

        Returns:
            Self.

        """
        # If the argument is positional it is always required.
        self.private.required = value
        return self


@dataclass()
class _GroupPrivate:
    """Class to hold business logic for ``MutuallyExclusiveGroup`` class."""

    children: List[Union[SubCommand, Arg]] = field(default_factory=lambda: [])
    required: bool = False
    help_heading: str = ""

    @property
    def is_help_arg(self) -> bool:
        """Check if arg is help arg.

        Returns:
            False if argument is not a help arg.

        """
        return False


class MutuallyExclusiveGroup:
    """Group to define group where only one command can be called."""

    def __init__(self):
        self.private = _GroupPrivate()

    def required(self, value: bool) -> Arg:
        """Set enabled and not passed parser will fail.

        Args:
            value: If True and arg is missing parser will fail and exit.

        Returns:
            Self.

        """
        # If the argument is positional it is always required.
        self.private.required = value
        return self

    def help_heading(self, label: str) -> MutuallyExclusiveGroup:
        """Lets you organize the help message visually by adding a header above related options.

        Args:
            label: Name of header.

        Returns:
            Self.

        """
        self.private.help_heading = label
        return self

    def arg(self, arg: Union[Arg, SubCommand]) -> MutuallyExclusiveGroup:
        """Add arg to group.

        Args:
            arg: Arg to add to mutually exclusive group.

        Raises:
            ValueError: Unsupported data type.

        Returns:
            Self.

        """
        if not isinstance(arg, (Arg, SubCommand)):
            raise ValueError(f"{type(self).__name__}.arg only supports Arg, SubCommand")

        if isinstance(arg, Arg) and self.private.help_heading:
            arg.private.tag = self.private.help_heading
        arg.private.group = self
        self.private.children.append(arg)
        return self

    def __iter__(self):
        return iter(self.private.children)


@dataclass()
class _CommandPrivate:
    """Class to hold business logic for ``SubCommand`` class."""

    command: SubCommand
    long_name: str
    short_name: str = ""
    help_msg: str = ""
    subcommand_required: bool = False
    arg_else_show_help: bool = False
    help_heading: str = ""
    tag: str = "Commands"
    group: MutuallyExclusiveGroup = None

    arguments: List[Union[Arg, SubCommand, MutuallyExclusiveGroup]] = field(
        default_factory=lambda: []
    )
    positional_args: List[Arg] = field(default_factory=lambda: [])
    parent: _CommandPrivate = None
    style: _PrivateStyle = field(default_factory=_PrivateStyle)
    version: str = ""
    width: int = 100

    def get_style(self) -> _PrivateStyle:
        """Get app style."""
        return self.get_app().style

    def get_app(self) -> _CommandPrivate:
        root = self
        while root.parent:
            root = root.parent
        return root

    def get_width(self) -> int:
        return self.get_app().width

    def name(self) -> str:
        """Name of command.

        Returns:
            Long command name.

        """
        return _ARG_PREFIX_RE.sub("", self.long_name).replace("-", "_")

    @property
    def is_help_arg(self) -> bool:
        """Check if arg is help argument.

        Returns:
            True if arg is help arg else False.

        """
        return False

    def get_arguments(self) -> List[Union[SubCommand, Arg]]:
        """Unpack args (groups).

        Returns:
            List of unpacked args and subcommands.

        """
        arguments = []
        for arg in self.arguments:
            if isinstance(arg, MutuallyExclusiveGroup):
                for g_arg in arg:
                    arguments.append(g_arg)
            else:
                arguments.append(arg)
        return arguments

    def get_commands_and_options(self) -> Tuple[List[SubCommand], List[Arg]]:
        """Get commands and optional args.

        Returns:
            Subcommands and optional args.

        """
        arguments = self.get_arguments()
        command = [arg for arg in arguments if isinstance(arg, SubCommand)]
        optional = [arg for arg in arguments if isinstance(arg, Arg)]
        return command, optional

    def arg_path_string(self) -> str:
        """Returns string of command that failed.

        Returns:
            App command or arg that failed e.g ``git clone``.

        """
        path = []
        node = self
        while node:
            path.insert(0, node.name())
            node = node.parent
        return " ".join(path)

    def usage_string(self) -> str:
        """Usage text.

        Returns:
            Usage text e.g Usage:app [--add [ADD ...]]

        """
        style = self.get_style()

        usage_positional_args = " ".join(
            [
                color_text(
                    f"<{arg.private.long_name}>",
                    style=style.flags.style,
                    color=style.flags.color,
                )
                for arg in self.positional_args
                if not arg.private.is_help_arg
            ]
        )

        commands = [arg for arg in self.arguments if isinstance(arg, SubCommand)]
        optional_args = [
            arg for arg in self.arguments if not isinstance(arg, SubCommand)
        ]

        usage_optional_args = " ".join(
            [
                f"[{_format_arg(arg, style)}]"
                for arg in optional_args
                if not arg.private.is_help_arg
            ]
        )
        usage_commands = "<COMMAND>" if commands else ""

        options = " ".join([usage_positional_args, usage_optional_args, usage_commands])

        return f"{color_text('Usage:', style=style.usage.style, color=style.usage.color)} {options}"

    def _print_version(self) -> None:
        """Print version info."""
        sys.stdout.write(f"{os.path.basename(sys.argv[0])} {self.version}\n")

    def print_help(self) -> None:
        """Print help message cli."""
        style = self.get_style()
        style_no_color = _PrivateStyle()

        max_text_width = self.get_width()

        msg = ""
        if self.help_msg:
            msg += f"{self.help_msg}\n"

        msg += f"{self.usage_string()}\n"
        max_width = max(
            len(_format_arg(arg, style_no_color))
            for arg in self.get_arguments() + self.positional_args
        )

        longest_str = min(50, max_width) + 4
        indent = 2

        grouped_args = {}
        for arg in self.positional_args + self.get_arguments():
            grouped_args.setdefault(arg.private.tag, []).append(arg)

        default_options = ["Arguments", "Commands", "Options"]
        order = default_options + list(set(grouped_args.keys()) - set(default_options))

        for title in order:
            arguments = grouped_args.get(title)
            if not arguments:
                continue
            msg += color_text(
                f"\n{title}:\n", style=style.headers.style, color=style.headers.color
            )

            for arg in arguments:
                text = " " * indent + _format_arg(arg, style)
                text_no_color = " " * indent + _format_arg(arg, style_no_color)
                spaces = " " * (longest_str - len(text_no_color))

                wrapper = textwrap.TextWrapper(
                    width=max_text_width, subsequent_indent=" " * (longest_str + 1)
                )
                line = f"{text}{spaces} {arg.private.help_msg}"
                msg += f"{wrapper.fill(line)}\n"

        sys.stdout.write(f"{msg}\n")

    # pylint: disable=too-many-branches
    def parse(
        self,
        args: List[str],
        visited: List[Union[_ArgPrivate, _CommandPrivate]],
        allow_unknown: bool,
    ) -> dict:
        """Parse cli args.

        Args:
            args: Args to parse.
            visited: List of visited nodes.
            allow_unknown:
                If true allow parsing of unknown arguments separated by "--"
                else raise exception.

        Raises:
            ClapPyException: Parsing failed.

        Returns:
            Dict with parsed result.

        """
        style_class = self.get_style()

        if not args and self.arg_else_show_help:
            self.print_help()
            sys.exit(0)

        self._check_mutually_exclusive_args(visited, style_class)

        # Populate with default data.
        parsed_data = self._initialize_parsed_data()
        self._skip_positional_args = False

        while args:
            arg_str = args.pop(0)
            # Check for help or version argument
            if self._parse_global_args(arg_str):
                sys.exit(0)
            if self._parse_positional_args(arg_str, args, visited, parsed_data):
                continue
            # Parse optional arguments or subcommands
            self._parse_subcommands_and_options(
                arg_str, args, visited, parsed_data, allow_unknown
            )

        self._validate_subcommands(visited)
        self._validate_required_arguments(visited, style_class)
        return {self.name(): parsed_data}

    def _parse_positional_args(
        self,
        arg_str: str,
        args: List[str],
        visited: List[Union[_ArgPrivate, _CommandPrivate]],
        parsed_data,
    ) -> bool:
        """Parse positional arguments.

        Args:
            arg_str: The current argument string to parse.
            args: The remaining arguments to parse.
            visited: List of arguments or commands that have already been visited during parsing.
            parsed_data: Dict to store parsed argument data in.

        Returns:
            True if a positional argument was successfully parsed.

        """
        if self._skip_positional_args:
            return False

        # Parse positional arguments
        for arg in self.positional_args:
            if arg_str.startswith("-"):
                self._skip_positional_args = True
                return False

            if arg.private not in visited:
                args.insert(0, arg_str)
                parsed_data.update(arg.private.parse(args, visited))
                visited.append(arg.private)
                return True
        return False

    def _parse_subcommands_and_options(
        self,
        arg_str: str,
        args: List[str],
        visited: List[Union[_ArgPrivate, _CommandPrivate]],
        parsed_data: dict,
        allow_unknown: bool,
    ) -> None:
        """Parse optional arguments and subcommands.

        Args:
            arg_str: The current argument string to parse.
            args: The remaining arguments to parse.
            visited: List of arguments or commands that have already been visited during parsing.
            parsed_data: Dict to store parsed argument data in.
            allow_unknown: If True allow parsing of unknown arguments.

        Raises:
            ClapPyException: If an argument is unrecognized and `allow_unknown`
            is `False`.

        """
        # Parse optional arguments or subcommands
        for arg in self.get_arguments():
            if arg_str in (
                arg.private.long_name,
                arg.private.short_name,
            ):
                if self._parse_global_args(arg.private.name()):
                    sys.exit(0)

                kwargs = (
                    {
                        "args": args,
                        "visited": visited,
                        "allow_unknown": allow_unknown,
                    }
                    if isinstance(arg, SubCommand)
                    else {"argv": args, "visited": visited}
                )
                parsed_data.update(arg.private.parse(**kwargs))
                visited.append(arg.private)
                return
        else:
            # Handle unknown arguments
            if arg_str == "--" and allow_unknown:
                parsed_data.setdefault("unknown", []).extend(args)
                args.clear()  # All args that where left have
                # been moved to unknown. Clear args to stop loop.
            else:
                style_class = self.get_style()
                raise ClapPyException(
                    f"unrecognized arguments: {color_text(arg_str, style=style_class.error.style, color=style_class.error.color)}",
                    self,
                )

    def _parse_global_args(self, arg_str: str) -> bool:
        """Parse global args (help arg and version arg).

        Args:
            arg_str: Arg string to parse.

        Returns:
            True if global arg was parsed.

        """
        # Check for help argument
        if arg_str in ("-h", "--help"):
            self.print_help()
            return True
        elif arg_str in ("-V", "--version") and self.version:
            self._print_version()
            return True
        return False

    def _initialize_parsed_data(self) -> dict:
        """Initialize the parsed data dictionary with default values."""
        parsed_data = {}
        # Populate with default data.
        for arg in self.get_arguments():
            if isinstance(arg, Arg) and arg.private.is_help_arg:
                continue
            if isinstance(arg, Arg) and arg.private.default_value is not None:
                parsed_data[arg.private.name()] = arg.private.default_value
            elif isinstance(arg, Arg) and not arg.private.takes_value:
                parsed_data[arg.private.name()] = False
        return parsed_data

    def _check_mutually_exclusive_args(
        self,
        visited: List[Union[_ArgPrivate, _CommandPrivate]],
        style_class: _PrivateStyle,
    ) -> None:
        """Check for mutually exclusive arguments in the visited list.

        Args:
            visited: List of arguments or commands that have already been visited during parsing.
            style_class: Style object for error message.

        Raises:
            ClapPyException: If mutually exclusive arguments are found.

        """
        active_args = [
            arg.private.long_name
            for arg in (self.group or [])
            if arg.private in visited
        ]
        if active_args:
            raise ClapPyException(
                f"argument {color_text(self.long_name, style=style_class.flags.style, color=style_class.flags.color)} "
                f"not allowed with argument {color_text(active_args[0], style=style_class.error.style, color=style_class.error.color)}",
                self.parent,
            )

    def _validate_required_arguments(
        self,
        visited: List[Union[_ArgPrivate, _CommandPrivate]],
        style_class: _PrivateStyle,
    ) -> None:
        """Validate that all required arguments are provided.

        Args:
            visited: List of arguments or commands that have already been visited during parsing.
            style_class: Style object for error message.

        Raises:
            ClapPyException: If required arguments or mutually exclusive groups
                are missing from the `visited` list.

        """
        # Gather required arguments
        required_args = [
            arg
            for arg in self.positional_args + self.get_arguments()
            if isinstance(arg, Arg) and arg.private.required
        ]
        required_groups = [
            arg
            for arg in self.arguments
            if isinstance(arg, MutuallyExclusiveGroup)
            if arg.private.required
        ]
        # Check for missing required arguments
        missing_args = [
            arg.private.long_name for arg in required_args if arg.private not in visited
        ]
        if missing_args:
            arg_text = color_text(
                ", ".join(missing_args),
                style=style_class.flags.style,
                color=style_class.flags.color,
            )
            raise ClapPyException(
                f"the following arguments are required: {arg_text}",
                self,
            )
        missing_group_args = [
            group
            for group in required_groups
            if not any(arg.private in visited for arg in group)
        ]
        if missing_group_args:
            missing_args_text = " | ".join(
                arg.private.long_name for arg in missing_group_args[0]
            )

            arg_text = color_text(
                missing_args_text,
                style=style_class.flags.style,
                color=style_class.flags.color,
            )
            raise ClapPyException(
                f"One of the following arguments are required: {arg_text}",
                self,
            )

    def _validate_subcommands(
        self, visited: List[Union[_ArgPrivate, _CommandPrivate]]
    ) -> None:
        """Validate that a required subcommand has been provided.

        Args:
            visited: List of arguments or commands that have already been visited during parsing.

        Raises:
            ClapPyException: If a required subcommand is missing.

        """
        sub_commands, _ = self.get_commands_and_options()
        if (
            self.subcommand_required
            and sub_commands
            and not any(cmd for cmd in sub_commands if cmd.private in visited)
        ):
            sub_commands_str = " | ".join(
                [arg.private.long_name for arg in sub_commands]
            )
            help_msg = "requires a subcommand but one was not provided\n"
            help_msg += f"  [subcommands: {sub_commands_str}]\n\n"
            help_msg += "For more information, try '--help'."
            raise ClapPyException(help_msg, self)


class SubCommand:
    """Sub command."""

    def __init__(self, long_name: str, short_name: str = ""):
        self.private = _CommandPrivate(self, long_name, short_name)

        help_arg = Arg("--help", "-h").help("Show this help message and exit")
        help_arg.private.is_help_arg = True
        help_arg.takes_value(False)
        help_arg.private.parent = self.private
        self.private.arguments.insert(0, help_arg)

    def help_heading(self, label: str) -> SubCommand:
        """Lets you organize the help message visually by adding a header above related options.

        Args:
            label: Name of header.

        Returns:
            Self.

        """
        self.private.help_heading = label
        return self

    def subcommand_required(self, value: bool) -> SubCommand:
        """If True and no subcommand passed show help message.

        Args:
            value: If True and no subcommand provided show help message and exit.

        Returns:
            Self.

        """
        self.private.subcommand_required = value
        return self

    def arg_required_else_help(self, value: bool) -> SubCommand:
        """If True and no args are passed show help message.

        Args:
            value: If True and no args provided show help message and exit.

        Returns:
            Self.

        """
        self.private.arg_else_show_help = value
        return self

    def about(self, text: str) -> SubCommand:
        """Description about subcommand or app.

        Args:
            text: Description about command.

        Returns:
            Self.

        """
        self.private.help_msg = text
        return self

    def arg(self, arg: Union[Arg, SubCommand, MutuallyExclusiveGroup]) -> SubCommand:
        """Add arg to self.

        Args:
            arg: Arg to add.

        Returns:
            Self.

        """
        if isinstance(arg, MutuallyExclusiveGroup):
            for group_arg in arg:
                group_arg.private.parent = self.private
                if self.private.help_heading and isinstance(group_arg, Arg):
                    group_arg.private.tag = self.private.help_heading
            self.private.arguments.append(arg)
            return self

        arg.private.parent = self.private
        if arg.private.long_name.startswith("-") or isinstance(arg, SubCommand):
            if isinstance(arg, Arg) and self.private.help_heading:
                arg.private.tag = self.private.help_heading
            self.private.arguments.append(arg)
        else:
            arg.private.tag = "Arguments"
            self.private.positional_args.append(arg)
        return self


class App(SubCommand):
    """Base class to build cli.

    **Example**::

        from clap_python import App, Arg
        args = (
            App()
            .arg(Arg("--hello"))
            .arg(Arg("--items").multiple_values(True))
            .parse_args()
        )

    """

    def __init__(self, name: str = os.path.basename(sys.argv[0])):
        super().__init__(name)

    def version(self, version_number: str) -> App:
        """Set version number for app.

        Args:
            version_number: App version number.

        Returns:
            Self.

        """
        self.private.version = version_number
        for arg in self.private.arguments:
            if arg.private.name() == "version":
                return self

        version_arg = Arg("--version", "-V").help("Print version info and exit")
        version_arg.takes_value(False)
        version_arg.private.is_help_arg = True
        version_arg.private.parent = self.private
        self.private.arguments.insert(1, version_arg)
        return self

    def width(self, value: int) -> App:
        """Set max width of help text.

        Arg:
            value: Max width.

        Returns:
            Self.

        """
        self.private.width = value
        return self

    def style(self, style: Style) -> App:
        """Apply style to app.

        Args:
            style: Style to use when coloring stdout.

        Returns:
            Self.

        """
        self.private.style = style.private
        return self

    def _parse(self, args: List[str], visited: list, allow_unknown: bool) -> dict:
        """Parse cli args.

        Args:
            args: Args to parse.
            visited: List of visited nodes.
            allow_unknown:
                If true allow parsing of unknown arguments sepaerated by "--"
                else print error message and exit.

        Returns:
            Dict with parsed result.

        """
        try:
            data = self.private.parse(
                args, allow_unknown=allow_unknown, visited=visited
            )
        except ClapPyException as err:
            style_class = self.private.get_style()
            sys.stderr.write(f"{err.command.usage_string()}\n")
            sys.stderr.write(
                (
                    f"{color_text(err.command.arg_path_string(), style=style_class.flags.style, color=style_class.flags.color)}: "  # TODO: Maby use usage or a diffrent style?
                    f"{color_text('error:', style=style_class.error.style, color=style_class.error.color)} {err.msg}\n"
                )
            )
            sys.exit(1)

        return data.get(self.private.name())

    def parse_args(self, args: List[str] = None) -> dict:
        """Parse known arguments. Any unknown arguments will stop execution.

        Args:
            args: List of arguments to parse (don't include the app name).

        Returns:
            Parsed result as dict.

        """
        args = args if args else sys.argv[1:]
        return self._parse(args=args, visited=[], allow_unknown=False)

    def parse_known_args(self, args: List[str] = None) -> dict:
        """Parse known and unknown arguments. Unknown arguments  are separated by "--".

        Args:
            args: List of arguments to parse (don't include the app name).


        **Example**:

            from clap_python import App, Arg

            args = (
                App()
                .about("run application")
                .arg(Arg("-c").help("name of application to run"))
                .parse_known_args(["-c", "nuke", "--", "-t"])
            )
            print(args)
            {"c": "nuke", "unknown": ["-t"]}

        Returns:
            Parsed result as dict.

        """
        args = args if args else sys.argv[1:]
        return self._parse(args=args, visited=[], allow_unknown=True)
