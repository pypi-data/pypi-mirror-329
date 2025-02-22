import logging
import os
import re

import mutagen

from flacfixer.util import rename

logger = logging.getLogger(__name__)


class Fixer:
    def __init__(self, dry_run: bool):
        self.dry_run = dry_run

    def fix(self):
        raise NotImplementedError()


class AlbumFixer(Fixer):
    def fix(self):
        """'Fixes' directory names, ie, converts them from some
        common structures to mine.

        Example:
            (1969) Space Oddity
        becomes
            1969 - Space Oddity

        """

        directories = os.listdir()
        logger.info("Directories found: %s", directories)

        for directory in directories:
            try:
                year, title = parse_directory(directory)
            except StopIteration:
                logger.info("Not renaming file %s", directory)
                continue

            new_directory = f"{year} - {title}"
            rename(directory, new_directory, self.dry_run)


def parse_directory(directory: str) -> tuple[str, str]:
    """Takes as input a directory name and returns a tuple of
    [year,title]. If no match can be found, a StopIteration is thrown.

    """
    original_formats = iter(
        [
            # ex: "(1969) Space Oddity"
            r"\((?P<year>\d{4})\) (?P<title>.+)",
            # ex: "1974 - Natty Dread (Japan Remaster)"
            r"(?P<year>\d{4}) - (?P<title>.+)",
            # ex: "Scary Monsters… and Super Creeps (1980)"
            r"(?P<title>.+) \((?P<year>\d{4})\)",
        ]
    )
    match = None
    while match is None:
        fmt = next(original_formats)
        match = re.match(fmt, directory)

    return match.group("year"), match.group("title")


class FilenameFixer(Fixer):
    def fix(self):
        filenames = [f for f in os.listdir() if f.endswith(".flac")]
        logger.info("Renaming %s files", len(filenames))
        for filename in filenames:
            mf = mutagen.File(filename)
            extension = filename.split(".")[-1]
            new_filename = convert_filename(mf, extension)
            if new_filename == filename:
                logger.info("Not renaming %s, is already correct", filename)
                continue

            rename(filename, new_filename, self.dry_run)


def convert_filename(mf: mutagen.FileType, extension: str) -> str:
    filename = f"{mf['tracknumber'][0].rjust(2, '0')} - {mf['title'][0]}.{extension}"
    filename = remove_forbidden_characters_filename(filename)
    return filename


def remove_forbidden_characters_filename(filename: str) -> str:
    return filename.replace("/", "")
