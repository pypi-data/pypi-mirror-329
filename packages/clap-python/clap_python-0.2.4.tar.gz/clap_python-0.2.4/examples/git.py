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

docs = """
MyGit is a command-line tool that mimics Git functionalities.

Supported commands:
- init: Initialize a new Git repository
- clone: Clone a repository into a new directory
- add: Add file contents to the index
- commit: Record changes to the repository
- status: Show the working tree status
- log: Show commit logs
- push: Update remote refs along with associated objects
- pull: Fetch from and integrate with another repository or a local branch
"""


# The Git-like command line structure
def cli() -> dict:
    return (
        App()
        .about(docs)
        .arg_required_else_help(True)
        .arg(SubCommand("init").about("Initialize a new Git repository"))
        .arg(
            SubCommand("clone")
            .arg(Arg("repository").help("The repository to clone"))
            .about("Clone a repository into a new directory")
        )
        .arg(
            SubCommand("add")
            .arg(Arg("files").help("Files to add to the index").multiple_values(True))
            .about("Add file contents to the index")
        )
        .arg(
            SubCommand("commit")
            .arg(Arg("-m", "--message").help("Commit message"))
            .arg(Arg("--amend").takes_value(False).help("Amend the previous commit"))
            .arg(
                Arg("--no-edit")
                .takes_value(False)
                .help("Use the previous commit message without editing")
            )
            .about("Record changes to the repository")
        )
        .arg(SubCommand("status").about("Show the working tree status"))
        .arg(
            SubCommand("log")
            .arg(Arg("--oneline").takes_value(False).help("Show logs as a summary"))
            .arg(
                Arg("--graph")
                .takes_value(False)
                .help("Show logs with a graph of the commit history")
            )
            .about("Show commit logs")
        )
        .arg(
            SubCommand("push")
            .arg(Arg("repository").help("The remote repository").required(False))
            .arg(Arg("branch").help("The branch to push").required(False))
            .about("Update remote refs along with associated objects")
        )
        .arg(
            SubCommand("pull")
            .arg(Arg("repository").help("The remote repository").required(False))
            .arg(Arg("branch").help("The branch to pull from").required(False))
            .about("Fetch from and integrate with another repository or a local branch")
        )
        .arg(
            SubCommand("checkout")
            .arg(Arg("branch").help("Branch name or commit hash to checkout"))
            .about("Switch branches or restore working tree files")
        )
        .arg(
            SubCommand("merge")
            .arg(Arg("branch").help("Branch to merge into the current branch"))
            .about("Join two or more development histories together")
        )
        .arg(
            SubCommand("branch")
            .arg(
                Arg("branch_name")
                .help("Name of the new branch to create")
                .required(False)
            )
            .arg(Arg("--delete", "-d").help("Delete a branch").required(False))
            .about("List, create, or delete branches")
        )
        .arg(
            SubCommand("remote")
            .arg(
                Arg("command")
                .choices(["add", "remove", "show"])
                .help("Manage set of tracked repositories")
            )
            .arg(Arg("remote_name").help("Name of the remote").required(False))
            .arg(Arg("url").help("URL of the remote repository").required(False))
            .about("Manage tracked remote repositories")
        )
        .arg(Arg("--verbose", "-v").help("Enable verbose output").required(False))
        .parse_args()
    )


if __name__ == "__main__":
    args = cli()
    import json

    print(json.dumps(args, indent=4))

# Example of how this could work:
# Running with "checkout master"
