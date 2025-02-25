# clap-python

> **Command Line Argument Parser for Python**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue?style=flat-square)](LICENSE-APACHE)
![PyPi](https://img.shields.io/pypi/v/clap_python)

Licensed under [Apache 2.0](LICENSE-APACHE).

## About

A full-featured, fast Command Line Argument Parser for Python 

For more details, see:
- [docs](https://clap-python.readthedocs.io/en/latest/)
- [examples](examples/)

## Quick Start
```bash
pip install clap_python
```

```python
from clap_python import App, Arg

app = (
    App()
    .version("0.1.0")  # Version of the app.
    .arg_required_else_help(True)  # If no args passed show help message.
    .arg(Arg("--name", "-n").help("Name of the person to greet").required(True))
    .arg(
        Arg("--count", "-c")
        .help("Number of times to greet")
        .default(1)
        .value_parser(int)  # tell the parser to cast arg to int.
    )
)

if __name__ == "__main__":
    args = app.parse_args()
    for _ in range(args["count"]):
        print(f"Hello {args['name']}!")

```

## Positionals

```python
from clap_python import App, Arg

if __name__ == "__main__":
    args = App().arg(Arg("names").multiple_values(True)).parse_args()
    print(f"names: {args['names']}")
```

## Autocomplete
```python
from clap_python import App, Arg
from clap_python.complete import autocomplete

app = App().arg(Arg("-c")).arg(Arg("--files").multiple_values(True))
autocomplete(app) # Enable autocompletion
args = app.parse_args() # Parse arguments
print(args)
```
You can read more at [docs](https://clap-python.readthedocs.io/en/latest/usage.html)
