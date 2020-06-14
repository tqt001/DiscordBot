import asyncio
import os
import unittest

from src.ExtensionManager import get_list_of_files, create_file_dict


class UtilitiesTest(unittest.TestCase):

    def test_list_of_files(self):
        expected = ['lof_test.a.a2.py', 'lof_test.a.aa.py', 'lof_test.b.b2.py', 'lof_test.b.bb.py']
        actual = asyncio.run(get_list_of_files('lof_test'))
        self.assertCountEqual(expected, actual)

    def test_get_dictionary_of_files(self):
        expected_dict = {'aa': 'lof_test.a.aa',
                         'a2': 'lof_test.a.a2',
                         'b2': 'lof_test.b.b2',
                         'bb': 'lof_test.b.bb'}
        self.assertDictEqual(expected_dict, asyncio.run(create_file_dict('lof_test')))


if __name__ == '__main__':
    unittest.main()
