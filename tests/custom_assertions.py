import unittest
from unittest.util import safe_repr


class CustomAssertions(unittest.TestCase):
    def assertDictInList(self, subset_dict, dict_list):
        """
        Asserts a Dict is contained in a List
        """
        assert isinstance(subset_dict, dict)
        assert isinstance(dict_list, list)

        found = False
        for element in dict_list:
            if element == subset_dict:
                found = True

        if not found:
            self.fail(f'{subset_dict} not found in superset sequence')

    def assertDictSequenceContainsDictSubset(self, subset_dict,
                                             dict_sequence):
        """
        Asserts that at least one item in dict_sequence contains subset_dict
        """
        assert isinstance(subset_dict, dict)
        assert isinstance(dict_sequence, list)
        assert all([type(item) == dict for item in dict_sequence])

        found = False
        for item in dict_sequence:
            mismatched, missing = self.compare_dict_with_subset(item,
                                                                subset_dict)
            if (not missing) and (not mismatched):
                found = True
                return

        if not found:
            self.fail('{} not found in superset sequence'.format(subset_dict))

    def assertAllSequenceItemsAreSubsetsOfResultSequenceItems(
            self, subset_sequence, result_sequence):
        """
        Asserts that each item in subset_sequence is contained in the
        corresponding item in result_sequence
        """
        assert isinstance(subset_sequence, list)
        assert isinstance(result_sequence, list)
        matched = True
        mismatches = []
        for num, item in enumerate(subset_sequence):
            if num < len(result_sequence):
                mismatched, missing = self.compare_dict_with_subset(
                    result_sequence[num], item)
                if missing or mismatched:
                    matched = False
                    mismatches.append(num)
            if len(result_sequence) == 0:
                self.fail('Result Sequence is empty')

        if not matched:
            self.fail('Items {} are mismatched with result_sequence'.format(
                mismatches))

    def assertDictContainsSubset(self, subset, dictionary, msg=None):
        """Checks whether dictionary is a superset of subset."""
        mismatched, missing = self.compare_dict_with_subset(dictionary, subset)

        if not (missing or mismatched):
            return

        standardMsg = ''
        if missing:
            standardMsg = 'Missing: %s' % ','.join(safe_repr(m) for m in
                                                   missing)
        if mismatched:
            if standardMsg:
                standardMsg += '; '
            standardMsg += 'Mismatched values: %s' % ','.join(mismatched)

        self.fail(self._formatMessage(msg, standardMsg))

    def compare_dict_with_subset(self, dictionary, subset):
        missing = []
        mismatched = []
        for key, value in subset.items():
            if key not in dictionary:
                missing.append(key)
            elif isinstance(value, dict):
                self.assertDictContainsSubset(value, dictionary[key])
            elif isinstance(value, list) and value:
                if all([type(item) == type(value[0]) for item in value]):
                    if type(value[0]) == dict:
                        self.assertAllSequenceItemsAreSubsetsOfResultSequenceItems(
                            value, dictionary[key])
                    else:
                        self.assertListEqual(value, dictionary[key])
            elif value != dictionary[key]:
                mismatched.append('%s, expected: %s, actual: %s' %
                                  (safe_repr(key), safe_repr(value),
                                   safe_repr(dictionary[key])))
        return mismatched, missing


class TestAssertDictContainsSubset(unittest.TestCase):

    def test_simple_subset(self):
        tb = CustomAssertions()
        tb.assertDictContainsSubset({'test': 'test'}, {'test': 'test'})

    def test_nested_subset(self):
        tb = CustomAssertions()
        subset = {'test_nested': {'test': 'test'}}
        superset = {'test_nested': {'test': 'test'},
                    'second_element': 'not to be compared'}
        tb.assertDictContainsSubset(subset, superset)

    def test_nested_subset_with_list(self):
        tb = CustomAssertions()
        subset = {
            'test_nested': {'test': 'test', 'list': ['item_1', 'item_2']}}
        superset = {
            'test_nested': {'test': 'test', 'list': ['item_1', 'item_2']},
            'second_element': 'not to be compared'}
        tb.assertDictContainsSubset(subset, superset)

    def test_nested_subset_with_dict_list(self):
        tb = CustomAssertions()
        subset = {'test_nested': {'test': 'test',
                                  'list': [
                                      {'item_1': 'value_1'},
                                      {'item_2': 'value_2'}
                                  ]}
                  }
        superset = {'test_nested': {'test': 'test',
                                    'list': [
                                        {'item_1': 'value_1'},
                                        {'item_2': 'value_2'}
                                    ]},
                    'second_element': 'not to be compared'}
        tb.assertDictContainsSubset(subset, superset)


class TestAssertAllSequenceItemsAreSubsetsOfResultSequenceItems(
    unittest.TestCase):
    def test_sequence_contains_subset(self):
        tb = CustomAssertions()
        subset = [{'test_nested': {'test': 'test'}}]
        superset = [{'test_nested': {'test': 'test'},
                     'second_element': 'not to be compared'}]
        tb.assertAllSequenceItemsAreSubsetsOfResultSequenceItems(subset,
                                                                 superset)

    def test_sequence_contains_not_only_subset(self):
        tb = CustomAssertions()
        subset = [{},
                  {'test_nested': {'test': 'test'}}]
        superset = [{'not exactly': {'test': 'not!'}},
                    {'test_nested': {'test': 'test'},
                     'second_element': 'not to be comapared'}]
        tb.assertAllSequenceItemsAreSubsetsOfResultSequenceItems(subset,
                                                                 superset)

    def test_sequence_contains_extra_item(self):
        tb = CustomAssertions()
        subset = [{},
                  {'test_nested': {'test': 'test'}},
                  {'extra_element': {'this element is extra': True}}]
        superset = [{'not exactly': {'test': 'not!'}},
                    {'test_nested': {'test': 'test'},
                     'second_element': 'not to be comapared'}]
        tb.assertAllSequenceItemsAreSubsetsOfResultSequenceItems(subset,
                                                                 superset)


class TestAssertSequenceDictListContainsSubset(unittest.TestCase):
    def test_subset_is_first_item(self):
        tb = CustomAssertions()
        subset = {'test_nested': {'test': 'test'}}
        superset = [{'test_nested': {'test': 'test'},
                     'not': {'to be': 'compared'}},
                    {'second_element': 'not to be compared'}]
        tb.assertDictSequenceContainsDictSubset(subset, superset)

    def test_subset_is_second_item(self):
        tb = CustomAssertions()
        subset = {'test_nested': {'test': 'test'}}
        superset = [{'first_element': 'not to be compared'},
                    {'test_nested': {'test': 'test'},
                     'not': {'to be': 'compared'}},
                    {'third_element': {'Not': 'this way'}}]
        tb.assertDictSequenceContainsDictSubset(subset, superset)

    @unittest.expectedFailure
    def test_sequence_contains_not_only_subset(self):
        tb = CustomAssertions()
        subset = {'doesnt': {'contain': 'this'}}
        superset = [{'not exactly': {'test': 'not!'}},
                    {'test_nested': {'test': 'test'}},
                    {'second_element': 'not to be compared'}]
        tb.assertDictSequenceContainsDictSubset(subset, superset)


class TestAssertDictInList(unittest.TestCase):
    def test_nested_dict_in_list(self):
        tb = CustomAssertions()
        my_dict = {'first': '1st value',
                   'nested_dict': {'nested_key': 'nested_value',
                                   'none_key': None}}
        my_list = ['test',
                   {},
                   {'first': '1st value',
                    'nested_dict': {'nested_key': 'nested_value',
                                    'none_key': None}}
                   ]
        tb.assertDictInList(my_dict, my_list)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAssertDictContainsSubset)
    suite.addTest(TestAssertAllSequenceItemsAreSubsetsOfResultSequenceItems)
    suite.addTest(TestAssertSequenceDictListContainsSubset)
    suite.addTest(TestAssertDictInList)
    return suite()


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
