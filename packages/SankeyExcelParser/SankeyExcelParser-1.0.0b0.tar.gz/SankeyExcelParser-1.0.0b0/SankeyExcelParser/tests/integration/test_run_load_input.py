"""
Auteur : Vincent LE DOZE
Date : 07/12/23
"""

# External libs ---------------------------------------------------------------
import argparse
import unittest
from parameterized import parameterized

# Local modules ---------------------------------------------------------------
from SankeyExcelParser.tests.integration.test_base import MFAProblemsTests
from SankeyExcelParser.tests.integration.test_base import TEST_PARAMETERS
from SankeyExcelParser.tests.integration.test_base import LOGS_KEY


# Class -----------------------------------------------------------------------
class MFAProblemTestInput(MFAProblemsTests):

    @parameterized.expand(TEST_PARAMETERS, skip_on_empty=True)
    def test_excel_input(
        self,
        test_name: str,
        file_name: str,
        expected_results: dict
    ):
        """
        Compare Sankey struct that is extracted from Excel file with expected results

        Parameters
        ----------
        :param test_name: Name of current test
        :type test_name: str

        :param file_name: Excel file to test
        :type file_name: str

        :param expected_results: Dict that contains results to check with
        :type expected_results: dict
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
        # Compare results
        self.compare_sankey(
            test_name,
            sankey,
            expected_results)
        # Delete useless entries to avoid erasing previous results
        if self.generate_results:
            del expected_results[LOGS_KEY]


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
        names = loader.getTestCaseNames(MFAProblemTestInput)
    else:
        names = args.filenames
    # Append tests to test suite
    suite = unittest.TestSuite()
    for name in names:
        try:
            suite.addTest(MFAProblemTestInput(name))
        except Exception:
            print("Error when adding {} to test base".format(name))
    # Run tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
