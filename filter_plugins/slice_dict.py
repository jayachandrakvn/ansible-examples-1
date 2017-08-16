import unittest

def slice_dict(dataset, attrs, default=None):
    dataset_attrs = dataset.keys()
    common_attrs = list(set(attrs) & set(dataset_attrs))
    if default == None:
        return { attr: dataset.get(attr) for attr in common_attrs }
    else:
        return { attr: dataset.get(attr, default) for attr in attrs }

class FilterModule(object):
    def filters(self):
        return {
            'slice_dict': slice_dict,
        }

#
# ---- Unit testing -----
#
class TestGetIn(unittest.TestCase):
    def setUp(self):
        self.example = { "a": 1, "b": 2, "c": 3 }

    def test_valid_path(self):
        self.assertEqual(
            slice_dict(
                self.example,
                ["a", "b"]),
            { "a": 1, "b": 2})

        self.assertEqual(
            slice_dict(
                self.example,
                ["a", "b", "d"]),
            { "a": 1, "b": 2 })

    def test_invalid_path_default(self):
        self.assertEqual(
            slice_dict(
                self.example,
                ["x"],
                "INVALID"),
            { "x": "INVALID"})

if __name__ == "__main__":
    unittest.main()
