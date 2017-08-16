import unittest
#
# zip_list2dict will merge a list and a dict in following manner:
# each list element will be converted into a dict, and then
# all those newly created dicts will be packed into a new list, which
# will be a return value of that function.
#
# when original list element is converted to a new dict,
# the key will be as specified in first argument, and a value
# would be a value of original list element.
#
# then a second argument (a static dicts) will be merged to a
# newly created dict, and combined dict will become a new list element
# of a result list.
#
# EXAMPLE: see test cases
#
def zip_list2dict(orig_list, newkey, static_dict):
    new_list = []
    for elem in orig_list:
        new_elem = { newkey: elem }
        new_elem.update(static_dict)
        new_list.append(new_elem)
    return new_list

class FilterModule(object):
    def filters(self):
        return {
            'zip_list2dict': zip_list2dict,
        }

#
# ---- Unit testing -----
#
class TestZipList2dict(unittest.TestCase):
    def setUp(self):
        self.list1 = ['a', 'b']
        self.dict1 = { 'bar': 1 }

    def test_valid(self):
        self.assertEqual(zip_list2dict(self.list1, 'foo', {}),
            [{'foo': 'a'}, {'foo': 'b'}])
        self.assertEqual(zip_list2dict(self.list1, 'foo', self.dict1),
            [
                {'foo': 'a', 'bar': 1},
                {'foo': 'b', 'bar': 1}
            ])

if __name__ == "__main__":
    unittest.main()
