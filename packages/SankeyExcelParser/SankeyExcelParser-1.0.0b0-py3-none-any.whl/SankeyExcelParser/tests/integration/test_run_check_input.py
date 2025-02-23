"""
Auteur : Vincent LE DOZE
Date : 07/12/23
"""

# External libs ---------------------------------------------------------------
import argparse
# import os
import unittest
from parameterized import parameterized

# Local modules ---------------------------------------------------------------
from SankeyExcelParser.tests.integration.test_base import MFAProblemsTests
from SankeyExcelParser.tests.integration.test_base import TEST_PARAMETERS
from SankeyExcelParser.tests.integration.test_base import SANKEY_KEY


# Class -----------------------------------------------------------------------
class MFAProblemTestCheckInput(MFAProblemsTests):

    # @parameterized.expand([(
    #     os.path.relpath('Projets/AlimentationAnimale/orge check')+' input',
    #     os.path.relpath('Projets/AlimentationAnimale/orge_new_segm.xlsx'),
    #     EXPECTED_RESULTS[os.path.relpath('Projets/AlimentationAnimale/orge')+' check input'])])
    @parameterized.expand(TEST_PARAMETERS, skip_on_empty=True)
    def test_check_input(
        self,
        test_name: str,
        file_name: str,
        expected_results: dict
    ):
        """
        Check if Sankey extraction from Excel file is OK.


        Parameters
        ----------
        :param test_name: Name of current test
        :type test_name: str

        :param file_name: Name of current excel file to test
        :type file_name: str

        :param ouput_log: Logs expected for sankey extraction and checks
        :type ouput_log: list

        Optional parameters
        -------------------
        """
        # For Debug
        print('\n{}'.format(self._testMethodName), end=' -> ', flush=True)
        # Read and check file
        (
            sankey,
            sheet_to_remove_names,
            excel_filepath,
            _
        ) = self.prepare_test(file_name)
        # Check logs
        self.check_logs(expected_results, test_name)
        # Delete useless entries to avoid erasing previous results
        if self.generate_results:
            del expected_results[SANKEY_KEY]


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
        MFAProblemsTests.set_generate_results()
    # Get tests names to run
    if len(args.filenames) == 0:
        loader = unittest.TestLoader()
        names = loader.getTestCaseNames(MFAProblemTestCheckInput)
    else:
        names = args.filenames
    # Append tests to test suite
    suite = unittest.TestSuite()
    for name in names:
        try:
            suite.addTest(MFAProblemTestCheckInput(name))
        except Exception:
            print("Error when adding {} to test base".format(name))
    # Run tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
