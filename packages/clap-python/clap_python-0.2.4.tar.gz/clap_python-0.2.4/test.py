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
from datetime import datetime
from unittest import TestCase, mock

import clap_python.complete
from clap_python import App, Arg, ClapPyException, MutuallyExclusiveGroup, SubCommand
from clap_python.complete import _autocomplete_args

complex_app = (
    App()
    .arg(
        MutuallyExclusiveGroup()
        .arg(
            SubCommand("--env", "-e")
            .arg(
                Arg("env-name")
                .choices(["maya", "nuke", "houdini"])
                .help("Recipe name.")
            )
            .arg(
                MutuallyExclusiveGroup()
                .arg(Arg("--add").help("Add packages to env").multiple_values(True))
                .arg(Arg("--rm").help("Remove packages from env").multiple_values(True))
                .arg(Arg("--del").help("delete env"))
                .arg(Arg("--list").takes_value(False).help("List packages in env"))
                .arg(
                    SubCommand("--run").arg(
                        Arg("--command", "-c")
                        .default("bash")
                        .help("Command to execute when running env")
                    )
                )
                .arg(Arg("--editor").takes_value(False).help("open code editor"))
            )
        )
        .arg(Arg("--list", "-l").help("List available envs ").takes_value(False))
        .arg(
            Arg("--generate", "-g")
            .help("Interactive tool to setup new dev env.")
            .takes_value(False)
        )
        .arg(Arg("--new").help("Create new env."))
    )
    .arg(Arg("--verbose", "-v"))
)

simple_parser = App().arg(Arg("--hello")).arg(Arg("--items").multiple_values(True))

date_app = (
    App()
    .arg(Arg("--year", "-y").choices([str(date) for date in range(2019, 2029)]))
    .arg(Arg("--name"))
)

pip_app = (
    App("pip")
    .subcommand_required(True)
    .arg(
        SubCommand("install")
        .arg(Arg("requirement-specifier").required(False))
        .arg(
            Arg("-r", "--requirement")
            .value_name("requirements file")
            .help(
                "Install from the given requirements file. This option can be used multiple times."
            )
        )
        .arg(
            Arg("-e", "--editable")
            .value_name("--editable <path/url>")
            .help(
                'Install a project in editable mode (i.e. setuptools "develop mode") from a local project path or a VCS url.'
            )
        )
        .arg(
            Arg("--user").help(
                (
                    "Install to the Python user install directory for your platform. Typically "
                    "~/.local/, or %APPDATA%\Python on Windows. (See the Python documentation for "
                    "site.USER_BASE for full details.)"
                )
            )
        )
    )
    .arg(SubCommand("uninstall"))
    .arg(SubCommand("list"))
)


class TestApp(TestCase):
    def test_parser_101(self):
        expected_result = {"hello": "Joy", "items": ["a", "b"]}

        self.assertEqual(
            expected_result,
            simple_parser.parse_args(["--items", "a", "b", "--hello", "Joy"]),
        )

    def test_parser_102(self):
        with self.assertRaises(ClapPyException) as contex:
            simple_parser.private.parse(["--hello", "a", "b"], [], False)
            self.assertEquals(contex.exception.msg, "unrecognized arguments: b")

    def test_validate_multiple_values(self):
        def validate(value) -> str:
            try:
                int(value)
                return ""
            except ValueError:
                return f"Not able to convert '{value}' to int"

        app = App().arg(Arg("--add").multiple_values(True).validate(validate))

        expected_result = {"add": ["1", "100"]}

        self.assertEqual(expected_result, app.parse_args(["--add", "1", "100"]))

        with self.assertRaises(ClapPyException) as context:
            app.private.parse(["--add", "1", "0.1"], [], False)
            self.assertEqual(context.exception.msg, "Not able to convert '0.8' to int")

    def test_positional_args101(self):
        app = App().arg(Arg("data")).arg(Arg("value")).arg(Arg("--test"))

        expected_result = {"data": "a", "value": "bbbbbbbbb", "test": "yes"}
        self.assertEqual(
            expected_result, app.parse_args(["a", "bbbbbbbbb", "--test", "yes"])
        )

    def test_positional_args102(self):
        app = (
            App()
            .arg(Arg("files").multiple_values(True))
            .arg(Arg("--test").required(True))
        )
        expected_result = {
            "files": ["/path/to/file1.txt", "/path/to/file2.exr"],
            "test": "yes",
        }
        self.assertEqual(
            expected_result,
            app.parse_args(
                ["/path/to/file1.txt", "/path/to/file2.exr", "--test", "yes"]
            ),
        )

    def test_unknown_args(self):
        expected_result = {
            "list": False,
            "generate": False,
            "env": {
                "list": False,
                "editor": False,
                "env_name": "maya",
                "run": {"command": "mayapy", "unknown": ["/file/path"]},
            },
        }
        self.assertEqual(
            expected_result,
            complex_app.parse_known_args(
                ["--env", "maya", "--run", "-c", "mayapy", "--", "/file/path"]
            ),
        )

    def test_uncomplete_args(self):
        with self.assertRaises(ClapPyException) as contxt:
            complex_app.private.parse(["-e", "maya", "--run", "-c"], [], False)
        self.assertEqual(contxt.exception.msg, "expected one argument")

    def test_default_args_populated(self):
        expected_result = {
            "list": False,
            "generate": False,
            "env": {
                "list": False,
                "editor": False,
                "env_name": "maya",
                "run": {"command": "bash"},
            },
        }

        self.assertEqual(
            expected_result, complex_app.parse_args(["-e", "maya", "--run"])
        )

    def test_parse_args_with_unknown_not_enabled(self):
        with self.assertRaises(ClapPyException) as context:
            complex_app.private.parse(
                ["-e", "maya", "--run", "-c", "mayapy", "--", "/file/path"], [], False
            )
        self.assertEqual(context.exception.msg, "unrecognized arguments: --")

    @mock.patch("clap_python.sys.stdout.write")
    def test_missing_argument(self, std_out_write):
        with self.assertRaises(SystemExit):
            complex_app.parse_args(["--env", "maya", "-h"])

    def test_multiple_values(self):
        expected_result = {
            "list": False,
            "generate": False,
            "env": {
                "list": False,
                "editor": False,
                "env_name": "maya",
                "rm": ["package-a", "package-b"],
            },
        }
        self.assertEqual(
            expected_result,
            complex_app.parse_args(["-e", "maya", "--rm", "package-a", "package-b"]),
        )

    def test_required_args(self):
        app = App().arg(Arg("--test")).arg(Arg("--abc").required(True))
        with self.assertRaises(ClapPyException) as context:
            app.private.parse(["--test", "hello"], [], False)
        self.assertEqual(
            context.exception.msg, "the following arguments are required: --abc"
        )

    def test_mutually_exclusive_group101(self):
        with self.assertRaises(ClapPyException) as context:
            visited = []
            complex_app.private.parse(["-g", "--list"], visited, False)

        self.assertEqual(
            context.exception.msg,
            "argument --list not allowed with argument --generate",
        )

    def test_mutually_exclusive_group102(self):
        app = (
            App()
            .arg(MutuallyExclusiveGroup().arg(SubCommand("hello")).arg(Arg("--test")))
            .arg(Arg("--debug"))
        )

        with self.assertRaises(ClapPyException) as context:
            visited = []
            app.private.parse(["--test", "1", "hello"], visited, False)

        self.assertEqual(
            context.exception.msg, "argument hello not allowed with argument --test"
        )

    def test_subcommand_required(self):
        with self.assertRaises(ClapPyException) as context:
            pip_app.private.parse([], [], False)
        self.assertTrue(
            "requires a subcommand but one was not provided" in context.exception.msg
        )

    def test_value_parser_int(self):
        app = App().arg(Arg("--number").value_parser(int))
        expected_result = {"number": 101}
        self.assertEqual(expected_result, app.parse_args(["--number", "101"]))

        app = App().arg(Arg("--number").value_parser(float))
        expected_result = {"number": 101.0}
        self.assertEqual(expected_result, app.parse_args(["--number", "101"]))

    def test_value_parser_datetime(self):
        def to_datetime(value: str) -> datetime:
            return datetime.strptime(value, "%Y-%m-%d:%H:%M:%S")

        app = App().arg(Arg("--date-time").value_parser(to_datetime))
        expected_result = {"date_time": datetime(2024, 1, 1, 19, 0, 1)}
        self.assertEqual(
            expected_result, app.parse_args(["--date-time", "2024-01-01:19:00:01"])
        )

    @mock.patch("clap_python.sys.stdout.write")
    def test_version_short_flag(self, std_out_write):
        app = App().version("1.51.0").arg(Arg("data"))

        expected_result = f"{os.path.basename(sys.argv[0])} 1.51.0\n"
        with self.assertRaises(SystemExit):
            app.parse_args(["-V"])
        std_out_write.assert_called_with(expected_result)

    @mock.patch("clap_python.sys.stdout.write")
    def test_version_long_flag(self, std_out_write):
        app = App().version("1.51.0").arg(Arg("data"))

        expected_result = f"{os.path.basename(sys.argv[0])} 1.51.0\n"
        with self.assertRaises(SystemExit):
            app.parse_args(["--version"])
        std_out_write.assert_called_with(expected_result)

    @mock.patch("clap_python.sys.stdout.write")
    def test_help_message(self, std_out_write):
        expected_result = "Usage:  [--year -y YEAR] [--name NAME] \n\nOptions:\n  --help -h        Show this help message and exit\n  --year -y YEAR\n  --name NAME\n\n"
        with self.assertRaises(SystemExit):
            date_app.parse_args(["--year", "2024", "--help"])
        std_out_write.assert_called_with(expected_result)
        with self.assertRaises(SystemExit):
            date_app.parse_args(["-h"])
        std_out_write.assert_called_with(expected_result)

    def test_sub_command_and_arg_with_multiple_values101(self):
        app = App().arg(Arg("--names").multiple_values(True)).arg(SubCommand("abc"))
        expected_result = {"names": ["test"], "abc": {}}
        self.assertEqual(expected_result, app.parse_args(["--names", "test", "abc"]))

    def test_sub_command_and_arg_with_multiple_values102(self):
        app = App().arg(Arg("--names").multiple_values(True)).arg(SubCommand("abc"))
        with self.assertRaises(ClapPyException) as context:
            app.private.parse(["--names", "abc"], [], False)
        self.assertEqual("expected at least one argument", context.exception.msg)

    def test_required_group(self):
        app = App().arg(
            MutuallyExclusiveGroup()
            .arg(Arg("--a").takes_value(False))
            .arg(Arg("--b").takes_value(False))
            .required(True)
        )
        with self.assertRaises(ClapPyException) as context:
            app.private.parse([], [], False)
        self.assertEqual(
            "One of the following arguments are required: --a | --b",
            context.exception.msg,
        )

    def test_optional_positional_args(self):
        with self.assertRaises(ClapPyException) as context:
            pip_app.private.parse(["install", "-e", ".", "hello"], [], False)
        self.assertEqual("unrecognized arguments: hello", context.exception.msg)

        self.assertEqual(
            {"install": {"requirement_specifier": "."}},  # Expected result
            pip_app.parse_args(["install", "."]),
        )


def mock_is_file(value):
    return value in [os.path.join(os.getcwd(), f) for f in ("file1.png", "file2.png")]


def mock_is_dir(value):
    return value in [os.path.join(os.getcwd(), f) for f in ("folder22",)]


class TestAutoComplete(TestCase):
    def test_complete_date(self):
        expected_result = ["2019"]
        self.assertEqual(
            expected_result, _autocomplete_args(date_app.private, ["--year", "201"])
        )

    def test_complete_next_arg(self):
        expected_result = ["--help", "-h", "--name"]
        self.assertEqual(
            expected_result, _autocomplete_args(date_app.private, ["--year", "2025"])
        )

    def test_complete_arg_that_takes_no_value(self):
        app = App().arg(Arg("--name")).arg(Arg("--sync").takes_value(False))
        expected_result = ["--help", "-h", "--name"]
        self.assertEqual(expected_result, _autocomplete_args(app.private, ["--sync"]))

    def test_help_arg(self):
        expected_result = ["--help"]
        self.assertEqual(
            expected_result, _autocomplete_args(date_app.private, ["--year", "--he"])
        )

    def test_unknown_word(self):
        expected_result = ["te"]

        self.assertEqual(
            expected_result,
            _autocomplete_args(complex_app.private, ["-e", "maya", "te"]),
        )

    def test_complete_sub_command_without_prefix(self):
        expected_result = ["install"]
        self.assertEqual(
            expected_result, _autocomplete_args(pip_app.private, ["instal"])
        )

        expected_result = [
            "--help",
            "-h",
            "-r",
            "--requirement",
            "-e",
            "--editable",
            "--user",
        ]
        self.assertEqual(
            expected_result, _autocomplete_args(pip_app.private, ["install"])
        )

    @mock.patch("clap_python.complete.os.path.isdir", side_effect=mock_is_dir)
    @mock.patch("clap_python.complete.os.path.isfile", side_effect=mock_is_file)
    @mock.patch("clap_python.complete.os.path.exists", side_effect=mock_is_file)
    @mock.patch(
        "clap_python.complete.os.path.split", side_effect=lambda value: ("", value)
    )
    @mock.patch(
        "clap_python.complete.os.listdir",
        return_value=["file1.png", "file2.png", "folder22"],
    )
    def test_autocomplete_multiple_args(
        self, mock_listdir, mock_split, mock_exists, mock_is_file, mock_is_dir
    ):
        app_test = App().arg(Arg("-c")).arg(Arg("--files").multiple_values(True))
        expected_result = ["folder22/"]
        self.assertEqual(
            expected_result,
            clap_python.complete._autocomplete_args(
                app_test.private, ["--files", "file1.png", "folder"]
            ),
        )
