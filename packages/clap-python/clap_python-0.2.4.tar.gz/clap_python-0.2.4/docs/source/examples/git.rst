
Git-Like CLI Example
====================

This section provides an example of how to build a Git-like command-line interface (CLI) using the `clap_python` library. The example demonstrates how to implement common Git commands like `init`, `clone`, `commit`, `status`, and more, along with their respective options and arguments.

Introduction
------------

The example `MyGit` CLI mimics the core functionalities of the Git version control system. Supported commands include:

- `init`: Initialize a new Git repository
- `clone`: Clone a repository into a new directory
- `add`: Add file contents to the index
- `commit`: Record changes to the repository
- `status`: Show the working tree status
- `log`: Show commit logs
- `push`: Update remote refs along with associated objects
- `pull`: Fetch from and integrate with another repository or a local branch
- `checkout`: Switch branches or restore working tree files
- `merge`: Join two or more development histories together
- `branch`: List, create, or delete branches
- `remote`: Manage tracked remote repositories

### Example Code

Here is the full Python code for creating this Git-like CLI:

.. code-block:: python

   from clap_python import App, Arg, SubCommand

   docs = '''
   MyGit is a command-line tool that mimics Git functionalities.
   Supported commands include: init, clone, add, commit, status, log, push, pull, and more.
   '''

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

### Running the Example

.. code-block:: bash

   # Initialize a new Git repository
   python examples/git.py init

   # Clone a repository
   python examples/git.py clone https://github.com/example/repo.git

   # Add files to the staging area
   python examples/git.py add file1.txt file2.txt

   # Commit the changes with a message
   python examples/git.py commit -m "Initial commit"

   # Check the status of the working directory
   python examples/git.py status

   # View the commit logs in summary format
   python examples/git.py log --oneline

   # Push changes to the remote repository
   python examples/git.py push origin main

   # Pull updates from a remote repository
   python examples/git.py pull origin main

   # Switch to a different branch
   python examples/git.py checkout feature_branch

   # Merge a branch into the current branch
   python examples/git.py merge feature_branch

   # Create a new branch
   python examples/git.py branch new_feature

   # Delete an existing branch
   python examples/git.py branch -d old_feature

   # Add a new remote repository
   python examples/git.py remote add origin https://github.com/example/repo.git

### Explanation

The example implements several common Git subcommands:

- **init**: Initializes a new Git repository.
- **clone**: Clones an existing repository.
- **add**: Adds files to the Git index.
- **commit**: Commits staged changes to the repository.
- **status**: Shows the status of the working directory.
- **log**: Displays the commit history.
- **push**: Pushes commits to a remote repository.
- **pull**: Fetches and merges changes from a remote repository.
- **checkout**: Switches to a different branch or commit.
- **merge**: Merges another branch into the current branch.
- **branch**: Manages Git branches (create, list, delete).
- **remote**: Manages remote repositories (add, remove, show).

### Output Example

When you run the example, the CLI will parse the arguments and display them as a JSON object. Here's an example output when running the `checkout` command:

.. code-block:: json

    {
        "checkout": {
            "branch": "master"
        }
    }

This output shows how the `clap_python` library interprets the provided command and arguments.
