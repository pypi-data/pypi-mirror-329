#!python

# External libs -----------------------------------------------------
import sys
import os
import argparse
import tempfile
import time

# External modules -------------------------------------------------
from shutil import copyfile

# Local modules -----------------------------------------------------
from SankeyExcelParser import su_trace
from SankeyExcelParser.sankey import Sankey
from SankeyExcelParser.io_excel import load_sankey_from_excel_file
from SankeyExcelParser.io_excel import write_excel_from_sankey


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
    parser.add_argument(
        "--output_dir",
        default="tmp",
        choices=['tmp', 'input', 'path'],
        nargs='*',
        help="'tmp', 'input' (same as input) or 'path'(full path without quote)")
    args = parser.parse_args()
    # Check if args are ok
    input_file = args.input_file
    iext = os.path.splitext(input_file.name)[1]
    if iext not in ('.xls', '.xlsx'):
        su_trace.logger.critical(
            "Mauvaise extension pour le fichier d\'input.\n" +
            parser.format_help())
        sys.exit()
    if type(args.output_dir) is not list:
        args.output_dir = [args.output_dir]
    # Return processed args
    return input_file.name, args.output_dir, False


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
    t0 = time.time()
    excel_input_filename, output_dir, debug = check_args()
    if output_dir[0] == 'tmp':
        output_directory = tempfile.mkdtemp()
    if output_dir[0] == 'input':
        output_directory = os.path.dirname(excel_input_filename)
    if output_dir[0] == 'path':
        output_directory = os.path.dirname(output_dir[1])

    if debug:
        su_trace.log_level("DEBUG")
    t = time.time()
    su_trace.logger.info('-- INPUT ARGUMENTS CHECKED --')
    su_trace.logger.debug(log_time(t_start, t))
    t_prev = t

    # 1. load sankey struct from excel file
    su_trace.logger.debug('-- LOAD SANKEY INPUT FROM EXCEL. --')
    su_trace.logger.debug('Input file is : {}'.format(excel_input_filename))
    sankey = Sankey()
    ok, msg = load_sankey_from_excel_file(
        excel_input_filename,
        sankey)
    t = time.time()
    if (ok):
        su_trace.logger.info('-- SANKEY INPUT LOADED FROM EXCEL SUCCEEDED --')
        su_trace.logger.debug(log_time(t_start, t, t_prev))
    else:
        su_trace.logger.critical('-- ERROR : Loading Excel file has failed')
        su_trace.logger.critical('-- {}'.format(msg))
        su_trace.logger.info('-- SANKEY INPUT LOADED FROM EXCEL FAILED -- ')
        su_trace.logger.debug(log_time(t_start, t, t_prev))
        su_trace.logger.info('[FAILED]')
        sys.exit()
    t_prev = t
    t1 = time.time()
    # Log infos about arguments used
    su_trace.logger.info('-- INPUT ARGUMENTS CHECKED, TOOK ' + str(round((t1-t0), 2)) + ' sec --')

    # 2. Check sankey integrity
    su_trace.logger.debug('-- CHECK SANKEY OVERALL STRUCTURE --')
    ok, msg = sankey.check_overall_sankey_structure()
    t = time.time()
    if (ok):
        su_trace.logger.info(
            '-- SANKEY OVERALL STRUCTURE SUCCEEDED --')
        su_trace.logger.debug(log_time(t_start, t, t_prev))
    else:
        su_trace.logger.critical(
            '-- ERROR : Sankey overall checked has failed')
        su_trace.logger.critical('-- {}'.format(msg))
        su_trace.logger.info(
            '-- SANKEY OVERALL STRUCTURE CHECK FAILED --')
        su_trace.logger.debug(log_time(t_start, t, t_prev))
        su_trace.logger.info('[FAILED]')
        sys.exit()
    t_prev = t

    # 3.  Writes results to excel
    su_trace.logger.debug('-- REWRITE SANKEY TO EXCEL --')
    try:
        excel_root_filename = os.path.splitext(os.path.basename(excel_input_filename))[0]
        excel_output_filename = os.path.join(output_directory, excel_root_filename+'_roundtrip'+'.xlsx')
        copyfile(excel_input_filename, excel_output_filename)
        su_trace.logger.info('-- Output file : {} '.format(excel_output_filename))
        write_excel_from_sankey(
            excel_output_filename,
            sankey)
    except Exception as excpt:
        t = time.time()
        su_trace.logger.critical('-- UNEXPECTED ERROR Rewriting sankey to excel file failed.')
        su_trace.logger.critical('-- {}'.format(excpt))
        su_trace.logger.info('-- REWRITE SANKEY TO EXCEL FAILED --')
        su_trace.logger.debug(log_time(t_start, t, t_prev))
        su_trace.logger.info('[FAILED]')
        sys.exit()

    t = time.time()
    su_trace.logger.info('-- REWRITE SANKEY TO EXCEL DONE --')
    su_trace.logger.debug(log_time(t_start, t, t_prev))

    # End
    su_trace.logger.info('[COMPLETED]')
    su_trace.logger.debug(log_time(t_start, time.time()))
