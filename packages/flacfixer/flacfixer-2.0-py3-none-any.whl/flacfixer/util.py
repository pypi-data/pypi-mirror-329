import logging
import os


def rename(old: str, new: str, dry_run: bool = False):
    if dry_run:
        print(f'Dry run, would rename "{old}" to "{new}"')
        return

    logging.getLogger(__name__).info('Renaming "%s" to "%s"', old, new)
    os.rename(old, new)
