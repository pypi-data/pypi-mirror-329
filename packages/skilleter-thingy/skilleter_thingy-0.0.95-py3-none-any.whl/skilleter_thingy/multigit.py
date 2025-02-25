#!/usr/bin/env python3

"""mg - MultiGit - utility for managing multiple Git repos in a hierarchical directory tree"""

import os
import sys
import fnmatch
import configparser

from dataclasses import dataclass, field

import thingy.git2 as git
import thingy.colour as colour

################################################################################

# DONE: / Output name of each git repo as it is processed as command sits there seeming to do nothing otherwise.
# DONE: Better error-handling - e.g. continue/abort option after failure in one repo
# DONE: Don't save the configuration on exit if it hasn't changed
# DONE: Don't use a fixed list of default branch names
# DONE: If the config file isn't in the current directory then search up the directory tree for it but run in the current directory
# DONE: Use the configuration file
# DONE: init function
# NOPE: Dry-run option - just pass the option to the Git command
# NOPE: Is it going to be a problem if the same repo is checked out twice or more in the same workspace - user problem
# NOPE: Pull/fetch - only output after running command and only if something updated
# NOPE: Switch to tomlkit
# TODO: -j option to run in parallel - yes, but it will only work with non-interactive Git commands
# TODO: Command that takes partial repo name and either returns full path or pops up window to autocomplete until single match found
# TODO: Consistent colours in output
# TODO: If run in a subdirectory, only process repos in that tree (or have an option to do so)
# TODO: Verbose option
# TODO: When specifying list of repos, if repo name doesn't contain '/' prefix it with '*'?
# TODO: select_git_repos() and +dir should use consist way of selecting repos if possible
################################################################################

DEFAULT_CONFIG_FILE = 'multigit.toml'

# If a branch name is specified as 'DEFAULT' then the default branch for the
# repo is used instead.

DEFAULT_BRANCH = 'DEFAULT'

################################################################################

HELP_INFO = """usage: multigit [-h] [--dryrun] [--debug] [--verbose] [--quiet] [--config CONFIG] [--directory DIRECTORY] [--repos REPOS] [--modified] [--branched]
                {+init, +config, +dir, GIT_COMMAND} ...

Run git commands in multiple Git repos. DISCLAIMER: This is beta-quality software, with missing features and liable to fail with a stack trace, but shouldn't eat your data

options:
  -h, --help            show this help message and exit
  --dryrun, --dry-run, -D
                        Dry-run comands
  --debug, -d           Debug
  --verbose, -v         Verbosity to the maximum
  --quiet, -q           Minimal console output
  --config CONFIG, -c CONFIG
                        The configuration file (defaults to multigit.toml)
  --directory DIRECTORY, --dir DIRECTORY
                        The top-level directory of the multigit tree (defaults to the current directory)
  --repos REPOS, -r REPOS
                        The repo names to work on (defaults to all repos and can contain shell wildcards and can be issued multiple times on the command line)
  --modified, -m        Select repos that have local modifications
  --branched, -b        Select repos that do not have the default branch checked out
  --continue, -C        Continue if a git command returns an error (by default, executation terminates when a command fails)

Sub-commands:
  {+init,+dir,+config,GIT_COMMAND}
    +init                Build or update the configuration file using the current branch in each repo as the default branch
    +config              Return the name and location of the configuration file
    +dir                 Return the location of a working tree, given the repo name, or if no parameter specified, the root directory of the multigit tree
    GIT_COMMAND          Any git command, including options and parameters - this is then run in all specified working trees

"""

################################################################################

@dataclass
class Arguments():
    """Data class to contain command line options and parameters"""

    dryrun: bool = False
    debug: bool = False
    quiet: bool = False
    verbose: bool = False
    configuration_file: str = DEFAULT_CONFIG_FILE
    directory: str = '.'
    repos: list[str] = field(default_factory=list)
    modified: bool = False
    branched: bool = False
    command: str = None
    error_continue: bool = False
    parameters: list[str] = field(default_factory=list)
    internal_command: bool = False

################################################################################

def error(msg, status=1):
    """Quit with an error"""

    colour.write(f'[RED:ERROR:] {msg}\n', stream=sys.stderr)
    sys.exit(status)

################################################################################

def find_configuration(args):
    """If the configuration file name has path elements, try and read it, otherwise
       search up the directory tree looking for the configuration file.
       Returns configuration file path or None if the configuration file
       could not be found."""

    if '/' in args.configuration_file:
        config_file = args.configuration_file
    else:
        config_path = os.getcwd()
        config_file = os.path.join(config_path, args.configuration_file)

        while not os.path.isfile(config_file) and config_path != '/':
            config_path = os.path.dirname(config_path)
            config_file = os.path.join(config_path, args.configuration_file)

    return config_file if os.path.isfile(config_file) else None

################################################################################

def show_progress(width, msg):
    """Show a single line progress message"""

    name = msg[:width-1]

    colour.write(f'{name}', newline=False)

    if len(name) < width-1:
        colour.write(' '*(width-len(name)), newline=False)

    colour.write('\r', newline=False)

################################################################################

def find_git_repos(args):
    """Locate and return a list of '.git' directory parent directories in the
       specified path.

       If wildcard is not None then it is treated as a list of wildcards and
       only repos matching at least one of the wildcards are returned.

       If the same repo matches multiple times it will only be returned once. """

    repos = set()

    for root, dirs, _ in os.walk(os.path.dirname(args.configuration_file)):
        if '.git' in dirs:
            if root.startswith('./'):
                root = root[2:]

            if args.repos:
                for card in args.repos:
                    if fnmatch.fnmatch(root, card):
                        if root not in repos:
                            yield root
                            repos.add(root)
                        break
            else:
                if root not in repos:
                    yield root
                    repos.add(root)

################################################################################

def select_git_repos(args, config):
    """Return git repos from the configuration that match the criteria on the
       multigit command line (the --repos, --modified and --branched options)
       or, return them all if no relevant options specified"""

    for repo in config.sections():
        # If repos are specified, then only match according to wildcards, full
        # path or just basename.

        if args.repos:
            for entry in args.repos:
                if '?' in entry or '*' in entry:
                    if fnmatch.fnmatch(repo, entry):
                        matching = True
                        break
                elif '/' in entry:
                    if repo == entry:
                        matching = True
                        break
                elif os.path.basename(repo) == entry:
                    matching = True
                    break

            else:
                matching = False
        else:
            matching = True

        # If branched specified, only match if the repo is matched _and_ branched

        if matching and args.branched:
            if git.branch(path=repo) == config[repo]['default branch']:
                matching = False

        # If modified specified, only match if the repo is matched _and_ modified

        if matching and args.modified:
            if not git.status(path=repo):
                matching = False

        if matching:
            yield config[repo]

################################################################################

def branch_name(name, default_branch):
    """If name is None or DEFAULT_BRANCH return default_branch, otherwise return name"""

    return default_branch if not name or name == DEFAULT_BRANCH else name

################################################################################

def mg_init(args, config, console):
    """Create or update the configuration
       By default, it scans the tree for git directories and adds or updates them
       in the configuration, using the current branch as the default branch. """

    # Sanity checks

    if args.modified or args.branched:
        error('The "--modified" and "--branched" options cannot be used with the "init" subcommand')
    elif not config:
        error(f'Unable to location configuration file "{args.configuration_file}"')

    # TODO: Update should remove or warn about repos that are no longer present

    # Search for .git directories

    for repo in find_git_repos(args):
        if not args.quiet:
            show_progress(console.columns, repo.name)

        if repo not in config:
            config[repo] = {
                'default branch': git.branch(path=repo)
            }

        remote = git.remotes(path=repo)

        if 'origin' in remote:
            config[repo]['origin'] = remote['origin']
            config[repo]['repo name']= os.path.basename(remote['origin']).removesuffix('.git')
        else:
            config[repo]['repo name'] = os.path.basename(repo)

################################################################################

def mg_dir(args, config, console):
    """Return the location of a working tree, given the name, or the root directory
       of the tree if not
       Returns an error unless there is a unique match"""

    # DONE: Should return location relative to the current directory or as absolute path

    _ = console
    _ = config

    if len(args.parameters) > 1:
        error('The +dir command takes no more than one parameter - the name of the working tree to search for')
    elif args.parameters:
        location = []
        wild_prefix_location = []
        wild_location = []

        search_name = args.parameters[0]

        # Search for exact matches, matches if prefixed by '*' or prefixed and suffixed with '*'
        # unless it already contains '*'

        for repo in select_git_repos(args, config):
            if fnmatch.fnmatch(repo['repo name'], search_name):
                location.append(repo.name)

            elif '*' not in search_name:
                if fnmatch.fnmatch(repo['repo name'], f'*{search_name}'):
                    wild_prefix_location.append(repo.name)

                elif fnmatch.fnmatch(repo['repo name'], f'*{search_name}*'):
                    wild_location.append(repo.name)

        destination = None
        for destinations in (location, wild_prefix_location, wild_location):
            if len(destinations) == 1:
                destination = destinations
                break
            elif len(destinations) > 1:
                destination = destinations

        if not destination:
            error(f'No matches with [BLUE:{search_name}]')

        if len(destination) > 1:
            error(f'Multiple matches with [BLUE:{search_name}] - {" ".join(destination)}')

        colour.write(os.path.join(os.path.dirname(args.configuration_file), destination[0]))
    else:
        colour.write(os.path.dirname(args.configuration_file))

################################################################################

def mg_config(args, config, console):
    """Output the path to the configuration file"""

    _ = config
    _ = console

    if len(args.parameters):
        error('The +config command does not take parameters')

    colour.write(args.configuration_file)

################################################################################

def run_git_command(args, config, console):
    """Run a command in each of the working trees, optionally continuing if
       there's an error"""

    _ = config
    _ = console

    for repo in select_git_repos(args, config):
        repo_command = [args.command]
        for cmd in args.parameters:
            repo_command.append(branch_name(cmd, repo['default branch']))

        colour.write(f'\n[BOLD:{repo.name}]\n')

        _, status = git.git_run_status(repo_command, path=repo.name, redirect=False)

        if status and not args.error_continue:
            sys.exit(status)

################################################################################

def parse_command_line():
    """Manually parse the command line as we want to be able to accept 'multigit <OPTIONS> <+MULTIGITCOMMAND | ANY_GIT_COMMAND_WITH_OPTIONS>
       and I can't see a way to get ArgumentParser to accept arbitrary command+options"""

    args = Arguments()

    # Expand arguments so that, for instance '-dv' is parsed as '-d -v'

    argv = []

    for arg in sys.argv:
        if arg[0] != '-' or arg.startswith('--'):
            argv.append(arg)
        else:
            for c in arg[1:]:
                argv.append('-' + c)

    # Currently doesn't handle single letter options in concatenated form - e.g. -dv

    i = 1
    while i < len(argv):
        param = argv[i]

        if param in ('--dryrun', '--dry-run', '-D'):
            args.dryrun = True

        elif param in ('--debug', '-d'):
            args.debug = True

        elif param in ('--verbose', '-v'):
            args.verbose = True

        elif param in ('--quiet', '-q'):
            args.quiet = True

        elif param in ('--config', '-c'):
            try:
                i += 1
                args.configuration_file = argv[i]
            except IndexError:
                error('--config - missing configuration file parameter')

        elif param in ('--repos', '-r'):
            try:
                i += 1
                args.repos.append(argv[i])
            except IndexError:
                error('--repos - missing repo parameter')

        elif param in ('--modified', '-m'):
            args.modified = True

        elif param in ('--branched', '-b'):
            args.branched = True

        elif param in ('--continue', '-C'):
            args.error_continue = True

        elif param in ('--help', '-h'):
            print(HELP_INFO)
            sys.exit(0)

        elif param[0] == '-':
            error(f'Invalid option: "{param}"')
        else:
            break

        i += 1

    # After the options, we either have a multigit command (prefixed with '+') or a git command
    # followed by parameter

    try:
        if argv[i][0] == '+':
            args.command = argv[i][1:]
            args.internal_command = True
        else:
            args.command = argv[i]
            args.internal_command = False

    except IndexError:
        error('Missing command')

    args.parameters = argv[i+1:]

    args.configuration_file = find_configuration(args)

    return args

################################################################################

def main():
    """Main function"""

    commands = {
       'init': mg_init,
       'dir': mg_dir,
       'config': mg_config,
    }

    args = parse_command_line()

    if args.internal_command and args.command not in commands:
        error(f'Invalid command "{args.command}"')

    # If the configuration file exists, read it

    config = configparser.ConfigParser()

    if not (args.internal_command and args.command == 'init'):
        if not args.configuration_file:
            error('Cannot locate configuration file')
        elif not os.path.isfile(args.configuration_file):
            error(f'Cannot read configuration file {args.configuration_file}')

    if os.path.isfile(args.configuration_file):
        config.read(args.configuration_file)
        os.chdir(os.path.dirname(args.configuration_file))

    # Get the console size

    try:
        console = os.get_terminal_size()
    except OSError:
        console = None
        args.quiet = True

    # Run an internal or external command-specific validation

    if args.internal_command:
        # Run the subcommand

        commands[args.command](args, config, console)

        # Save the updated configuration file if it has changed (currently, only the init command will do this).

        if config and args.command == 'init':
            with open(args.configuration_file, 'w', encoding='utf8') as configfile:
                config.write(configfile)

    else:
        # Run the external command, no need to update the config as it can't change here

        run_git_command(args, config, console)

################################################################################

def multigit():
    """Entry point"""

    try:
        main()

    # Catch keyboard aborts

    except KeyboardInterrupt:
        sys.exit(1)

    # Quietly fail if output was being piped and the pipe broke

    except BrokenPipeError:
        sys.exit(2)

    # Catch-all failure for Git errors

    except git.GitError as exc:
        sys.stderr.write(exc.msg)
        sys.exit(exc.status)

################################################################################

if __name__ == '__main__':
    multigit()
