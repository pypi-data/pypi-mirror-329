#!python

# External libs -----------------------------------------------------
import sys
import os
import argparse
import time

# External modules -------------------------------------------------
# ...

# Local modules -----------------------------------------------------

from SankeyExcelParser import su_trace
from SankeyExcelParser.sankey import Sankey
from SankeyExcelParser.io_excel import load_sankey_from_excel_file


# Functions ---------------------------------------------------------
def check_args():
    ''' This function controls parameters passed to the program
    '''
    # Get args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_file",
        required=True,
        type=argparse.FileType('r'),
        help="Input excel file (.xls or .xlsx)")
    args = parser.parse_args()
    # Check if args are ok
    input_file = args.input_file
    iext = os.path.splitext(input_file.name)[1]
    if iext not in ('.xls', '.xlsx'):
        su_trace.logger.critical(
            "Mauvaise extension pour le fichier d\'input.\n" +
            parser.format_help())
        sys.exit()
    # Return processed args
    return input_file.name, False


def log_time(t_start, t_cur, t_prev=None):
    if t_prev is None:
        log = '-- Took {} seconds --'.format(
            round((t_cur-t_start), 2))
    else:
        log = '-- Took {0} / {1} seconds --'.format(
            round((t_cur-t_prev), 2),
            round((t_cur-t_start), 2))
    return log


# Main ---------------------------------------------------------
if __name__ == '__main__':

    log_file = su_trace.check_log()
    su_trace.run_log(log_file)
    su_trace.logger.info('[STARTED]')
    t_start = time.time()

    # 0. Get conversion arguments
    excel_input_filename, debug = check_args()
    if debug:
        su_trace.log_level("DEBUG")
    t = time.time()
    su_trace.logger.info('-- INPUT ARGUMENTS CHECKED --')
    su_trace.logger.debug(log_time(t_start, t))
    t_prev = t

    # 1. load sankey struct from excel file
    su_trace.logger.debug('-- LOAD MFA PROBLEM INPUT FROM EXCEL. --')
    su_trace.logger.debug('Input file is : {}'.format(excel_input_filename))
    sankey = Sankey()
    ok, msg = load_sankey_from_excel_file(
        excel_input_filename,
        sankey)
    t = time.time()
    if (ok):
        su_trace.logger.info(
            '-- MFA PROBLEM INPUT LOADED FROM EXCEL SUCCEEDED --')
        su_trace.logger.debug(log_time(t_start, t, t_prev))
    else:
        su_trace.logger.critical(
            '-- ERROR : Loading Excel file has failed')
        su_trace.logger.critical('-- {}'.format(msg))
        su_trace.logger.info(
            '-- MFA PROBLEM INPUT LOADED FROM EXCEL FAILED -- ')
        su_trace.logger.debug(log_time(t_start, t, t_prev))
        su_trace.logger.info('[FAILED]')
        sys.exit()
    t_prev = t

    # 2. Check sankey integrity
    su_trace.logger.debug('-- CHECK MFA PROBLEM OVERALL STRUCTURE --')
    ok, msg = sankey.check_overall_sankey_structure()
    t = time.time()
    if (ok):
        su_trace.logger.info(
            '-- MFA PROBLEM OVERALL STRUCTURE SUCCEEDED --')
        su_trace.logger.debug(log_time(t_start, t, t_prev))
    else:
        su_trace.logger.critical(
            '-- ERROR : Sankey overall checked has failed')
        su_trace.logger.critical('-- {}'.format(msg))
        su_trace.logger.info(
            '-- MFA PROBLEM OVERALL STRUCTURE CHECK FAILED --')
        su_trace.logger.debug(log_time(t_start, t, t_prev))
        su_trace.logger.info('[FAILED]')
        sys.exit()
    t_prev = t

    # End
    su_trace.logger.info('[COMPLETED]')
    su_trace.logger.debug(log_time(t_start, time.time()))
