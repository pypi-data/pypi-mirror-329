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
from clap_python.style import AnsiColor, AnsiStyle, Style, TextStyle

docs = """
Cargo is a command-line tool that mimics Cargo functionalities for managing Rust projects."""

styles = (
    Style()
    .usage(TextStyle(AnsiColor.Green, AnsiStyle.Bold))
    .headers(TextStyle(AnsiColor.Green, AnsiStyle.Bold))
    .error(TextStyle(AnsiColor.Red))
    .flags(TextStyle(AnsiColor.Cyan, AnsiStyle.Bold))
    .value_names(TextStyle(AnsiColor.Cyan))
    .tip(TextStyle(AnsiColor.Green))
)


def cli() -> dict:
    """The Cargo-like command line structure"""
    return (
        App()
        .about(docs)
        .arg_required_else_help(True)
        .arg(
            SubCommand("new")
            .arg(Arg("package_name").help("The name of the new package"))
            .arg(
                Arg("--bin")
                .takes_value(False)
                .help("Create a binary application package")
            )
            .arg(Arg("--lib").takes_value(False).help("Create a library package"))
            .about("Create a new Rust package")
        )
        .arg(
            SubCommand("build")
            .arg(
                Arg("--release")
                .takes_value(False)
                .help("Build artifacts in release mode with optimizations")
            )
            .arg(Arg("--target").help("Build for the target triple"))
            .arg(
                Arg("--verbose", "-v").help("Enable verbose output").takes_value(False)
            )
            .about("Compile the current package")
        )
        .arg(
            SubCommand("run")
            .arg(
                Arg("--release")
                .takes_value(False)
                .help("Run the binary in release mode")
            )
            .arg(Arg("--example").help("Run a specific example from the package"))
            .arg(
                Arg("args")
                .help("Arguments to pass to the binary")
                .multiple_values(True)
                .required(False)
            )
            .about("Run a binary or example of the local package")
        )
        .arg(
            SubCommand("test")
            .arg(Arg("--release").takes_value(False).help("Run tests in release mode"))
            .arg(Arg("--verbose", "-v").help("Enable verbose output"))
            .about("Run the tests")
        )
        .arg(
            SubCommand("check")
            .arg(Arg("--release").takes_value(False).help("Check code in release mode"))
            .arg(Arg("--verbose", "-v").help("Enable verbose output").required(False))
            .about("Check the code without compiling")
        )
        .arg(
            SubCommand("clean")
            .arg(
                Arg("--release")
                .takes_value(False)
                .help("Clean release build artifacts")
            )
            .about("Remove artifacts that Cargo has generated")
        )
        .arg(
            SubCommand("update")
            .arg(Arg("--verbose", "-v").help("Enable verbose output"))
            .about("Update dependencies as recorded in the lock file")
        )
        .arg(
            SubCommand("doc")
            .arg(
                Arg("--open")
                .takes_value(False)
                .help("Open the documentation in a web browser after building it")
            )
            .arg(
                Arg("--no-deps")
                .takes_value(False)
                .help("Do not build documentation for dependencies")
            )
            .about("Build documentation for the project")
        )
        .arg(
            SubCommand("bench")
            .arg(
                Arg("--release")
                .takes_value(False)
                .help("Run benchmarks in release mode")
            )
            .arg(Arg("--verbose", "-v").help("Enable verbose output"))
            .about("Run benchmarks")
        )
        # Optional arguments
        .arg(
            Arg("-V", "--version")
            .takes_value(False)
            .help("Print version info and exit")
        )
        .arg(Arg("--list").takes_value(False).help("List installed commands"))
        .arg(
            Arg("--explain").help(
                "Provide a detailed explanation of a rustc error message"
            )
        )
        .arg(
            Arg("--color")
            .choices(["auto", "always", "never"])
            .help("Coloring: auto, always, never")
        )
        .arg(Arg("-C").help("Change to DIRECTORY before doing anything"))
        .arg(
            Arg("--locked")
            .takes_value(False)
            .help("Assert that Cargo.lock will remain unchanged")
        )
        .arg(
            Arg("--offline")
            .takes_value(False)
            .help("Run without accessing the network")
        )
        .arg(
            Arg("--frozen")
            .takes_value(False)
            .help("Equivalent to specifying both --locked and --offline")
        )
        .arg(Arg("--config").help("Override a configuration value (KEY=VALUE)"))
        .arg(Arg("-Z").help("Unstable (nightly-only) flags to Cargo"))
        .style(styles)
        .parse_known_args()
    )


# Placeholder for argument handling logic
if __name__ == "__main__":
    args = cli()
    import json

    print(json.dumps(args, indent=4))

    # Handle logic based on parsed arguments
