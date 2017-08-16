import unittest

#
# zip_lists will merge two lists: element-by-element
# if one list is shorter than the other, if will re-use last
# available element from shorter list and repeat it for all
# subsequent element-by-element merges
#
# It makes merging a constant values to dynamic values very easy!
#
def zip_lists(list1, list2):
    len1 = len(list1)
    len2 = len(list2)
    if (len1 == 0) or (len2 == 0):
        return []

    newlist = []
    idx1 = 0
    idx2 = 0
    max_len = max([len1, len2])

    for i in range(max_len):
        elem1 = list1[idx1]
        elem2 = list2[idx2]
        newlist.append(str(elem1) + str(elem2))
        if idx1 < (len1-1):
            idx1 += 1
        if idx2 < (len2-1):
            idx2 += 1

    return newlist

class FilterModule(object):
    def filters(self):
        return {
            'zip_lists': zip_lists,
        }

#
# ---- Unit testing -----
#
class TestGetIn(unittest.TestCase):
    def setUp(self):
        self.l1 = [1, 2, 3]
        self.l2 = ['a']
        self.l3 = ['a', 'b', 'c']

        self.res1 = ['1a', '2a', '3a']
        self.res2 = ['a1', 'a2', 'a3']
        self.res3 = ['a1', 'b2', 'c3']

    def test_valid_path(self):
        self.assertEqual(zip_lists(self.l1, self.l2),
            self.res1)
        self.assertEqual(zip_lists(self.l2, self.l1),
            self.res2)
        self.assertEqual(zip_lists(self.l3, self.l1),
            self.res3)

    def test_invalid_path_default(self):
        self.assertEqual(zip_lists(self.l1, []), [])
        self.assertEqual(zip_lists([], self.l1), [])

if __name__ == "__main__":
    unittest.main()
