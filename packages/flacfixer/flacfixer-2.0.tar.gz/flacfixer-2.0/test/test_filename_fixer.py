import unittest
from unittest.mock import patch

from flacfixer.fixer import FilenameFixer


def correct_filename(tracknumber: str, title: str) -> str:
    tracknumber_just = tracknumber.rjust(2, "0")
    filename = f"{tracknumber_just} - {title}.flac"
    filename = remove_forbidden_characters_filename(filename)
    return filename


def remove_forbidden_characters_filename(filename):
    return filename.replace("/", "")


@patch("mutagen.File")
@patch("flacfixer.fixer.rename")
@patch("os.listdir")
class TestFilenameFixer(unittest.TestCase):
    def setUp(self):
        self.fixer = FilenameFixer(False)
        # test_data is a list with tuples: (current filename, tracknumber, title)
        self.test_data = [
            ("01. Terrible Love.flac", "1", "Terrible Love"),
            ("2 - Sorrow.flac", "2", "Sorrow"),
            ("Anyone's Ghost.flac", "3", "Anyone's Ghost"),
            ("04 - little faith.flac", "4", "Little Faith"),
        ]

    def test_calls_rename_on_incorrect_filenames(self, listdir, rename, mutagen_file):
        listdir.return_value = [row[0] for row in self.test_data]
        mutagen_file.side_effect = [
            {"tracknumber": [row[1]], "title": [row[2]]} for row in self.test_data
        ]
        self.fixer.fix()
        for row in self.test_data:
            rename.assert_any_call(row[0], correct_filename(row[1], row[2]), False)
        self.assertEqual(len(self.test_data), rename.call_count)

    def test_doesnt_call_rename_correct_filenames(self, listdir, rename, mutagen_file):
        local_test_data = self.test_data.copy()
        corrected_item = local_test_data[2]
        local_test_data[2] = (
            correct_filename(corrected_item[1], corrected_item[2]),
            corrected_item[1],
            corrected_item[2],
        )
        listdir.return_value = [row[0] for row in local_test_data]
        mutagen_file.side_effect = [
            {"tracknumber": [row[1]], "title": [row[2]]} for row in local_test_data
        ]
        self.fixer.fix()
        self.assertEqual(len(self.test_data) - 1, rename.call_count)

    def test_passes_dry_run_to_rename(self, listdir, rename, mutagen_file):
        dry_run = True
        self.fixer = FilenameFixer(dry_run)
        listdir.return_value = [row[0] for row in self.test_data]
        self.fixer.fix()
        rename.assert_any_call(unittest.mock.ANY, unittest.mock.ANY, dry_run)

    def test_removes_forbidden_characters(self, listdir, rename, mutagen_file):
        track = (
            "13 - Leaving Nara ; Lovely Day.flac",
            "13",
            "Leaving Nara / Lovely Day",
        )
        listdir.return_value = [track[0]]
        mutagen_file.return_value = {"tracknumber": [track[1]], "title": [track[2]]}

        self.fixer.fix()

        correct = correct_filename(track[1], track[2])
        self.assertFalse("/" in correct, "Cannot have '/' in filename")
        rename.assert_called_with(track[0], correct, False)


if __name__ == "__main__":
    unittest.main()
