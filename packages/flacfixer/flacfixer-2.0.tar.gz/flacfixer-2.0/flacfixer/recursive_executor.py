import logging
import os

from flacfixer.fixer import Fixer

logger = logging.getLogger(__name__)


def execute_recursively(fixer: Fixer, recurse_levels: int, current_level: int = 0):
    if current_level <= recurse_levels:
        logger.debug("Currently at level %s", current_level)
        fixer.fix()
        directories = [f for f in os.scandir() if f.is_dir()]
        current_level += 1
        for d in directories:
            logger.debug("Moving into directory %s", d)
            os.chdir(d)
            execute_recursively(fixer, recurse_levels, current_level)
            logger.debug("Finished directory %s, moving back up", d)
            os.chdir("..")
