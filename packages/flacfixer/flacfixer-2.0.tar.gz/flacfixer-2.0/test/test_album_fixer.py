import unittest
from unittest.mock import patch

from flacfixer.fixer import AlbumFixer, parse_directory

# original_fmt: new_format
album_formats = {
    "(1969) Space Oddity": "1969 - Space Oddity",
    "2001 - Lateralus": "2001 - Lateralus",
    "Trouble Will Find Me (2013)": "2013 - Trouble Will Find Me",
}


@patch("flacfixer.fixer.rename")
@patch("os.listdir")
class TestAlbumFixer(unittest.TestCase):
    def setUp(self):
        self.fixer = AlbumFixer(False)

    def test_calls_rename_on_known_directory_fmts(self, listdir, rename):
        listdir.return_value = album_formats.keys()
        self.fixer.fix()
        for d in album_formats.keys():
            rename.assert_any_call(d, album_formats[d], False)
        self.assertEqual(len(album_formats), rename.call_count)

    def test_doesnt_call_rename_on_unknown_fmts(self, listdir, rename):
        formats_with_unknown = album_formats.copy()
        formats_with_unknown["unknown"] = "unknown format"
        listdir.return_value = formats_with_unknown.keys()
        self.fixer.fix()
        self.assertEqual(len(album_formats) + 1, len(formats_with_unknown))
        self.assertEqual(len(album_formats), rename.call_count)

    def test_passes_dry_run_to_rename(self, listdir, rename):
        dry_run = True
        self.fixer = AlbumFixer(dry_run)
        listdir.return_value = album_formats.keys()
        self.fixer.fix()
        rename.assert_any_call(unittest.mock.ANY, unittest.mock.ANY, dry_run)


class TestParseDirectory(unittest.TestCase):
    def test_parse_directory_fmt1(self):
        d = "(1969) Space Oddity"
        year, title = parse_directory(d)
        self.assertEqual("1969", year)
        self.assertEqual("Space Oddity", title)

    def test_parse_directory_fmt2(self):
        d = "1974 - Natty Dread (Japan Remaster)"
        year, title = parse_directory(d)
        self.assertEqual("1974", year)
        self.assertEqual("Natty Dread (Japan Remaster)", title)

    def test_parse_directory_fmt3(self):
        d = "Scary Monsters… and Super Creeps (1980)"
        year, title = parse_directory(d)
        self.assertEqual("1980", year)
        self.assertEqual("Scary Monsters… and Super Creeps", title)

    def test_parse_directory_unknown_format(self):
        d = "random"
        with self.assertRaises(StopIteration):
            parse_directory(d)


if __name__ == "__main__":
    unittest.main()
