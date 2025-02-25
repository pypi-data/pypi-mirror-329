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
import platform
import sys
import textwrap

from clap_python import App, Arg


def validate_path(path: str) -> str:
    """Check that file path exists."""
    if os.path.exists(path):
        return ""
    return f"File path '{path}' does not exists."


def create_file(my_app: str, install_path):
    template = textwrap.dedent(
        f"""
        # {my_app} bash completion start
        _{my_app}_completion()
        {{
            COMPREPLY=( $( COMP_WORDS="${{COMP_WORDS[*]}}" \\
                           {my_app.upper()}_AUTO_COMPLETE=1 $1 ) )
        }}

        # Register the completion function for your app
        complete -o default -F _{my_app}_completion {my_app}
        # {my_app} bash completion end
        """
    )
    export_path = os.path.join(install_path, my_app)
    with open(export_path, "w") as f:
        f.write(template)
    print(f"File created at '{export_path}'")


def cli() -> dict:
    """Setup cli."""
    if platform.system() == "Windows":
        print("Windows not supported.")
        sys.exit(1)
    if platform.system() == "Darwin":
        install_path = "/usr/local/etc/bash_completion.d"
    else:
        install_path = "/etc/bash_completion.d"

    return (
        App()
        .arg_required_else_help(True)
        .arg(Arg("--name").required(True).help("Name of app to register. E.g cargo"))
        .arg(
            Arg("--output-path", "-o")
            .default(install_path)
            .validate(validate_path)
            .help("File path to install completion script at.")
        )
    ).parse_args()


def run() -> None:
    """Run application."""
    args = cli()
    create_file(args["name"], install_path=args["output_path"])
