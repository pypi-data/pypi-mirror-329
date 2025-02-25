Cargo-Like CLI Example
----------------------

This example defines a Cargo-like CLI for managing Rust-like projects using `clap_python`. The CLI supports commands like `new`, `build`, `run`, `test`, and more.


.. code-block:: python

   import clap_python
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
                .arg(Arg("--verbose", "-v").help("Enable verbose output").takes_value(False))
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


### Running the Example

.. code-block:: bash

   # Create a new package
   python examples/cargo.py new my_package

   # Build the package in release mode
   python examples/cargo.py build --release

   # Run the package with custom arguments
   python examples/cargo.py run -- args_to_binary

   # Test the package
   python examples/cargo.py test

   # Clean build artifacts
   python examples/cargo.py clean

### Explanation

The CLI example mimics a subset of Cargo's functionalities:

- **Subcommands**:
  - `new`: Creates a new Rust package.
  - `build`: Compiles the package.
  - `run`: Executes the package.
  - `test`: Runs tests.
  - `clean`: Cleans up build artifacts.
  - `update`, `doc`, `bench`, `check`: Other functionalities.

- **Arguments**:
  - `--release`: A common flag to switch to release mode for several commands.
  - `--verbose`, `-v`: Enable verbose output.

### Output Example

When you run the example ``cargo.py build --verbose`` , parsed arguments will be printed in JSON format. Here's an example of what you might see:

.. code-block:: json

    {
        "V": false,
        "list": false,
        "locked": false,
        "offline": false,
        "frozen": false,
        "build": {
            "release": false,
            "verbose": true
        }
    }



