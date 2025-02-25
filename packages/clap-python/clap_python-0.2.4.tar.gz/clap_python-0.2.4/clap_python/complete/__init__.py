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
import os
import sys
from typing import Any, List, Union

from clap_python import App, _CommandPrivate


class _DualKeyDict:
    """A dictionary-like structure that allows two keys to access the same value.
    Removing either key deletes the entry for both keys.

    """

    def __init__(self):
        self.value_map = {}  # To store key-value pairs
        self.key_map = {}  # To store mappings between keys

    def keys(self) -> List[Any]:
        """Gets all keys stored in `_DualKeyDict`.

        Returns:
            A list of all keys currently stored in `_DualKeyDict`.

        """
        return list(self.value_map.keys())

    def add(self, key1: str, key2: Union[str, None], value: Any) -> None:
        """Adds a value associated with two keys to the dictionary.

        If `key2` is `None`, only `key1` will be added. Both keys will map
        to the same value. If either key is removed, both keys and the value
        are deleted.

        Args:
            key1: The primary key for the value.
            key2: Optional secondary key for the value. If `None`, only `key1` is used.
            value: The value to be associated with `key1` and `key2`.

        """
        self.value_map[key1] = value
        if not key2:
            return
        self.value_map[key2] = value

        # Map each key to the other in key_map for easy access to both keys
        self.key_map[key1] = key2
        self.key_map[key2] = key1

    def get(self, key: str) -> Any:
        """Retrieves the value associated with a key.

        Args:
            key: The key whose value should be retrieved.

        Returns:
            The value associated with the given key, or `None` if the key is not found.
        """
        return self.value_map.get(key)

    def remove(self, key: str) -> None:
        """Removes the entry for the given key and its paired key, if it exists.

        Args:
            key: The key to be removed, along with its paired key.

        Raises:
            KeyError: If the specified key is not found in the dictionary.

        """
        if key not in self.value_map:
            raise KeyError(f"Key '{key}' not found.")

        paired_key = self.key_map.get(key)

        # Delete both keys from value_map
        self.value_map.pop(key, None)
        self.value_map.pop(paired_key, None)

        # Delete both keys from key_map
        self.key_map.pop(key, None)
        self.key_map.pop(paired_key, None)

    def __repr__(self) -> str:
        """Returns a string representation of the `_DualKeyDict` instance.

        Returns:
            String representing the dictionary with keys and values.

        """
        return f"{type(self).__name__}({self.value_map})"

    def __contains__(self, item) -> bool:
        """Checks if a key is in the dictionary.

        Args:
            item: The key to check.

        Returns:
            `True` if the key is present in `value_map`; otherwise, `False`.
        """
        return item in self.value_map


def _command_to_dict(command: _CommandPrivate) -> _DualKeyDict:
    """Converts a given command into an args decision tree
    structure representing its options, subcommands, and their respective arguments.

    Args:
        command: The command object from which to extract information.

    Returns:
        A dictionary where the keys are command names and values are either
              subcommands (as nested dictionaries) or argument options (as lists of choices).
    """
    data = _DualKeyDict()

    for arg in command.positional_args:
        if arg.private.choices:
            data.add(" ".join(arg.private.choices), None, None)

    subcommands, args = command.get_commands_and_options()

    for arg in args:
        if arg.private.choices:
            value = arg.private.choices  # Tab complete choices.
        elif arg.private.takes_value:
            # Tab complete file paths.
            if arg.private.multiple_values:
                value = 2
            else:
                value = 1
        else:
            value = None  # Tab complete next arg.

        data.add(arg.private.long_name, arg.private.short_name or None, value)

    for command in subcommands:
        data.add(
            command.private.long_name,
            command.private.short_name or None,
            _command_to_dict(command.private),
        )

    return data


def _auto_complete_paths(current: str) -> List[str]:
    """Provide tab complete for file paths."""
    directory, filename = os.path.split(current)

    current_path = os.path.abspath(directory)
    # Don't complete paths if they can't be accessed
    if not os.access(current_path, os.R_OK):
        return []

    # List all files that start with ``filename``
    file_list = [
        path
        for path in os.listdir(current_path)
        if os.path.normcase(path).startswith(os.path.normcase(filename))
    ]

    paths = []
    for file in file_list:
        opt = os.path.join(current_path, file)
        comp_file = os.path.normcase(os.path.join(directory, file))
        if os.path.isfile(opt):
            paths.append(comp_file)
        elif os.path.isdir(opt):
            paths.append(f"{comp_file}/")

    return paths or [current]


def _autocomplete_args(command: _CommandPrivate, words: List) -> List[str]:
    """Provide autocompletion based on the app's command structure and typed words.

    Args:
        command: App to complete args for.
        words: Lis of typed words to complete.

    Returns:
        List of options to complete.

    """
    arg_decision_tree = _command_to_dict(command)
    active_arg = ""

    positional_args = [arg for arg in arg_decision_tree.keys() if " " in arg]
    for arg in positional_args:
        arg_decision_tree.remove(arg)

    word = ""
    for word in words:
        for index, arg in enumerate(positional_args):
            if word in arg.split(" "):
                positional_args.pop(index)
                word = ""
                break
        else:
            if positional_args:
                break

            if arg_decision_tree.get(word) and isinstance(
                arg_decision_tree.get(word), _DualKeyDict
            ):
                arg_decision_tree = arg_decision_tree.get(word)
                positional_args = [
                    arg for arg in arg_decision_tree.keys() if " " in arg
                ]
                for arg in positional_args:
                    arg_decision_tree.remove(arg)
                word = ""
                continue
            elif word in arg_decision_tree:
                active_arg = arg_decision_tree.get(word)
                arg_decision_tree.remove(word)
                word = ""
            elif isinstance(active_arg, (str, list, tuple)) and word in active_arg:
                active_arg = ""
                word = ""
            elif word.startswith("-"):
                active_arg = ""
            elif active_arg == 1 and os.path.exists(word) and not word.endswith("/"):
                active_arg = ""
                word = ""
            elif active_arg == 2 and os.path.isfile(word):
                word = ""

    if positional_args:
        commands = positional_args[0].split(" ")
        if word in positional_args[0]:
            return [cmd for cmd in commands if cmd.startswith(word)]
        else:
            return commands
    elif isinstance(active_arg, int):
        return _auto_complete_paths(word)
    elif active_arg:
        return [cmd for cmd in active_arg if cmd.startswith(word)] or active_arg
    else:
        if any(cmd.startswith(word) for cmd in arg_decision_tree.keys()):
            return [cmd for cmd in arg_decision_tree.keys() if cmd.startswith(word)]
        else:
            return [word]


def autocomplete(app: App) -> None:
    """Provide autocompletion based on the app's command structure.

    Args:
        app: The application to add tab completion to.

    """
    # Environment variable name for triggering autocompletion
    env_name = f"{app.private.name().replace('-', '_').upper()}_AUTO_COMPLETE"
    if not os.getenv(env_name):
        return

    # Get the current input and cursor position from the environment
    words = os.environ["COMP_WORDS"].split()  # All words typed so far
    words = words[1:]  # Remove name of EXE (application).
    print(" ".join(_autocomplete_args(app.private, words)))
    sys.exit(0)  # Stop execution after printing completions
