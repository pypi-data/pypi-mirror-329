"""
Auteur : Vincent LE DOZE
Date : 07/12/23
"""

# External libs ---------------------------------------------------------------
import unittest
import os
import json
import tempfile

# External modules ------------------------------------------------------------
from os import listdir
from shutil import copyfile

# Local modules ---------------------------------------------------------------
from SankeyExcelParser.io_excel import load_sankey_from_excel_file
from SankeyExcelParser.sankey import Sankey
from SankeyExcelParser import su_trace as su_trace

# Constants -------------------------------------------------------------------
TESTS_DIR = os.environ.get('TESTS_DIR')
XLPARSER_TESTS_REFS_DIR = 'ref_tests__SankeyExcelParser'
SCMFA_TESTS_REFS_DIR = 'ref_tests__SCMFA'
OPENSANKEY_TESTS_REFS_DIR = 'ref_tests__OpenSankey'
MFASANKEY_TESTS_REFS_DIR = 'ref_tests__MFASankey'

DIRS_TO_EXCLUDE = [
    '.git',
    '.md',
    XLPARSER_TESTS_REFS_DIR,
    SCMFA_TESTS_REFS_DIR,
    OPENSANKEY_TESTS_REFS_DIR,
    MFASANKEY_TESTS_REFS_DIR
]

MAXSIZE = 200000

REF_TEST_PREFIX = 'expected_'
REF_SANKEY_SUFFIX = '_sankey-dict'
REF_LOG_SUFFIX = '_parsing_logs'

EXPECTED_RESULTS = {}
EXPECTED_RESULTS[os.path.relpath('Tests/create_empty_ter/pommes_poires') + ' create empty ter'] = None
EXPECTED_RESULTS[os.path.relpath('Tests/create_empty_ter/simplified_example_fr') + ' create empty ter'] = None
EXPECTED_RESULTS[os.path.relpath('Projets/AlimentationAnimale/orge check input')] = None

LOGS_KEY = 'Logs'
SANKEY_KEY = 'Sankey'

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
        # Does test file exists ?
        if os.path.isfile(os.path.join(current_dir, file_or_folder)):
            # It it something like <file>.xlsx ?
            if ('xlsx' in file_or_folder) and \
               ('reconciled' not in file_or_folder) and \
               ('converted' not in file_or_folder) and \
               ('old' not in file_or_folder) and \
               ('solution' not in file_or_folder):
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
                test_refs_dir = os.path.join(current_dir, XLPARSER_TESTS_REFS_DIR)
                if XLPARSER_TESTS_REFS_DIR not in listdir(current_dir):
                    os.mkdir(test_refs_dir)
                # Get related logs
                test_ref_log_path = os.path.join(
                    test_refs_dir,
                    REF_TEST_PREFIX + test_subname + REF_LOG_SUFFIX + '.json')
                EXPECTED_RESULTS[test_name][LOGS_KEY] = {}
                if os.path.isfile(test_ref_log_path):
                    with open(test_ref_log_path, "r") as test_ref_log_file:
                        test_ref_log = json.load(test_ref_log_file)
                        EXPECTED_RESULTS[test_name][LOGS_KEY] = test_ref_log
                # Get related sankey as dict expected result
                test_ref_sankey_path = os.path.join(
                    test_refs_dir,
                    REF_TEST_PREFIX + test_subname + REF_SANKEY_SUFFIX + '.json')
                EXPECTED_RESULTS[test_name][SANKEY_KEY] = {}
                if os.path.isfile(test_ref_sankey_path):
                    with open(test_ref_sankey_path, "r") as test_ref_sankey_file:
                        test_ref_sankey = json.load(test_ref_sankey_file)
                        EXPECTED_RESULTS[test_name][SANKEY_KEY] = test_ref_sankey
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
class MFAProblemsTests(unittest.TestCase):
    generate_results = False

    @classmethod
    def set_generate_results(cls):
        cls.generate_results = True
        cls.new_results = {}

    def prepare_test(
        self,
        file_name: str,
        use_reconciled: bool = False
    ):
        """
        Read and check input excel file to use for tests.

        Parameters
        ----------
        :param file_name: Input excel file to read
        :type file_name: str

        Optional parameters
        -------------------
        :param use_reconciled: Use reconciled version of given file
        :type use_reconciled: bool, optional (defaults to False)

        Returns
        -------
        :return: sankey, sheet_to_remove_names, excel_filepath, tmp_dir
        :rtype: tuple as (Sankey, list, str, str)
        """
        # Make temp directory
        tmp_dir = tempfile.mkdtemp()
        # Init log file
        logname = tmp_dir + os.path.sep + "rollover.log"
        su_trace.logger_init(logname, "w")
        # Get path of file to test
        tests_dir = os.environ.get('TESTS_DIR')
        excel_filepath = os.path.join(tests_dir, file_name)
        # Get reconcilied version of file to test
        excel_rec_filename = os.path.splitext(file_name)[0]+'_reconciled.xlsx'
        excel_rec_filepath = os.path.join(tests_dir, excel_rec_filename)
        # Can we test reconciled file ?
        if os.path.isfile(excel_rec_filepath):
            file_stats = os.stat(excel_rec_filepath)
            if file_stats.st_size > MAXSIZE:
                use_reconciled = False
        # Read files
        sheet_to_remove_names = []
        sankey = Sankey()
        if use_reconciled and os.path.isfile(excel_rec_filepath):
            excel_rectmp_filepath = os.path.join(tmp_dir, os.path.basename(excel_rec_filename))
            excel_filepath = excel_rec_filepath
            copyfile(excel_rec_filepath, excel_rectmp_filepath)
            ok, msg = load_sankey_from_excel_file(
                excel_rectmp_filepath,
                sankey,
                sheet_to_remove_names)
            if not ok:
                su_trace.logger.error(msg)
                return (sankey, sheet_to_remove_names, excel_filepath, tmp_dir)
            # Remove results if needed
            if sankey.has_at_least_one_result():
                sankey.reset_all_results()
        else:
            sankey = Sankey()
            ok, msg = load_sankey_from_excel_file(
                excel_filepath,
                sankey,
                sheet_to_remove_names)
            if not ok:
                su_trace.logger.error(msg)
                return (sankey, sheet_to_remove_names, excel_filepath, tmp_dir)
        # Verify structure that we got
        ok, msg = sankey.check_overall_sankey_structure()
        if not ok:
            su_trace.logger.error(msg)
            return (sankey, sheet_to_remove_names, excel_filepath, tmp_dir)
        # Return
        return (sankey, sheet_to_remove_names, excel_filepath, tmp_dir)

    def _compare_recursively(
        self,
        test_entry: dict,
        ref_entry: dict
    ):
        """
        Compare two dicts recursively

        Parameters
        ----------
        :param test_entry: _description_
        :type test_entry: dict

        :param ref_entry: _description_
        :type ref_entry: dict

        Optional parameters
        -------------------
        """
        # Dict -> Recurs
        if isinstance(test_entry, dict):
            for key in test_entry.keys():
                if key != LOGS_KEY:
                    self._compare_recursively(
                        test_entry[key],
                        ref_entry[key])
            return
        # List -> loop on all items
        if isinstance(test_entry, list):
            for item_to_test, item_as_ref in zip(test_entry, ref_entry):
                self._compare_recursively(
                    item_to_test,
                    item_as_ref)
            return
        # Float -> test approx
        if isinstance(test_entry, float):
            self.assertAlmostEqual(
                test_entry,
                ref_entry, 2)
            return
        # Normal test
        self.assertEqual(
            test_entry,
            ref_entry)

    def check_logs(
        self,
        expected_results: dict,
        test_name: str
    ):
        """
        Compare logs with expected logs

        Parameters
        ----------
        :param expected_results: Dict that contains results to check with
        :type expected_results: dict

        :param test_name: Name of current test
        :type test_name: str
        """
        # Read current logs
        base_filename = su_trace.base_filename()
        with open(base_filename, "r") as f:
            results = f.read()
        # Splited lines
        results_array = results.split('\n')
        # Splited line but filtered
        filter_result_array = []
        for row in results_array:
            if ('Main Problem' in row) or \
               ('DEBUG' in row) or \
               ('PERF' in row) or \
               ('SOLVED in' in row):
                continue
            if 'Entering variables classification at' in row:
                continue
            if ('took' in row) or \
               ('Took' in row) or \
               ('done in' in row) or \
               ('matrix reduction done' in row) or \
               ('Output (matrix_reduction)' in row) or \
               ('Interval' in row):
                continue
            filter_result_array.append(row)
        # Check if logs are the same
        if not self.generate_results:
            self.assertEqual(
                filter_result_array,
                expected_results[LOGS_KEY])
        else:
            if test_name not in self.new_results:
                self.new_results[test_name] = {}
            self.new_results[test_name][LOGS_KEY] = filter_result_array

    def compare_sankey(
        self,
        test_name: str,
        sankey: Sankey,
        expected_results: dict
    ):
        """
        Compare a Sankey struct to expected results

        Parameters
        ----------
        :param test_name: name of current test
        :type test_name: str

        :param sankey: current sankey struct to check
        :type sankey: Sankey

        :param expected_results:  Dict that contains results to check with
        :type expected_results: dict
        """
        # Get sankey equivalent dict
        sankey_dict = sankey.get_as_dict()
        # Run tests
        if not self.generate_results:
            # Compare with ref
            self._compare_recursively(
                sankey_dict,
                expected_results[SANKEY_KEY])
            return
        # Create test
        if test_name not in self.new_results:
            self.new_results[test_name] = {}
        self.new_results[test_name][SANKEY_KEY] = sankey_dict

    @classmethod
    def tearDownClass(cls):
        if cls.generate_results:
            for test_name in cls.new_results:
                test_dir, test_subname = os.path.split(test_name)
                test_refs_dir = os.path.join(TESTS_DIR, test_dir, XLPARSER_TESTS_REFS_DIR)
                # Save logs
                if LOGS_KEY in cls.new_results[test_name].keys():
                    test_logs_filename = REF_TEST_PREFIX + test_subname + REF_LOG_SUFFIX + '.json'
                    test_logs_filepath = os.path.join(test_refs_dir, test_logs_filename)
                    logs_as_json = json.dumps(cls.new_results[test_name][LOGS_KEY], indent=2)
                    with open(test_logs_filepath, "w") as test_logs_file:
                        test_logs_file.write(logs_as_json)
                # Save sankey struct as json if present (if reconciliation did not failed)
                if SANKEY_KEY in cls.new_results[test_name].keys():
                    test_sankey_filename = REF_TEST_PREFIX + test_subname + REF_SANKEY_SUFFIX + '.json'
                    test_sankey_filepath = os.path.join(test_refs_dir, test_sankey_filename)
                    sankey_as_json = json.dumps(cls.new_results[test_name][SANKEY_KEY], indent=2)
                    with open(test_sankey_filepath, "w") as test_sankey_file:
                        test_sankey_file.write(sankey_as_json)
