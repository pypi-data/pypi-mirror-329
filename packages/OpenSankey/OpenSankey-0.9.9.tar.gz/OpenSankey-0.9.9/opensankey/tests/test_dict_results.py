"""
Auteur : Vincent LE DOZE
Date : 07/12/23
"""

# External libs ---------------------------------------------------------------
import argparse
import unittest
import os
import sys
import json
import tempfile

# Local libs ------------------------------------------------------------------
try:
    import SankeyExcelParser.io_excel_constants as io_const
except ImportError:
    sys.path.insert(0, os.getcwd())
    import SankeyExcelParser.io_excel_constants as io_const

# External modules ------------------------------------------------------------
from os import listdir
from shutil import copyfile
from parameterized import parameterized

# Local modules ---------------------------------------------------------------
from SankeyExcelParser.io_excel import load_sankey_from_excel_file
from SankeyExcelParser.sankey import Sankey
from SankeyExcelParser import su_trace as su_trace
from opensankey.server import converter


# Constants -------------------------------------------------------------------
TESTS_DIR = os.environ.get('TESTS_DIR')
XLPARSER_TESTS_REFS_DIR = 'ref_tests__SankeyExcelParser'
SCMFA_TESTS_REFS_DIR = 'ref_tests__SCMFA'
OPENSANKEY_TESTS_REFS_DIR = 'ref_tests__OpenSankey'
MFASANKEY_TESTS_REFS_DIR = 'ref_tests__MFASankey'

DIRS_TO_EXCLUDE = [
    'mfadata',
    'sankeylayout',
    '.git',
    '.md',
    'Archive',
    'Archives',
    'OpenSankey',
    'OptimSankey',
    'not_tested',
    'artefacts',
    'Formations',
    'Recherche',
    'Etudes',
    XLPARSER_TESTS_REFS_DIR,
    SCMFA_TESTS_REFS_DIR,
    OPENSANKEY_TESTS_REFS_DIR,
    MFASANKEY_TESTS_REFS_DIR
]

MAXSIZE = 1000000000000000000
TESTS_TO_SKIP = [
    'Tests_update_ter_mettre_a_jour_ter_reconciled_sankey',
    'Fili_res_Agricole_Vin_Vin_AURA_reconciled_sankey',
    'Fili_res_Agricole_Vin_Vin_Occitanie_reconciled_sankey'
]

REF_FILE_PREFIX = 'expected_'
REF_FILE_SUFFIX = ' sankey'

EXPECTED_RESULTS = {}
TEST_PARAMETERS = []


# Functions -------------------------------------------------------------------
def keep_exploring_file_or_folder(file_or_folder):
    # Exclude certains files or folders
    for _ in DIRS_TO_EXCLUDE:
        if _ in file_or_folder:
            return False
    return True

def parse_folder(current_dir):
    folder_content = listdir(current_dir)
    for file_or_folder in folder_content:
        # Folder exclusion conditions
        if not keep_exploring_file_or_folder(file_or_folder):
            continue
        # We found a file
        if os.path.isfile(os.path.join(current_dir, file_or_folder)):
            # It it something like <file>.xlsx ?
            if ('xlsx' in file_or_folder) and \
               ('old' not in file_or_folder) and \
               ('new' not in file_or_folder):
                # If file is too large, don't test
                file_stats = os.stat(os.path.join(current_dir, file_or_folder))
                if file_stats.st_size > MAXSIZE:
                    continue
                # Get file name
                file_relpath = os.path.relpath(
                    os.path.join(current_dir, file_or_folder),
                    TESTS_DIR)
                test_name = os.path.splitext(file_relpath)[0]
                test_dir, test_subname = os.path.split(test_name)
                # Update expected results
                if test_name not in EXPECTED_RESULTS:
                    EXPECTED_RESULTS[test_name] = {}
                # Create results output dir
                test_refs_dir = os.path.join(current_dir, OPENSANKEY_TESTS_REFS_DIR)
                if OPENSANKEY_TESTS_REFS_DIR not in listdir(current_dir):
                    os.mkdir(test_refs_dir)
                # Get related results
                test_ref_file_path = os.path.join(
                    test_refs_dir,
                    REF_FILE_PREFIX + test_subname + REF_FILE_SUFFIX + '.json')
                if os.path.isfile(test_ref_file_path):
                    with open(test_ref_file_path, "r") as test_ref_file:
                        test_ref = json.load(test_ref_file)
                        EXPECTED_RESULTS[test_name] = test_ref
                # Finish updating test
                TEST_PARAMETERS.append((
                    test_name,
                    file_relpath,
                    EXPECTED_RESULTS[test_name]))
            continue
        # Recursivly parse sub-directories
        parse_folder(os.path.join(current_dir, file_or_folder))


# Fill constants values
parse_folder(TESTS_DIR)


# Class -----------------------------------------------------------------------
class DictResultTest(unittest.TestCase):
    generate_results = False

    @classmethod
    def set_generate_results(cls):
        cls.generate_results = True
        cls.new_results = {}

    def check_dict(self, to_test, ref):
        """
        Recursivly compare 2 dicts

        Parameters
        ----------
        :param to_test: Dict to test
        :type to_test: dict

        :param ref: Dict to check with
        :type ref: dict
        """
        if ref is None:
            return
        for key in ref:
            if type(to_test[key]) is dict:
                self.check_dict(to_test[key], ref[key])
            else:
                try:
                    self.assertEqual(to_test[key], ref[key])
                except Exception:
                    self.assertEqual(to_test, ref)

    @parameterized.expand(TEST_PARAMETERS)
    def test_results_dict(
        self,
        test_name: str,
        file_name: str,
        expected_results: dict
    ):
        """
        Test Excel -> Json conversion

        Parameters
        ----------
        :param test_name: Name of current test
        :type test_name: str

        :param file_name: Current excel file that is tested
        :type file_name: str

        :param expected_results: Dict of expected results to check with
        :type expected_results: dict
        """
        # For Debug
        print('\n{}'.format(self._testMethodName), end=' -> ', flush=True)
        # TODO : redondant ?
        if len( [test_to_skip for test_to_skip in TESTS_TO_SKIP if test_to_skip in self._testMethodName]) > 0:
            return
        # Read sankey struct
        sankey = Sankey()
        load_sankey_from_excel_file(
            os.path.join(TESTS_DIR, file_name),
            sankey)
        # Convert in json format
        sankey_json = converter.extract_json_from_sankey(sankey)
        if not self.generate_results:
            self.check_dict(sankey_json, expected_results)
        else:
            self.new_results[test_name] = sankey_json

    @classmethod
    def tearDownClass(cls):
        """
        Method that write result to given result files.
        """
        if cls.generate_results:
            for test_name in cls.new_results:
                # Construct path
                test_ref = json.dumps(cls.new_results[test_name], indent=2)
                test_dir, test_subname = os.path.split(test_name)
                test_ref_dir = os.path.join(
                    TESTS_DIR,
                    test_dir,
                    OPENSANKEY_TESTS_REFS_DIR)
                # Write file
                test_ref_file_path = os.path.join(
                    test_ref_dir,
                    REF_FILE_PREFIX + test_subname + REF_FILE_SUFFIX + '.json')
                with open(test_ref_file_path, "w") as test_ref_file:
                    test_ref_file.write(test_ref)


# Main ------------------------------------------------------------------------
if __name__ == '__main__':
    # Get args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--generate_results",
        action='store_true',
        required=False,
        help="Option to regenerate tests results")
    parser.add_argument(
        'filenames',
        metavar='F',
        type=str,
        nargs='*',
        help='Specific files to test')
    args = parser.parse_args()
    # Generate test if needed
    if args.generate_results:
        DictResultTest.set_generate_results()
    # Get tests names to run
    if len(args.filenames) == 0:
        loader = unittest.TestLoader()
        names = loader.getTestCaseNames(DictResultTest)
    else:
        names = args.filenames
    # Append tests to test suite
    suite = unittest.TestSuite()
    for name in names:
        try:
            if len([test_to_skip for test_to_skip in TESTS_TO_SKIP if test_to_skip in name]) > 0:
                continue
            suite.addTest(DictResultTest(name))
        except Exception:
            print("Error when adding {} to test base".format(name))
    # Run tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
