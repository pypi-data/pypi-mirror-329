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
from clap_python import App, Arg
from clap_python.style import AnsiColor, AnsiStyle, Style, TextStyle

styles = (
    Style()
    .usage(TextStyle(AnsiColor.Blue, AnsiStyle.Bold))
    .headers(TextStyle(AnsiColor.Blue, AnsiStyle.Bold))
    .error(TextStyle(AnsiColor.Red))
    .flags(TextStyle(AnsiColor.Yellow, AnsiStyle.Bold))
    .value_names(TextStyle(AnsiColor.Yellow))
    .tip(TextStyle(AnsiColor.Green))
)


def cli() -> dict:
    return (
        App()
        .version("1.12.4")
        .style(styles)
        .width(170)
        .arg(
            Arg("--verbose", "-v")
            .help("show all command lines while building")
            .takes_value(False)
        )
        .arg(
            Arg("--quiet")
            .help("don't show progress status, just command output")
            .takes_value(False)
        )
        .arg(
            Arg("-C").value_name("DIR").help("change to DIR before doing anything else")
        )
        .arg(
            Arg("-f")
            .value_name("FILE")
            .help("specify input build file [default=build.ninja]")
        )
        .arg(
            Arg("-j")
            .value_name("N")
            .help(
                "run N jobs in parallel (0 means infinity) [default=10 on this system]"
            )
        )
        .arg(
            Arg("-k")
            .value_name("N")
            .help("keep going until N jobs fail (0 means infinity) [default=1]")
        )
        .arg(
            Arg("-l")
            .value_name("N")
            .help("do not start new jobs if the load average is greater than N")
        )
        .arg(
            Arg("-n")
            .help("dry run (don't run commands but act like they succeeded)")
            .takes_value(False)
        )
        .arg(
            Arg("-d")
            .value_name("MODE")
            .help("enable debugging (use '-d list' to list modes)")
        )
        .arg(
            Arg("-t")
            .value_name("Tool")
            .help(
                (
                    "run a subtool (use '-t list' to list subtools) terminates "
                    "toplevel options; further flags are passed to the tool"
                )
            )
        )
        .arg(
            Arg("-w")
            .value_name("FLAG")
            .help("adjust warnings (use '-w list' to list warnings)")
        )
    ).parse_args()


if __name__ == "__main__":
    args = cli()
    print(args)
