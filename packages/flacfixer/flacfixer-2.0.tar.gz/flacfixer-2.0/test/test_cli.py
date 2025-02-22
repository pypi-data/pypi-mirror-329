import argparse
import logging
import unittest
from unittest.mock import patch

from flacfixer import cli


class TestCli(unittest.TestCase):
    required_argument = "-a"
    default_kwargs = {
        "filenames": True,
        "albums": False,
        "dry_run": False,
        "recurse_levels": 0,
    }

    def test_loglevel_defaults_warning(self):
        args = cli.parser.parse_args([self.required_argument])
        loglevel = cli.get_loglevel(args.verbose)
        self.assertEqual(loglevel, logging.WARNING)

    def test_loglevel_verbose_info(self):
        args = cli.parser.parse_args([self.required_argument, "-v"])
        loglevel = cli.get_loglevel(args.verbose)
        self.assertEqual(loglevel, logging.INFO)

    def test_loglevel_double_verbose_debug(self):
        args = cli.parser.parse_args([self.required_argument, "-vv"])
        loglevel = cli.get_loglevel(args.verbose)
        self.assertEqual(loglevel, logging.DEBUG)

    @patch("argparse.ArgumentParser.parse_args")
    def test_main_sets_loglevel(self, parse_args):
        parse_args.return_value = argparse.Namespace(verbose=1, **self.default_kwargs)
        cli.main()
        self.assertEqual(
            logging.getLogger("flacfixer").getEffectiveLevel(), logging.INFO
        )
