#! /usr/bin/env python3

################################################################################
""" Output the top level directory of the git working tree or return
    an error if we are not in a git working tree.

    Copyright (C) 2017, 2018 John Skilleter

    Licence: GPL v3 or later
"""
################################################################################

import sys
import argparse
import os

import pygit2

################################################################################

def main():
    """ Main function """

    # Command line parameters

    parser = argparse.ArgumentParser(description='Report top-level directory of the current git working tree.')
    parser.add_argument('--parent', '-p', action='store_true',
                        help='If we are already at the top of the working tree, check if the parent directory is in a working tree and output the top-level directory of that tree.')
    parser.add_argument('--dir', '-d', action='store', default=os.getcwd(),
                        help='Find the location of the top-level directory in the working tree starting at the specified directory')
    parser.add_argument('level', nargs='?', type=int, default=0, help='Number of levels below the top-level directory to report')
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f'Unable to locate directory {args.dir}')
        sys.exit(1)

    # Try to get the current working tree

    try:
        working_tree = pygit2.Repository(args.dir).workdir
    except pygit2.GitError:
        print(f'Directory {args.dir} is not in a Git working tree')
        sys.exit(2)

    # If we are in a working tree and also looking for the parent working
    # tree, check if we are at the top of the current tree, and, if so,
    # hop up a level and try again.

    if args.parent:
        current_directory = os.getcwd()

        if os.path.samefile(working_tree, current_directory):
            os.chdir('..')
            current_directory = os.getcwd()

            try:
                working_tree = pygit2.Repository(current_directory).workdir
            except pygit2.GitError:
                print(f'Parent directory {current_directory} is not in a Git working tree')
                sys.exit(3)

    # Output the result, if we have one

    if args.level:
        start = args.dir.split('/')
        working = working_tree.split('/')

        working_tree = os.path.join(working_tree, '/'.join(start[len(working):len(working) + int(args.level)]))

    if working_tree:
        print(working_tree)

################################################################################

def git_wt():
    """Entry point"""

    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
    except BrokenPipeError:
        sys.exit(2)

################################################################################

if __name__ == '__main__':
    git_wt()
