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

from dataclasses import dataclass, field
from enum import IntEnum


class AnsiColor(IntEnum):
    """Enum for ANSI color codes."""

    Black = 30
    Red = 31
    Green = 32
    Yellow = 33
    Blue = 34
    Magenta = 35
    Cyan = 36
    White = 37
    BrightBlack = 90
    BrightRed = 91
    BrightGreen = 92
    BrightYellow = 93
    BrightBlue = 94
    BrightMagenta = 95
    BrightCyan = 96
    BrightWhite = 97


class AnsiStyle(IntEnum):
    """Enum for ANSI text styles."""

    Normal = 0
    Bold = 1
    Dim = 2
    Italic = 3
    Underline = 4
    Blink = 5
    Inverse = 7
    Hidden = 8
    Strikethrough = 9


@dataclass()
class TextStyle:
    """Class representing how to format and style text.

    Attributes:
        color: The color of the text.
        style: The style of the text (default is Normal).
    """

    color: AnsiColor
    style: AnsiStyle = AnsiStyle.Normal


@dataclass()
class _PrivateStyle:
    """Class holding data for styling clap_python help messages and output.

    This class encapsulates different styles used in the application,
    allowing for customized styling of usage text, headers, errors,
    flags, and tips.

    Attributes:
        flags: Style for flags.
        usage: Style for usage information.
        tip: Style for tips.
        headers: Style for headers.
        error: Style for error messages.
        value_names: Style for flag names.

    """

    flags: TextStyle = field(default_factory=lambda: TextStyle(AnsiColor.White))
    usage: TextStyle = field(default_factory=lambda: TextStyle(AnsiColor.White))
    tip: TextStyle = field(default_factory=lambda: TextStyle(AnsiColor.White))

    headers: TextStyle = field(default_factory=lambda: TextStyle(AnsiColor.White))
    error: TextStyle = field(default_factory=lambda: TextStyle(AnsiColor.White))
    value_names: TextStyle = field(default_factory=lambda: TextStyle(AnsiColor.White))


class Style:
    """Class for managing text styles.

    This class allows you to set and retrieve styles for different
    text elements in a terminal application. You can customize styles
    for usage information, headers, error messages, flags, and tips.

    """

    def __init__(self):
        """Initializes the Style instance with default styles."""
        self.private = _PrivateStyle()

    def usage(self, style: TextStyle) -> Style:
        """Sets the style for usage information.

        Args:
            style (TextStyle): The text style to be set for usage.

        Returns:
            Style: The current Style instance for method chaining.

        """
        self.private.usage = style
        return self

    def headers(self, style: TextStyle) -> Style:
        """Sets the style for headers.

        Args:
            style (TextStyle): The text style to be set for headers.

        Returns:
            Style: The current Style instance for method chaining.

        """
        self.private.headers = style
        return self

    def error(self, style: TextStyle) -> Style:
        """Sets the style for error messages.

        Args:
            style (TextStyle): The text style to be set for error messages.

        Returns:
            Style: The current Style instance for method chaining.

        """
        self.private.error = style
        return self

    def flags(self, style: TextStyle) -> Style:
        """Sets the style for flags.

        Args:
            style (TextStyle): The text style to be set for flags.

        Returns:
            Style: The current Style instance for method chaining.

        """
        self.private.flags = style
        return self

    def value_names(self, style: TextStyle) -> Style:
        """Sets the style for flag names.

        Args:
            style (TextStyle): The text style to be set for flag names.

        Returns:
            Style: The current Style instance for method chaining.

        """
        self.private.value_names = style
        return self

    def tip(self, style: TextStyle) -> Style:
        """Sets the style for tips.

        Args:
            style (TextStyle): The text style to be set for tips.

        Returns:
            Style: The current Style instance for method chaining.

        """
        self.private.tip = style
        return self
