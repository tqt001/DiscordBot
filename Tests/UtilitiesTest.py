import asyncio
import os
import unittest


async def create_file_dict(directory):
    """Creates a dict with all the files available in the directory.
    Sets the file name as the key and its path using '.' as a delimiter instead of '/'
    """
    file_paths = await get_list_of_files(directory)
    file_dict = {}
    for file_path in file_paths:
        value = file_path.replace('.py', '')
        key = value[value.rindex('.') + 1:]
        file_dict[key] = value
    return file_dict


async def get_list_of_files(directory):
    all_files = []

    def helper(path_dir, ext_path):
        for p in os.listdir(path_dir):
            path = os.path.join(path_dir, p)
            new_ext_path = ext_path + '.' + p
            if os.path.isdir(path):
                helper(path, new_ext_path)
            else:
                all_files.append(new_ext_path)
    helper(directory, directory)
    return all_files


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
