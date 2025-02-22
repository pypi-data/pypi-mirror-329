#!/usr/bin/env python3
import argparse
import logging

from flacfixer.fixer import AlbumFixer, FilenameFixer
from flacfixer.recursive_executor import execute_recursively

parser = argparse.ArgumentParser(description="Fix filenames in my music dir")
action = parser.add_mutually_exclusive_group(required=True)
action.add_argument(
    "-a", "--albums", action="store_true", help="Fixes album names (directories) in PWD"
)
action.add_argument(
    "-f",
    "--filenames",
    action="store_true",
    help="Fixes filenames in PWD",
)
parser.add_argument(
    "-n",
    "--dry-run",
    action="store_true",
    help="Perform dry run and output what would be changed",
)
parser.add_argument(
    "-r",
    "--recurse-levels",
    type=int,
    default=0,
    help="Levels to recurse into. Defaults to 0, current level",
)
parser.add_argument(
    "-v",
    "--verbose",
    help="Be verbose. Pass multiple times to increase verbosity",
    action="count",
    default=0,
)


def main():
    args = parser.parse_args()
    logging.basicConfig(level=get_loglevel(args.verbose))

    fixer = AlbumFixer if args.albums else FilenameFixer
    fixer = fixer(args.dry_run)
    execute_recursively(fixer, args.recurse_levels)


def get_loglevel(verbose_count):
    default = 30
    stepsize = 10
    return default - stepsize * verbose_count


if __name__ == "__main__":
    main()
