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
from clap_python import App, Arg, MutuallyExclusiveGroup


def cli() -> dict:
    return (
        App()
        .about("oiiotool CLI - Image manipulation tool using OpenImageIO.")
        .arg_required_else_help(True)  # Show help if no args are provided
        .arg(Arg("--input", "-i").required(True).help("Input image file"))
        .arg(
            MutuallyExclusiveGroup()  # Mutually exclusive input options
            .arg(Arg("--resize").help("Resize the image"))
            .arg(Arg("--crop").help("Crop the image"))
            .arg(Arg("--rotate").help("Rotate the image"))
            .arg(Arg("--flip").takes_value(False).help("Flip the image vertically"))
            .arg(Arg("--flop").takes_value(False).help("Flip the image horizontally"))
            .arg(Arg("--add").help("Composite another image").multiple_values(True))
            .arg(Arg("--sub").help("Subtract another image").multiple_values(True))
            .arg(
                Arg("--mul").help("Multiply image by a constant").multiple_values(True)
            )
        )
        .arg(
            Arg("--output", "-o").help(
                "Output image file"
            )  # Subcommand for specifying output files
        )
        .arg(Arg("--list").help("List available operations").takes_value(False))
        .arg(
            Arg("--info")
            .help("Display information about the input image")
            .takes_value(False)
        )
        .arg(Arg("--verbose", "-v").help("Enable verbose output").takes_value(False))
        .parse_known_args()
    )


if __name__ == "__main__":
    args = cli()
    import json

    print(json.dumps(args, indent=4))

# Example of how this could work:
# Running with "--input image.jpg --resize 800x600 --output result.jpg"
