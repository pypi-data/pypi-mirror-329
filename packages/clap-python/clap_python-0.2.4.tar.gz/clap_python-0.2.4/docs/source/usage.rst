Usage
=====


Overview
--------

`clap_python` allows you to:

- Define commands and subcommands
- Add arguments with options, flags, and values
- Create custom help messages and descriptions
- Style the output using ANSI colors and styles

Key features:

- Automatic help generation (`--help`)
- Error reporting for invalid input
- Support for mutually exclusive argument groups

Basic Example
-------------

This is a simple example that demonstrates how to create a basic CLI using `clap_python`:

.. code-block:: python

   from clap_python import App, Arg

   def cli() -> dict:
       return (
           App()
           .about("MyApp is a simple command-line tool.")
           .arg_required_else_help(True)
           .arg(
               Arg("--name")
               .help("Name of the person to greet")
           )
           .parse_args()
       )

   if __name__ -- "__main__":
       args = cli()
       print(args)

In this example:

- The app requires at least one argument (`--name`).
- Help and usage instructions are automatically generated with the `.help()` method.

Key Components
--------------

App
---

The `App` object defines the overall structure of the command-line tool. This includes commands, subcommands, and global configurations.

.. code-block:: python

   App()
   .about("Description of your CLI tool")
   .arg_required_else_help(True)
   .style(custom_styles)
   .parse_known_args()

- **about(description)**: Defines the description of the application, shown in the help output.
- **arg_required_else_help(flag)**: If `True`, the help message is displayed when no arguments are provided.
- **style(style)**: Optionally defines custom styles for usage, headers, errors, etc.
- **parse_known_args()**: Parses command-line arguments and returns them as a dictionary.

SubCommand
----------

`SubCommand` defines a command that can have its own arguments and subcommands, such as `git commit` or `cargo build`.

.. code-block:: python

   SubCommand("build")
   .about("Compile the project")
   .arg(Arg("--release").help("Build in release mode"))

- **about(description)**: Sets the description for the subcommand.
- **arg(argument)**: Adds an argument to the subcommand.

Arg
---

`Arg` defines an argument that can be positional or optional (like flags). It can take values and have additional configurations.

.. code-block:: python

   Arg("filename").help("File to process")  # Positional argument.
   Arg("--release").takes_value(False).help("Enable release mode")
   Arg("--age").value_parser(int)  # Cast value to int.

- **help(text)**: A description of the argument for the help message.
- **required(flag)**: Marks an argument as required.
- **takes_value(flag)**: If `True`, the argument takes a value (useful for options like `--config <file>`).
- **multiple_values(flag)**: If `True`, allows multiple values for the argument.
- **choices([values])**: Limits the valid values for the argument to a predefined set.
- **value_parser(value)** Function to cast value (default is ``str``).

MutuallyExclusiveGroup
----------------------

`MutuallyExclusiveGroup` ensures that only one of the specified arguments in the group can be provided at a time.

.. code-block:: python

   MutuallyExclusiveGroup()
   .arg(Arg("--add").help("Add a package"))
   .arg(Arg("--rm").help("Remove a package"))

Style and TextStyle
-------------------

`clap_python` supports ANSI styling for command-line output. You can customize usage messages, headers, flags, and errors with colors and styles.

.. code-block:: python

   from clap_python.style import AnsiColor, AnsiStyle, Style, TextStyle

   styles = (
       Style()
       .usage(TextStyle(AnsiColor.Green, AnsiStyle.Bold))
       .headers(TextStyle(AnsiColor.Yellow))
       .flags(TextStyle(AnsiColor.Cyan, AnsiStyle.Bold))
       .error(TextStyle(AnsiColor.Red))
   )

- **usage(style)**: Sets the style for the usage message.
- **headers(style)**: Sets the style for headers in the help message.
- **flags(style)**: Sets the style for flags (e.g., `--verbose`).
- **error(style)**: Sets the style for error messages.

Advanced Features
----------------=

Subcommands with Arguments
--------------------------

In `clap_python`, subcommands can have their own arguments and options, just like top-level commands. For example:

.. code-block:: python

   SubCommand("commit")
   .about("Record changes to the repository")
   .arg(Arg("-m", "--message").help("Commit message"))
   .arg(Arg("--amend").takes_value(False).help("Amend the previous commit"))

Positional and Optional Arguments
---------------------------------

Arguments can be either positional or optional (flags). Positional arguments are required by default, while optional arguments (flags) can be turned on or off.

.. code-block:: python

   Arg("file").help("File to process")
   Arg("--verbose", "-v").takes_value(False).help("Enable verbose mode")

Multiple Values
---------------

To allow an argument to accept multiple values, use the `.multiple_values(True)` method:

.. code-block:: python

   Arg("files").multiple_values(True).help("Files to add")

Argument Choices
----------------

You can restrict argument values to a set of predefined choices using `.choices()`:

.. code-block:: python

   Arg("env").choices(["development", "production"]).help("Specify the environment")

Example: Git-like CLI
---------------------

Here is an example of how to create a Git-like CLI application using `clap_python`:

.. code-block:: python

   from clap_python import App, Arg, SubCommand

   def cli() -> dict:
       return (
           App()
           .about("A Git-like CLI tool")
           .arg(SubCommand("init").about("Initialize a new repository"))
           .arg(
               SubCommand("commit")
               .arg(Arg("-m", "--message").help("Commit message"))
               .about("Record changes to the repository")
           )
           .arg(
               SubCommand("clone")
               .arg(Arg("repository").help("The repository to clone"))
               .about("Clone a repository into a new directory")
           )
           .parse_known_args()
       )

   if __name__ -- "__main__":
       args = cli()
       print(args)

In this example:

- The CLI has three subcommands: `init`, `commit`, and `clone`.
- Each subcommand can have its own arguments, such as the `-m` option for `commit`.



Autocompletion
----------------------------------------------

The `autocomplete` function in `clap_python` provides tab-completion functionality for
applications, helping users discover available commands, options, and file paths as they
type. This documentation explains how to set up and use autocompletion for a command-line
application built with `clap_python`.

To enable autocompletion for your application, follow these steps:

1. **Define Your Application**: Set up your command-line application with necessary commands, options, and arguments using `App` and `Arg`.
2. **Enable Autocompletion**: Call the `autocomplete` function with your `App` instance.
3. **Parse Arguments**: Use `app.parse_args()` to parse user input and enable autocompletion.
4. **Register your app** For bash to tab-complete your app you need to generate a file.

Autocompletion Example
----------------------

The following example demonstrates how to enable autocompletion in a `clap_python` application:

Create the app.

.. code-block:: shell

    touch my_cool_app
    chmod +x my_cool_app

Code of ``my_cool_app``

.. code-block:: python

    #!/usr/bin/env python

    from clap_python import App, Arg
    from clap_python.complete import autocomplete

    app = App().arg(Arg("-c")).arg(Arg("--files").multiple_values(True))
    autocomplete(app) # Step 2: Enable autocompletion
    args = app.parse_args() # Step 3: Parse arguments
    print(args)


Register the app

.. code-block:: shell

    clap-python-register-complete-app --name my_cool_app
    File created at '/usr/local/etc/bash_completion.d/my_cool_app'

If your on MacOS you need to tell ``bash`` to source your ``bash_completion`` dir.
In your ``~/.bashrc`` make sure you have

.. code-block:: bash

    [ -f /usr/local/etc/bash_completion ] && . /usr/local/etc/bash_completion


Summary
-------

`clap_python` is a flexible and easy-to-use Python library for building command-line tools. It provides a clear and intuitive API for defining commands, subcommands, and arguments, while offering powerful features like mutually exclusive groups, argument validation, and ANSI-styled output. With `clap_python`, you can create sophisticated CLI tools in a Pythonic way.
