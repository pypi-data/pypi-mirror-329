import unittest

from tests.PatchTest import PatchTest


class EmptyPatch(PatchTest):
    def test_empty_dict(self):
        self.assertPatch([], [], [])

    def test_empty_list(self):
        self.assertPatch({}, {}, [])

    def test_dict(self):
        self.assertPatch(["foo"], ["foo"], [])

    def test_list(self):
        self.assertPatch({"foo": 1}, {"foo": 1}, [])


if __name__ == "__main__":
    unittest.main()
