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

from clap_python import App, Arg, SubCommand
from clap_python.complete import autocomplete


def cli() -> App:
    """The pip-like command line interface."""
    return (
        App("pip")
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
                    "Install to the Python user install directory for your platform. Typically ~/.local/, or %APPDATA%\Python on Windows. (See the Python documentation for site.USER_BASE for full details.)"
                )
            )
        )
        .arg(
            SubCommand("uninstall")
            .help_heading("Uninstall Options")
            .arg(
                Arg("-r", "--requirement")
                .value_name("--requirement <file>")
                .help(
                    "Uninstall all the packages listed in the given requirements file.  This option can be used multiple times."
                )
            )
            .arg(
                Arg("-y", "--yes").help(
                    "Don't ask for confirmation of uninstall deletions."
                )
            )
            .help_heading("General Options")
            .arg(
                Arg("--debug").help(
                    "Let unhandled exceptions propagate outside the main subroutine, instead of logging them to stderr."
                )
            )
        )
        .arg(
            SubCommand("list")
            .arg(
                Arg("-o", "--outdated")
                .help("List outdated packages")
                .takes_value(False)
            )
            .arg(
                Arg("-e", "--editable")
                .help("List editable projects.")
                .takes_value(False)
            )
            .arg(
                Arg("--user")
                .help("Only output packages installed in user-site.")
                .takes_value(False)
            )
        )
    )


# Placeholder for argument handling logic
if __name__ == "__main__":
    import json

    app = cli()
    autocomplete(app)
    args = app.parse_args()
    print(json.dumps(args, indent=4))
