"""
Auteur : Vincent LE DOZE
Date : 07/12/23
"""

# External libs ---------------------------------------------------------------
import argparse
import os
import unittest
from parameterized import parameterized

# Local modules ---------------------------------------------------------------
from SankeyExcelParser.tests.integration.test_base import MFAProblemsTests
from SankeyExcelParser.tests.integration.test_base import TEST_PARAMETERS
from SankeyExcelParser.io_excel import write_excel_from_sankey


# Class -----------------------------------------------------------------------
class MFAProblemTestConversion(MFAProblemsTests):

    @parameterized.expand(TEST_PARAMETERS, skip_on_empty=True)
    def test_conversions(
        self,
        test_name: str,
        file_name: str,
        expected_results: dict
    ):
        """
        Check if rewriting Excel works as intended

        Parameters
        ----------
        :param test_name: Name of current test
        :type test_name: str

        :param file_name: Name of current excel fil to test
        :type file_name: str

        :param expected_results: Dict of expected results to check with
        :type expected_results: dict
        """
        # For Debug
        print('\n{}'.format(self._testMethodName), end=' -> ', flush=True)
        # Read and check file
        (
            sankey,
            sheet_to_remove_names,
            excel_filepath,
            tmp_dir
        ) = self.prepare_test(file_name, use_reconciled=False)
        # Prepare output file
        root_file_name = os.path.splitext(os.path.basename(excel_filepath))[0]
        output_file_name = os.path.join(tmp_dir, root_file_name+'.xlsx')
        # Write output file
        write_excel_from_sankey(
            output_file_name,
            sankey,
            mode='w',
            sheets_to_remove__names=sheet_to_remove_names)


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
        names = loader.getTestCaseNames(MFAProblemTestConversion)
    else:
        names = args.filenames
    # Append tests to test suite
    suite = unittest.TestSuite()
    for name in names:
        try:
            suite.addTest(MFAProblemTestConversion(name))
        except Exception:
            print("Error when adding {} to test base".format(name))
    # Run tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
