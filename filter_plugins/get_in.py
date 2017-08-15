#
# This is a collection of useful/reusable functions
# available for import into any custom Ansible filters
#

import unittest

def get_in(d, path, default=None):
    init, special = d, {}
    for p in path:
        try:
            init = init.get(p, special)
        except:
            init = special
        if init is special:
            return default
    return init


class FilterModule(object):
    def filters(self):
        return {
            'get_in': get_in,
        }

#
# ---- Unit testing -----
#
class TestGetIn(unittest.TestCase):
    def setUp(self):
        self.example = { "a": { "b": { "c": 123 } } }

    def test_valid_path(self):
        self.assertEqual(
            get_in(
                self.example,
                ["a", "b"]),
            {"c": 123})

        self.assertEqual(
            get_in(
                self.example,
                ["a", "b", "c"]),
            123)

    def test_invalid_path(self):
        self.assertIsNone(
            get_in(
                self.example,
                ["x"]))

        self.assertIsNone(
            get_in(
                self.example,
                ["a", "x"]))

    def test_invalid_path_default(self):
        self.assertEqual(
            get_in(
                self.example,
                ["x"],
                "INVALID"),
            "INVALID")

    def test_nondict_path(self):
        self.assertEqual(
            get_in(
                {"a": 123},
                ["a", "b"],
                "INVALID"),
            "INVALID")


if __name__ == "__main__":
    unittest.main()
