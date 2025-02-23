"""
This module is dedicated to the conversion from outside format to internal json format.
Outside formats may be: a workbook (excel), another json file, a database etc...
Structure and specifications of internal json format are defined in this module. Internal
json format can take two main forms: one to adress input informations and a second one
for output communications.
"""

# External libs -----------------------------------------------------
import pandas as pd
import numpy as np
import re

# Local libs -------------------------------------------------------
import SankeyExcelParser.io_excel_constants as CONST
import SankeyExcelParser.su_trace as su_trace

# External modules -------------------------------------------------
from unidecode import unidecode

# Local modules -----------------------------------------------------
from SankeyExcelParser.sankey import Sankey, UserExcelConverter

# has_xl_wings = True
# try:
#     # import xlwings as xl
#     import pythoncom
#     pythoncom.CoInitialize()
# except Exception:
#     has_xl_wings = False


# Private functions ----------------------------------------------------------------
def _compareStrings(
    string_in: str,
    string_ref: str,
    strip_input_string=False
):
    """
    Uniformize strings for easier comparison.

    Parameters
    ----------
    :param string_in: String to compare.
    :type string_in: str

    :param string_ref: Ref string to compare with.
    :type string_ref: str

    :param strip_input_string: Remove ' ' at start / or end for input string.
    :type strip_input_string: boolean, optionnal (default=False)

    Returns
    -------
    :return:  True if strings mean the same thing, False otherwise
    :rtype: bool
    """
    s1 = string_in.lower()
    s2 = string_ref.lower()
    if strip_input_string:
        s1 = s1.strip()
    return (re.fullmatch(unidecode(s2), unidecode(s1)) is not None)


def _consistantColName(
    sheet_name: str,
    usr_col_name: str,
    xl_names_converter: UserExcelConverter,
    tags: list = []
):
    '''
    Test if the usr_col_name is consistent with the allowed col list.

    Parameters
    ----------
    :param sheet_name: Sheet name to check.
    :type sheet_name: string

    :param prop_cols: Column to find
    :type prop_cols: string

    :param tags: Tags list to check
    :type tags: list

    Returns
    -------
    :return:
        If the column corresponds to an entry in the sheetname dictionnary, then result is the corresponding key.
        If the column is a tag column / an additonnal column, the result is the standard format of the column name.
    :rtype: string
    '''
    # Check if Sheet is about data
    if _compareStrings(sheet_name, 'flux data', strip_input_string=True):
        xl_names_converter.add_new_col(sheet_name, CONST.DATA_SHEET, usr_col_name)
        return True, CONST.DATA_SHEET
    sheet_name_lower = sheet_name.lower()
    usr_col_name_lower = usr_col_name.lower()
    if sheet_name_lower != '' and usr_col_name_lower != '':
        # Is the proposed column a tag column ?
        for tag in tags:
            if _compareStrings(usr_col_name_lower, tag, strip_input_string=True):
                return True, tag
        # Is the proposed column in allowed columns ?
        for std_col_name in CONST.DICT_OF_COLS_NAMES__RE[sheet_name_lower].keys():
            for allowed_col_re in CONST.DICT_OF_COLS_NAMES__RE[sheet_name_lower][std_col_name]:
                if _compareStrings(usr_col_name_lower, allowed_col_re, strip_input_string=True):
                    xl_names_converter.add_new_col(sheet_name_lower, std_col_name, usr_col_name)
                    return True, std_col_name
    return False, usr_col_name


def _consistantSheetName(
    usr_sheet_name: str,
    xl_names_converter: UserExcelConverter,
):
    '''
    Test if the usr_sheet_name is consistent with the allowed sheet list.

    Parameters
    ----------
    :param usr_sheet_name: Sheet name to check.
    :type usr_sheet_name: string

    Returns
    -------
    :return:
        - out1: True if tested sheet is consistant.
        - out2: The dictionary key corresponding of the allowed list found, if tested sheet is consitant.
                List of allowed sheet names if not.
    :rtype: (bool, string)

    Notes
    -----
    - If the usr_sheet_name input is empty ('') the result is a list of
    allowed sheet name as a string.
    - A particular case is taken into account for proxy input file which
    usualy has 3 proxy sheets (and one of them with 'sector' keyword in its name)
    '''
    # Check if Sheet is about data
    if _compareStrings(usr_sheet_name, 'flux data', strip_input_string=True):
        xl_names_converter.add_new_sheet(CONST.DATA_SHEET, usr_sheet_name)
        return True, CONST.DATA_SHEET
    # If we have a sheet to check
    if usr_sheet_name != '':
        # Is sheet in list of possible names for sheets
        for std_sheet_name in CONST.DICT_OF_SHEET_NAMES__RE.keys():
            for allow_sheet_re in CONST.DICT_OF_SHEET_NAMES__RE[std_sheet_name]:
                if _compareStrings(usr_sheet_name, allow_sheet_re, strip_input_string=True):
                    xl_names_converter.add_new_sheet(std_sheet_name, usr_sheet_name)
                    return True, std_sheet_name
    #  We didn't found the corresponding key
    return False, _allowedSheetNames()


def _allowedSheetNames(sheets_to_show=[]):
    '''
    Return the table of allowed sheet names with respect to their type of informations.

    Parameters
    ----------
    :param sheets_to_show: list of sheet to print. If list empty, print all.
    :type sheets_to_show: list, optional, default=[]

    Returns
    -------
    :return:
        Result is empty string if the tested col is not consistant.
        Result is the dictionary key corresponding of the allowed list found.
    :rtype: string
    '''
    wcol1 = 30
    wcol2 = 70
    # Create table header
    list_allowed = '{0: <{w1}} | {1: <{w2}}\n'.format("Sheet type", "Possible sheet names", w1=wcol1, w2=wcol2)
    list_allowed += '-'*(wcol1 + wcol2 + 3) + '\n'
    # Keys to show = table first column
    if len(sheets_to_show) > 0:
        list_dict_keys = [_ for _ in sheets_to_show if _ in CONST.DICT_OF_SHEET_NAMES.keys()]
    else:
        list_dict_keys = CONST.DICT_OF_SHEET_NAMES.keys()
    # Create table
    for dict_key in list_dict_keys:
        list_allowed += '{: <{w}} | '.format(dict_key, w=wcol1)
        if len(CONST.DICT_OF_SHEET_NAMES[dict_key]) != 0:
            list_allowed += ', '.join(set(CONST.DICT_OF_SHEET_NAMES[dict_key]))
        list_allowed += '\n'
    return list_allowed


def _checkNeededColumns(
    columns: list,
    columns_needed: list,
    sheet_name: str,
    columns_needed_onlyone: list = []
):
    """_summary_

    Parameters
    ----------
    :param columns: Current list of columns
    :type columns: list

    :param columns_needed: List of columns to have
    :type columns_needed: list

    :param sheet_name: Sheet name from which to check names
    :type sheet_name: str

    :param columns_needed_onlyone: List of columns in which at least only one is needed
    :type columns_needed_onlyone: list

    Returns
    -------
    :return: (Success?, Log message)
    :rtype: (bool, str)
    """
    # Check columns need
    for column_needed in columns_needed:
        if not (column_needed in columns):
            err_msg = 'The \"{}\" column is missing '.format(column_needed)
            err_msg += 'or does not have the correct name.\n'
            err_msg += '\n'
            err_msg += '{}\n'.format(CONST.DICT_OF_COMMENTS[sheet_name][column_needed][0])
            err_msg += '\n'
            std_column_names = set(CONST.DICT_OF_COLS_NAMES[sheet_name][column_needed])
            err_msg += 'Acceptable names for this column : {}'.format(
                ', '.join(['\"{}\"'.format(_) for _ in std_column_names]))
            return False, err_msg
    # Check optionnal columns (need_only one)
    if len(columns_needed_onlyone) > 0:
        if (not any(np.in1d(columns_needed_onlyone, columns))):
            err_msg = 'A mandatory column is missing or does not have the correct name.\n'
            err_msg += 'A least one of these columns must be present : {}'.format(
                ', '.join(['\"{}\"'.format(_) for _ in columns_needed_onlyone]))
            return False, err_msg
    return True, ''


def _castColumnType(
    sheet: pd.DataFrame,
    columns_types,
    empty_to_default_value=False
):
    """
    Set specific columns values to str.

    Parameters
    ----------
    :param sheet: Sheet to modify.
    :type sheet: pandas.DataFrame, modified

    :param columns_types: Dict of column and their default types/values OR any default value.
    :type columns_types: any

    :param empty_to_default_value: If true, set empty cells with default value, if not, set as None.
    :type: bool

    Returns
    -------
    :return: (Success? ; Log message)
    :rtype: (bool, str)
    """
    # Filter column to convert / Columns that are in sheet
    if type(columns_types) is dict:
        cols_to_convert = \
            [(_, columns_types[_]) for _ in columns_types.keys() if _ in sheet.columns]
    else:
        cols_to_convert = \
            [(_, columns_types) for _ in sheet.columns]
    # Convert
    for (col, _) in cols_to_convert:
        try:
            # Special type
            if type(_) is dict:
                val = _['val']
            else:
                val = _
            # Convert as string
            if type(val) is str:
                sheet[col] = sheet[col].replace({np.nan: 'None'})
                sheet[col] = sheet[col].astype(str)
                if empty_to_default_value:
                    sheet[col] = sheet[col].replace({'None': val})
                else:
                    sheet[col] = sheet[col].replace({'None': None})
            # Convert as float
            elif type(val) is float:
                sheet[col] = sheet[col].astype(float)
                if empty_to_default_value:
                    sheet[col] = sheet[col].replace({np.nan: val})
                else:
                    sheet[col] = sheet[col].replace({np.nan: None})
            # Convert as int
            elif type(val) is int:
                sheet[col] = sheet[col].replace({np.nan: -702313053})
                sheet[col] = sheet[col].astype(int)
                if empty_to_default_value:
                    sheet[col] = sheet[col].replace({-702313053: val})
                else:
                    sheet[col] = sheet[col].replace({-702313053: None})
            # Convert to other types
            else:
                sheet[col] = sheet[col].astype(type(val))
        except Exception:
            err = 'Column \"{}\" contains values '.format(col)
            err += 'that could not be read as {} values'.format(type(val))
            return False, err
    # Replace remaining empty data with None
    sheet.replace({np.nan: None}, inplace=True)
    return True, ''


def _pd_sorted_col(
    dft: pd.DataFrame,
    lico: list
):
    """
    Sort columns order of a dataframe in function of a column list

    Parameters
    ----------
    :param dft: Input dataframe to sort.
    :type dft: pandas.DataFrame

    :param lico: Ordered list of columns to have.
    :type lico: list

    Returns
    -------
    :return: Sorted dataframe.
    :rtype: (bool; string)

    """
    li_df = list(dft)
    if li_df != lico:
        dftm = pd.DataFrame(columns=lico)
        for col in lico:
            dftm[col] = dft[col]
    return dftm


def _extractTablesFromSheet(
    sheet: pd.DataFrame,
    new_sheets: list,
    default_columns_names=None
):
    """
    Extract all tables from an excel sheet.

    Ex: Extract tables from a sheet like this

    +----+----+----+----+----+
    | -  | -  | -  | -  | -  |
    +----+----+----+----+----+
    | -  | -  | C1 | C2 | C3 |
    +----+----+----+----+----+
    | -  | R1 | x  | -  | x  |
    +----+----+----+----+----+
    | -  | R2 | x  | x  | -  |
    +----+----+----+----+----+
    | -  | -  | -  | -  | -  |
    +----+----+----+----+----+
    | -  | -  | C4 | C5 | C6 |
    +----+----+----+----+----+
    | -  | R3 | -  | x  | x  |
    +----+----+----+----+----+
    | -  | R4 | x  | -  | -  |
    +----+----+----+----+----+

    Or like this

    +----+----+----+----+----+
    | -  | -  | -  | -  | -  |
    +----+----+----+----+----+
    | -  | -  | C1 | C2 | C3 |
    +----+----+----+----+----+
    | -  | R1 | x  | -  | x  |
    +----+----+----+----+----+
    | -  | R2 | x  | x  | -  |
    +----+----+----+----+----+
    | -  | -  | -  | -  | -  |
    +----+----+----+----+----+
    | -  | R3 | -  | x  | x  |
    +----+----+----+----+----+
    | -  | R4 | x  | -  | -  |
    +----+----+----+----+----+

    Parameters
    ----------
    :param sheet: Sheet to parse
    :type sheet: pd.DataFrame

    :param new_sheets: List of sheets extracted from sheet
    :type new_sheets: list(pd.DataFrame), modified

    Returns
    -------
    :return: _description_
    :rtype: _type_
    """
    # Nothing to do
    if sheet.empty:
        return True
    # If we dont have any default column name -> read column index
    # -> Useful if first row is composed of name of node
    # -> Need to get rid of Unamed cols
    # -> Then if nodes are mentionned in more than one column, panda add a '.x' (x a number)
    #    at the end of the node name, so we need to get rid of that too...
    if default_columns_names is None:
        default_columns_names = []
        for _ in sheet.columns:
            if isinstance(_, str):
                if (re.fullmatch('Unnamed:.*', _) is None):
                    end_ = re.search('([.][0-9]+)\Z', _)  # noqa: W605
                    if end_ is not None:
                        default_columns_names.append(_[:-len(end_[0])])
                    else:
                        default_columns_names.append(_)
    # Need to reindex sheet to use enumerated correctly index and columns
    sheet = sheet.reset_index(drop=True)
    sheet = sheet.T.reset_index(drop=True).T
    # ----------------- Initialize starting and ending points
    start_row = 0
    start_col = 0
    index_col = 0  # Column number for index names
    end_row = sheet.shape[0]
    end_col = sheet.shape[1]
    # ---------------- Find starting point
    found_starting_point = False
    for row in range(sheet.shape[0]):
        for col in range(sheet.shape[1]):
            # Check if current val is NaN (empty cell)
            val = sheet.iat[row, col]
            is_nan = (val != val)
            # If not -> Bingo
            found_starting_point = (not is_nan)
            if found_starting_point:
                start_row = row
                start_col = col
                index_col = col
                break
        if found_starting_point:
            break
    # ------------ Check table format with upper left corner
    upper_left_corner = sheet.iloc[start_row:min(start_row+2, end_row), start_col:min(start_col+2, end_col)]
    # Not enought data in given sheet -> stop ?
    if (upper_left_corner.shape[0] < 2):
        # Modify starting row to avoid missing table with only one line
        start_row = max(0, start_row-1)
        upper_left_corner = sheet.iloc[start_row:min(start_row+2, end_row), start_col:min(start_col+2, end_col)]
    if (upper_left_corner.shape[1] < 2):
        # Modify starting col to avoid missing table with only one col
        start_col = max(0, start_col-1)
        index_col = start_col
        upper_left_corner = sheet.iloc[start_row:min(start_row+2, end_row), start_col:min(start_col+2, end_col)]
    if (upper_left_corner.shape[0] < 2) or (upper_left_corner.shape[1] < 2):
        # Ok table does not contain any data
        return True
    # Upper left corner is an isolated value ?
    v1 = upper_left_corner.iloc[0, 1]
    v2 = upper_left_corner.iloc[1, 0]
    if (v1 != v1) and (v2 != v2):
        # Retry but without the isolated value
        sheet_copy = sheet.copy()  # copy to be sure that we dont modify original sheet
        sheet_copy.iloc[start_row, start_col] = np.nan
        return _extractTablesFromSheet(sheet_copy, new_sheets, default_columns_names=default_columns_names)
    # First column is an overhead ?
    if (not _isValueAcceptedInMatrixTable(upper_left_corner.iloc[1, 1])):
        # Retry but without the isolated value
        sheet_copy = sheet.copy()  # copy to be sure that we dont modify original sheet
        sheet_copy.iloc[start_row, start_col:end_col] = np.nan
        return _extractTablesFromSheet(sheet_copy, new_sheets, default_columns_names=default_columns_names)
    # Check if the content of first row = column names
    columns_names = None
    # Check what upper left corner of table contains
    # In all case : 'val' can be 'x', 'X' or some stringified float value.
    # Case 1 : upper left corner = ['R1', 'val' / NaN]
    # ...                          ['R2', 'val' / NaN]
    # ...      -> 'val' and NaN can be turned as float.
    # Case 2 : upper left corner = ['C1',        'C2']
    # ...                          ['val' / Nan, 'val' / NaN]
    # ...      -> On first row, can not turn columns names as float
    # ...      -> On first col, 'val' and NaN can be turned as float
    # Case 3 : upper left corner = ['table name', 'C1'       ]
    # ...                          ['R1'        , 'val' / NaN]
    # ...      -> On first row, can not turn table name or columns names as float
    # ...      -> On first col, No row name can be turned as float
    if _isValueAcceptedInMatrixTable(upper_left_corner.iloc[0, 1]):
        case = 1
    else:
        if _isValueAcceptedInMatrixTable(upper_left_corner.iloc[1, 0]):
            case = 2
        else:
            case = 3
    # Check in which case we are
    if (case == 1):
        # Case 1 -> need to use defaut columns names
        columns_names = default_columns_names
        # Start col is one col on the right, because first col is index names
        start_col = min(start_col+1, end_col)
        # Ending col is easy to find
        end_col = min(start_col + len(columns_names), end_col)
    if (case == 2):
        # Case 2 -> There are columns name on the first row
        columns_names = sheet.astype('str').iloc[start_row, start_col:].to_list()
        # start row is one row below & index col is one col before
        start_row = min(start_row+1, end_row)
        index_col = max(0, index_col-1)
    if (case == 3):
        # Case 3 -> There are columns name on the first row, but starting one col on the right
        columns_names = sheet.astype('str').iloc[start_row, (start_col+1):].to_list()
        # start row is one row below & index col does not change, and start col is one col on the right
        start_row = min(start_row+1, end_row)
        start_col = min(start_col+1, end_col)
    if (case == 2) or (case == 3):
        # Case 2 & 3 : Find ending col
        for [i, col_name] in enumerate(columns_names):
            # Check if current col name is NaN (empty cell)
            is_nan = (col_name != col_name)
            # If nan -> Bingo
            if is_nan:
                end_col = min(start_col + i, end_col)
                columns_names = columns_names[:i]
                break
    # No default column name was provided -> Error
    if columns_names is None:
        return False
    # ------------ Check what first col contains
    index_names = sheet.iloc[start_row:end_row, index_col].to_list()
    # ------------- Find ending row
    for (i, index_name) in enumerate(index_names):
        # Check if current val is NaN (empty cell)
        is_nan = (index_name != index_name)
        # If nan -> Bingo
        if is_nan:
            end_row = min(i + start_row, end_row)
            index_names = index_names[:i]
            break
    # New table
    new_table = sheet.iloc[start_row:end_row, start_col:end_col]
    if len(new_table.columns) != len(columns_names):
        su_trace.logger.error('Could not read ter table')
        return False
    new_table.columns = [_.strip() if (type(_) is str) else _ for _ in columns_names]
    new_table.index = [_.strip() if (type(_) is str) else _ for _ in index_names]
    new_sheets.append(new_table)
    # Find other table if needed
    ok = True
    ok &= _extractTablesFromSheet(
        sheet.iloc[:, end_col:], new_sheets,
        default_columns_names=columns_names)  # Upper right missing part of sheet
    ok &= _extractTablesFromSheet(
        sheet.iloc[end_row:, :], new_sheets,
        default_columns_names=columns_names)  # Down missing part of sheet
    # TODO revoir découpage des restes de table en recurrence
    return ok


def _isValueAcceptedInMatrixTable(value):
    """
    In Matrix table, accepted values are NaN, Numbers and 'x' or 'X'

    Parameters
    ----------
    :param value: Value to test
    :type value: Any

    Returns
    -------
    :return: True if value is Ok, else false
    :rtype: boolean
    """
    # First check if value is a number or NaN
    # by try to convert it to float
    try:
        float(value)
        return True
    except ValueError:
        # If it fails, then it's not NaN or a number
        # but it can be either 'x' or 'X'
        OK_but_not_a_number = '[xX]'
        try:
            if (re.fullmatch(OK_but_not_a_number, str(value)) is not None):
                return True
        except ValueError:
            pass
    return False


def _hasDuplicatedEntry(entries: list):
    """
    """
    duplicates = {}
    for (i, entry) in enumerate(entries):
        if entries.count(entry) > 1:
            if entry not in duplicates.keys():
                duplicates[entry] = []
            duplicates[entry].append(i)
    # duplicates = [entry for entry in entries if entries.count(entry) > 1]
    return (len(duplicates) > 0), duplicates


def _fuseDuplicatedColumns(table: pd.DataFrame, dup_cols: dict):
    # Get current columns names
    new_columns_names = table.columns.to_list()
    new_tables = {}
    # For each duplicated column, get the column name and positions of duplicat
    for (col_name, cols_index) in dup_cols.items():
        # Fuse columns
        new_tables[col_name] = table.loc[:, col_name].apply(lambda row: row.values[0], axis=1)
        # Rename duplicated columns, except the first one
        for (i, col_index) in enumerate(cols_index):
            if i == 0:
                continue
            new_columns_names[col_index] = col_name+'_dup'
    # Set new columns names
    table.columns = new_columns_names
    # Drop and replace
    for (col_name, sub_table) in new_tables.items():
        # Drop the renamed columns (except the first one)
        table.drop(columns=(col_name+'_dup'), inplace=True)
        # Apply the fused data on the remaining column
        table[col_name] = sub_table


def _fuseDuplicatedRows(table: pd.DataFrame, dup_rows: dict):
    # Get current columns names
    new_index_names = table.index.to_list()
    new_tables = {}
    # For each duplicated column, get the column name and positions of duplicat
    for (row_name, rows_index) in dup_rows.items():
        # Fuse columns
        new_tables[row_name] = table.loc[row_name, :].apply(lambda col: col.values[0], axis=0)
        # Rename duplicated columns, except the first one
        for (i, row_index) in enumerate(rows_index):
            if i == 0:
                continue
            new_index_names[row_index] = row_name+'_dup'
    # Set new index names
    table.index = new_index_names
    # Drop and replace
    for (row_name, sub_table) in new_tables.items():
        # Drop the renamed columns (except the first one)
        table.drop(index=(row_name+'_dup'), inplace=True)
        # Apply the fused data on the remaining column
        table.loc[row_name, :] = sub_table


# PUBLIC FUNCTIONS ----------------------------------------------------------------
def consistantSheetName(
    usr_sheet_name: str,
    sankey: Sankey
):
    '''
    Test if the usr_sheet_name is consistent with the allowed sheet list.

    Parameters
    ----------
    usr_sheet_name : string
        Sheet name to check.

    Returns
    -------
    string
        Result is empty string if the tested sheet is not consistant.
        Result is the dictionary key corresponding of the allowed list found.

    Notes
    -----
    - If the usr_sheet_name input is empty ('') the result is a list of
    allowed sheet name as a string.
    - A particular case is taken into account for proxy input file which
    usualy has 3 proxy sheets (and one of them with 'sector' keyword in its name)
    '''
    _, res = _consistantSheetName(usr_sheet_name, sankey.xl_user_converter)
    return res


def consistantColName(
    sheet_name: str,
    prop_col: str,
    sankey: Sankey,
    tags: list = []
):
    '''
    Test if the prop_col is consistent with the allowed col list.

    Parameters
    ----------
    :param sheet_name: Sheet name to check.
    :type sheet_name: string

    :param prop_cols: Column to find
    :type prop_cols: string

    :param tags: Tags list to check
    :type tags: list

    Returns
    -------
    :return:
        If the column corresponds to an entry in the sheetname dictionnary, then result is the corresponding key.
        If the column is a tag column / an additonnal column, the result is the standard format of the column name.
    :rtype: string
    '''
    _, res = _consistantColName(
        sheet_name,
        prop_col,
        sankey.xl_user_converter,
        tags)
    return res


def load_sankey_from_excel_file(
    input_file: str,
    sankey: Sankey,
    do_coherence_checks: bool = False,
    sheet_to_remove_names: list = None,
):
    '''
    Main convertor routine. Call dedicated routine depending on input type
    Use global variable 'su_trace' to trace the file processing

    Parameters
    ----------
    :param input_file: input file name to load (with extension and path)
    :type input_file: string

    :param sankey: data struct as a Sankey object
    :type sankey: Sankey, modified

    :param do_coherence_checks: Do we trigger coherence checks on sankey structure ?
    :type do_coherence_checks: bool

    :param sheet_to_remove_names: List of sheet that will be rewrite or removed when re-export as excel
    :type sheet_to_remove_names: list, modified, optionnal (default=None)

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)
    '''
    # Read excel input
    excel_file = pd.ExcelFile(input_file)
    # If every went fine, get sheet name
    excel_sheet_names = excel_file.sheet_names
    # keeping sheets_to_show consistent sheets
    necessary_sheet_names = {}
    unconsistant_sheet_names = []
    use_sheet_to_remove_names = True
    if type(sheet_to_remove_names) is not list:
        use_sheet_to_remove_names = False
    for sheet_name in excel_sheet_names:
        # Get sheet reference name for given sheet name
        is_sheet_consistant, sheet_refkey = _consistantSheetName(sheet_name, sankey.xl_user_converter)
        if is_sheet_consistant:  # Got the reference name
            if sheet_refkey not in necessary_sheet_names:
                necessary_sheet_names[sheet_refkey] = [sheet_name]
            else:
                necessary_sheet_names[sheet_refkey].append(sheet_name)
        else:  # No reference name Found
            unconsistant_sheet_names.append(sheet_name)
    # Check if we got some sheets to process
    if len(necessary_sheet_names.keys()) == 0:
        err_msg = "We didn't find any sheet name as specified in the following table : \n"
        err_msg += _allowedSheetNames()
        return False, err_msg
    # Debug log
    su_trace.logger.debug('Names of excel sheets that will be processed : ')
    [su_trace.logger.debug('- {}'.format(_)) for _ in necessary_sheet_names.values()]
    if len(unconsistant_sheet_names) > 0:
        su_trace.logger.debug('Names of excel sheets that will be ignored : ')
        [su_trace.logger.debug('- {}'.format(_)) for _ in unconsistant_sheet_names]
    if use_sheet_to_remove_names:
        if len(sheet_to_remove_names) > 0:
            su_trace.logger.debug('Names of excel sheets that will be removed : ')
            [su_trace.logger.debug('- {}'.format(_)) for _ in sheet_to_remove_names]
    # Update struct
    return _read_sankey_from_excel_book(
        input_file,
        necessary_sheet_names,
        sankey,
        do_coherence_checks=do_coherence_checks)


def _read_sankey_from_excel_book(
    excel_file_name: str,
    sheet_names: dict,
    sankey: Sankey,
    do_coherence_checks: bool = False
):
    """
    Parse all sheets from excel book to create a sankey struct.

    Parameters
    ----------
    :param excel_book: Dataframe (eqv dict) corresponding to the sheets of the input excel file
    :type excel_book: pd.DataFrame

    :param sheet_names: input file worksheet dict as [reference sheet name: user sheet name]
    :type sheet_names: dict

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    :param do_coherence_checks: Do we trigger coherence checks on sankey structure ?
    :type do_coherence_checks: bool

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)
    """
    # TODO : useless but I keep it for now
    mfa_dict = {}
    # Verify that we have the minimum number of sheets
    ok, msg = check_sheets_before_reading(sheet_names)
    if not ok:
        return ok, msg
    # First create standardized node type tags if needed
    for _ in (CONST.PRODUCTS_SHEET, CONST.SECTORS_SHEET, CONST.EXCHANGES_SHEET):
        if _ in sheet_names.keys():
            sankey.get_or_create_tagg(
                CONST.NODE_TYPE,
                CONST.TAG_TYPE_NODE,
                ':'.join([
                    CONST.NODE_TYPE_PRODUCT,
                    CONST.NODE_TYPE_SECTOR,
                    CONST.NODE_TYPE_EXCHANGE]))
            break
    # Then check all other TAGS
    if CONST.TAG_SHEET in sheet_names.keys():
        # Read tags
        for tag_sheet_name in sheet_names[CONST.TAG_SHEET]:
            su_trace.logger.info('Reading sheet {}'.format(tag_sheet_name))
            ok, msg = xl_read_tags_sheet(pd.read_excel(excel_file_name, tag_sheet_name), sankey)
            if not ok:
                return ok, "Error on sheet {0} ({1}) : {2}".format(tag_sheet_name, CONST.TAG_SHEET, msg)
            # Log warning messages
            if len(msg) > 0:
                su_trace.logger.error('Warning(s) on sheet {0} ({1}) :'.format(tag_sheet_name, CONST.TAG_SHEET))
                for _ in msg.split('\n'):
                    if len(_) > 0:
                        su_trace.logger.error(' - {}'.format(_))
    # Then check nodes, but in this order
    options = {}
    options['warn_on_new_nodes'] = False
    options['warn_on_new_flux'] = False
    prev_mfa_entry_name = []
    sheets_processing_order = [
        (CONST.NODES_SHEET, xl_read_nodes_sheet, [CONST.NODES_SHEET, options, sankey]),
        (CONST.PRODUCTS_SHEET, xl_read_products_sectors_sheet, [CONST.PRODUCTS_SHEET, options, sankey]),
        (CONST.SECTORS_SHEET, xl_read_products_sectors_sheet, [CONST.SECTORS_SHEET, options, sankey]),
        (CONST.EXCHANGES_SHEET, xl_read_products_sectors_sheet, [CONST.EXCHANGES_SHEET, options, sankey]),
        (CONST.IO_SHEET, xl_read_input_output_sheet, [options, mfa_dict, sankey]),
        (CONST.TER_SHEET, xl_read_terbase_sheet, [options, mfa_dict, sankey]),
        (CONST.DATA_SHEET, xl_read_data_sheet, [options, sankey]),
        (CONST.IO_DATA_SHEET, xl_read_input_output_data_sheet, [options, mfa_dict, sankey]),
        (CONST.MIN_MAX_SHEET, xl_read_min_max_sheet, [options, sankey]),
        (CONST.CONSTRAINTS_SHEET, xl_read_constraints_sheet, [options, sankey]),
        (CONST.RESULTS_SHEET, xl_read_result_sheet, [sankey]),
        # (CONST.ANALYSIS_SHEET, xl_read_analysis_sheet, [mfa_dict, sankey]),
        (CONST.UNCERTAINTY_SHEET, xl_read_uncertainty_sheet, [mfa_dict, sankey]),
        (CONST.CONVERSIONS_SHEET, xl_read_conversions_sheet, [mfa_dict, sankey])
    ]
    # Process all sheets in correct order if they exist
    for (std_sheet_name, extract_function, args) in sheets_processing_order:
        if std_sheet_name in sheet_names.keys():
            # Warn on new node creation
            if (not options['warn_on_new_nodes']) and (len(prev_mfa_entry_name) > 0):
                options['warn_on_new_nodes'] = \
                    (CONST.NODES_SHEET in prev_mfa_entry_name) or \
                    (CONST.IO_SHEET in prev_mfa_entry_name) or \
                    (CONST.TER_SHEET in prev_mfa_entry_name)
                options['warn_on_new_nodes'] |= \
                    (CONST.PRODUCTS_SHEET in prev_mfa_entry_name) and \
                    (CONST.SECTORS_SHEET in prev_mfa_entry_name) and \
                    (std_sheet_name != CONST.EXCHANGES_SHEET)
            # Warn on new flux creation
            if (not options['warn_on_new_flux']) and (len(prev_mfa_entry_name) > 0):
                options['warn_on_new_flux'] = \
                    (CONST.IO_SHEET in prev_mfa_entry_name) or \
                    (CONST.TER_SHEET in prev_mfa_entry_name) or \
                    (CONST.DATA_SHEET in prev_mfa_entry_name)
            # User sheet name
            for sheet_name in sheet_names[std_sheet_name]:
                # Extract sheet
                excel_sheet = pd.read_excel(excel_file_name, sheet_name)
                # If nothing inside -> continue
                nb_rows = excel_sheet.shape[0]
                if nb_rows < 1:
                    continue
                # Parse
                su_trace.logger.info('Reading sheet {}'.format(sheet_name))
                ok, msg = extract_function(excel_sheet, *args)
                if not ok:
                    return ok, "Error on sheet {0} ({1}) : {2}".format(sheet_name, std_sheet_name, msg)
                # Log warning messages
                if len(msg) > 0:
                    su_trace.logger.error('Warning(s) on sheet {0} ({1}) :'.format(sheet_name, std_sheet_name))
                    for _ in msg.split('\n'):
                        if len(_) > 0:
                            su_trace.logger.error(' - {}'.format(_))
                # Auto-compute missing flux
                if std_sheet_name in [CONST.IO_SHEET, CONST.TER_SHEET, CONST.DATA_SHEET, CONST.RESULTS_SHEET]:
                    ok = sankey.autocompute_missing_flux()
                    if not ok:
                        return False, ''
                # Ok node parsing
                prev_mfa_entry_name.append(std_sheet_name)
    # Synchronize all nodes levels
    sankey.autocompute_nodes_levels()
    # if sankey.has_at_least_one_mat_balance():
    # Compute mat balance
    sankey.autocompute_mat_balance()
    # else:
    #     # Recompute mat_balance only if it was specified for at least a node
    #     su_trace.logger.info('Matter balance was not specified in entry file, no computing.')

    # Overall coherence checks
    if do_coherence_checks:
        su_trace.logger.info('Overall coherence checks on Sankey structure')
        ok = sankey.check_overall_sankey_coherence()
        if not ok:
            return False, 'Sankey structure is not coherent. Abort.'
    # End
    return True, ''


def check_sheets_before_reading(sheet_names):
    """
    Verify if there are enough sheets for parsing

    Parameters
    ----------
    :param sheet_names: input file worksheet dict as [reference sheet name: user sheet name]
    :type sheet_names: dict

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)

    """
    # With data sheet, enought data to structure the Sankey
    if CONST.DATA_SHEET in sheet_names.keys():
        return True, 'OK - Data sheet'
    # No data sheet -> Do we have Node sheet ?
    if CONST.NODES_SHEET in sheet_names.keys():
        return True, 'OK - Node sheet'
    # No Node sheet -> Do we have Product & Sector ?
    if (CONST.PRODUCTS_SHEET in sheet_names.keys()) and \
       (CONST.SECTORS_SHEET in sheet_names.keys()):
        return True, 'OK - Products & Sectors sheets'
    # No product & sector sheets -> Do we have IO sheet ?
    if (CONST.IO_SHEET in sheet_names.keys()):
        return True, 'OK - IO sheets'
    # No IO sheet -> Do we have TER sheet
    if CONST.TER_SHEET in sheet_names.keys():
        return True, 'OK - TER sheet'
    # not enough sheets
    err_msg = "Not enough sheets. To create the Sankey, we need at least one of theses sheets: \n"
    err_msg += _allowedSheetNames([CONST.DATA_SHEET, CONST.NODES_SHEET, CONST.IO_SHEET, CONST.TER_SHEET])
    err_msg += "Or all theses sheets instead : \n"
    err_msg += _allowedSheetNames([CONST.PRODUCTS_SHEET, CONST.SECTORS_SHEET])
    return False, err_msg


def xl_read_tags_sheet(
    tags_sheet: dict,
    sankey: Sankey
):
    '''
    Read tags sheet.

    Parameters
    ----------
    :param tags_sheet: Feuille excel à lire
    :type tags_sheet: dict

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)
    '''
    # Keep only the first columns. Clean the remaining empty right columns.
    for i, col in enumerate(tags_sheet.columns):  # iterable on columns names
        if 'Unnamed' in col:
            tags_sheet.drop(tags_sheet.columns[i:], inplace=True, axis=1)
            break
    # Standardise les noms de colonne celon le dictionnaire si il fait partie
    # du dictionnaire sinon le recherche aussi dans les nodeTags
    tags_sheet.columns = list(map(lambda x: consistantColName(CONST.TAG_SHEET, x, sankey), tags_sheet.columns))
    # Waiting for these columns
    # Obligatory columns to have in tags sheet, with their default type
    oblig_columns = {CONST.TAG_NAME: '', CONST.TAG_TYPE: '', CONST.TAG_TAGS: ''}
    # Check if we have at least the obligatory columns
    ok, err_msg = _checkNeededColumns(tags_sheet.columns, oblig_columns.keys(), CONST.TAG_SHEET)
    if not ok:
        return ok, err_msg
    # Facultative columns we can have, with default value
    facul_columns = {CONST.TAG_IS_PALETTE: 0, CONST.TAG_COLORMAP: '', CONST.TAG_COLOR: ''}
    # Check if we need to add facultative columns
    for facul_column_name in facul_columns.keys():
        if facul_column_name not in tags_sheet.columns:
            tags_sheet[facul_column_name] = facul_columns[facul_column_name]
    # Convert data as specific type
    ok, msg = _castColumnType(
        tags_sheet, dict(oblig_columns, **facul_columns),
        empty_to_default_value=True)
    if not ok:
        return ok, msg
    # Update Sankey
    return sankey.update_from_tags_table(tags_sheet)


def xl_read_data_sheet(
    data_sheet: pd.DataFrame,
    options: dict,
    sankey: Sankey
):
    '''
    Read data sheet.

    Parameters
    ----------
    :param data_sheet: Feuille excel à lire
    :type data_sheet: pd.DataFrame

    :param options: Dictionnary of parsing options
    :type options: dict

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success code; Error message )
    :rtype: (int; string)
    '''
    # Set column header consitant with specified columns names for data sheet
    tags = list(sankey.taggs[CONST.TAG_TYPE_FLUX].keys())
    tags += list(sankey.taggs[CONST.TAG_TYPE_DATA].keys())
    new_columns_names = list(
        map(lambda x: consistantColName(CONST.DATA_SHEET, x, sankey, tags),
            data_sheet.columns))
    # Waiting for these columns
    # Obligatory columns to have in tags sheet, with their default type
    oblig_columns = {
        CONST.DATA_ORIGIN: '',
        CONST.DATA_DESTINATION: '',
        }
    # Check if we have the mandatory columns (Origin, destination, values)
    ok, msg = _checkNeededColumns(new_columns_names,  list(oblig_columns.keys()), CONST.DATA_SHEET)
    if not ok:
        return ok, msg
    # Ok to Update columns name with consistant names
    data_sheet.columns = new_columns_names
    # Facultative columns we can have, with default value
    facul_columns = {
        CONST.DATA_VALUE: 0.,
        CONST.DATA_QUANTITY: 0.0,
        CONST.DATA_FACTOR: 0.0,
        CONST.DATA_UNCERT: 0.0}
    # Convert columns data to default data type or None if Nan
    ok, msg = _castColumnType(
        data_sheet, dict(oblig_columns, **facul_columns))
    if not ok:
        return ok, msg
    # Update Sankey
    return sankey.update_from_data_table(
        data_sheet,
        options['warn_on_new_nodes'],
        options['warn_on_new_flux'])


def xl_read_nodes_sheet(
    nodes_sheet: dict,
    mfa_entry_name: str,
    options: dict,
    sankey: Sankey
):
    """
    Read node sheet.

    Parameters
    ----------
    :param nodes_sheet: Excel sheet to read (dataframe)
    :type nodes_sheet: dict

    :param mfa_entry_name: Type of sheet to parse.
    :type mfa_entry_name: str

    :param options: Dictionnary of parsing options.
    :type options: dict

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)

    """
    # Standardise les noms de colonne selon le dictionnaire,
    # sinon renvoit les noms de colones tels quels
    tags = list(sankey.taggs[CONST.TAG_TYPE_NODE].keys())
    tags += list(sankey.taggs[CONST.TAG_TYPE_LEVEL].keys())
    nodes_sheet.columns = list(
        map(lambda x: consistantColName(mfa_entry_name, x, sankey, tags),
            nodes_sheet.columns))
    # Waiting for these columns
    # Obligatory columns to have in tags sheet, with their default type
    oblig_columns = {
        CONST.NODES_LEVEL: 0,
        CONST.NODES_NODE: ''}
    # Check if we have at least the obligatory columns
    ok, msg = _checkNeededColumns(nodes_sheet.columns, list(oblig_columns.keys()), mfa_entry_name)
    if not ok:
        return ok, msg
    # Facultative columns we can have, wi
    facul_columns = {
        CONST.NODES_MAT_BALANCE: 1,
        CONST.NODES_SANKEY: 1,
        CONST.NODES_COLOR: '',
        CONST.NODES_DEFINITIONS: ''}
    # Convert to int, str, or None if Nan
    ok, msg = _castColumnType(
        nodes_sheet, dict(oblig_columns, **facul_columns))
    if not ok:
        return ok, msg
    # Update Sankey
    return sankey.update_from_nodes_table(
        nodes_sheet,
        warn_on_new_nodes=options['warn_on_new_nodes'])


def xl_read_products_sectors_sheet(
    excel_sheet: dict,
    mfa_entry_name: str,
    options: dict,
    sankey: Sankey
):
    """
    Read either Product, Sector or Exchange sheet

    Parameters
    ----------
    :param excel_sheet: Excel sheet to read (dataframe)
    :type excel_sheet: dict

    :param mfa_entry_name: Type of sheet to parse.
    :type mfa_entry_name: str

    :param options: Dictionnary of parsing options.
    :type options: dict

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)
    """
    # Add tag column
    if mfa_entry_name == CONST.PRODUCTS_SHEET:
        excel_sheet[CONST.NODE_TYPE] = CONST.NODE_TYPE_PRODUCT
    elif mfa_entry_name == CONST.SECTORS_SHEET:
        excel_sheet[CONST.NODE_TYPE] = CONST.NODE_TYPE_SECTOR
    elif mfa_entry_name == CONST.EXCHANGES_SHEET:
        excel_sheet[CONST.NODE_TYPE] = CONST.NODE_TYPE_EXCHANGE
    # Read as node
    return xl_read_nodes_sheet(
        excel_sheet,
        mfa_entry_name,
        options,
        sankey)


def xl_read_terbase_sheet(
    ter_excel_sheet: dict,
    options: dict,
    mfa_dict: dict,
    sankey: Sankey
):
    """
    Read TER sheet

    Parameters
    ----------
    :param excel_sheet: Excel sheet to read (dataframe)
    :type excel_sheet: dict

    :param options: Dictionnary of parsing options.
    :type options: dict

    :param mfa_dict: Data struct for Sankey
    :type mfa_dict: dict, modified

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)
    """
    # Extract all tables from sheet
    tables = []
    _extractTablesFromSheet(ter_excel_sheet, tables)
    if len(tables) != 2:
        err_msg = 'Could not find or extract the necessary two tables, found {}.\n'.format(len(tables))
        err_msg += 'Are all the tables here and correctly formatted ?'
        return False, err_msg
    # Do we have duplicated cols or row
    for i, table in enumerate(tables):
        has_dup_cols, dup_cols = _hasDuplicatedEntry(table.columns.to_list())
        if has_dup_cols:
            _fuseDuplicatedColumns(table, dup_cols)
        has_dup_rows, dup_rows = _hasDuplicatedEntry(table.index.to_list())
        if has_dup_rows:
            _fuseDuplicatedRows(table, dup_rows)
    # Do we have the sames columns and rows for each tables
    has_missing_entry = False
    msg = ""
    sets_headers = [(set(table.index.to_list()), set(table.columns.to_list())) for table in tables]
    for i in range(len(sets_headers) - 1):
        diff_rows = sets_headers[i][0] - sets_headers[i+1][0]
        if len(diff_rows) > 0:
            has_missing_entry = True
            msg += 'Tables {0} and {1} have incompatibles rows : {2}\n'.format(
                i, i+1, list(diff_rows))
        diff_cols = sets_headers[i][1] - sets_headers[i+1][1]
        if len(diff_cols) > 0:
            has_missing_entry = True
            msg += 'Tables {0} and {1} have incompatibles columns : {2}\n'.format(
                i, i+1, list(diff_cols))
    if has_missing_entry:
        return False, msg
    # Separate tables
    table_supplies = tables[0]  # Define flux Sectors->Products, with Cols=Sectors, Rows=Product
    table_uses = tables[1]     # Define flux Products->Sectors, with Cols=Sectors, Rows=Product
    # In Sankey struct
    log = ''
    ok, msg = sankey.update_from_matrix_table(
        table_supplies.T.replace({np.nan: None}),
        warn_on_new_nodes=options['warn_on_new_nodes'],
        warn_on_new_flux=options['warn_on_new_flux'],
        tagg_name='Type de noeud',
        tagg_type=CONST.TAG_TYPE_NODE,
        tag_name_col=CONST.NODE_TYPE_PRODUCT,
        tag_name_row=CONST.NODE_TYPE_SECTOR)
    if not ok:
        err = 'Could not process supplies table : {}'.format(msg)
        return ok, msg
    log += msg
    ok, msg = sankey.update_from_matrix_table(
        table_uses.replace({np.nan: None}),
        warn_on_new_nodes=options['warn_on_new_nodes'],
        warn_on_new_flux=options['warn_on_new_flux'],
        tagg_name='Type de noeud',
        tagg_type=CONST.TAG_TYPE_NODE,
        tag_name_col=CONST.NODE_TYPE_SECTOR,
        tag_name_row=CONST.NODE_TYPE_PRODUCT)
    log += msg
    if not ok:
        err = 'Could not process use table : {}'.format(msg)
        return ok, err
    # Set MFA dict - Needed for retrocompatibility
    # Set 'x' and 'X' as 1
    table_uses.replace({'x': 1}, inplace=True)
    table_uses.replace({'X': 1}, inplace=True)
    table_supplies.replace({'x': 1}, inplace=True)
    table_supplies.replace({'X': 1}, inplace=True)
    # Default type = int
    _castColumnType(table_uses, 0, empty_to_default_value=True)
    _castColumnType(table_supplies, 0, empty_to_default_value=True)
    # Save in MFA_dict
    mfa_dict[CONST.TER_SHEET] = {}
    mfa_dict[CONST.TER_SHEET]['use'] = table_uses
    mfa_dict[CONST.TER_SHEET]['supply'] = table_supplies
    return True, log


def xl_read_input_output_sheet(
    io_excel_sheet: dict,
    options: dict,
    mfa_input: dict,
    sankey: Sankey,
    read_data_in_matrix=False
):
    """
    Read IO sheet

    Parameters
    ----------
    :param io_excel_sheet: Excel sheet to read (dataframe)
    :type io_excel_sheet: dict

    :param options: Dictionnary of parsing options.
    :type options: dict

    :param mfa_dict: Data struct for Sankey
    :type mfa_dict: dict, modified

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)
    """
    # Extract all tables from sheet
    tables = []
    _extractTablesFromSheet(io_excel_sheet, tables)
    if len(tables) != 1:
        err_msg = 'Did not found the correct amount of tables. Need one table, found {}.'.format(len(tables))
        if len(tables) == 0:
            err_msg += '\nIs the table in the given sheet or correctly formatted ?'
        return False, err_msg
    io_sheet = tables[0]
    # Do we have duplicated cols or row
    has_dup_cols, dup_cols = _hasDuplicatedEntry(io_sheet.columns.to_list())
    if has_dup_cols:
        _fuseDuplicatedColumns(io_sheet, dup_cols)
    has_dup_rows, dup_rows = _hasDuplicatedEntry(io_sheet.index.to_list())
    if has_dup_rows:
        _fuseDuplicatedRows(io_sheet, dup_rows)
    # In Sankey struct
    ok, msg = sankey.update_from_matrix_table(
        io_sheet.replace({np.nan: None}),
        data_in_matrix=read_data_in_matrix,
        warn_on_new_nodes=options['warn_on_new_nodes'],
        warn_on_new_flux=options['warn_on_new_flux'])
    # Update MFA data dict - Needed for retrocompatibility
    # Set 'x' and 'X' as 1
    io_sheet.replace({'x': 1}, inplace=True)
    io_sheet.replace({'X': 1}, inplace=True)
    # Default type = int
    _castColumnType(io_sheet, 0, empty_to_default_value=False)
    # Save in MFA_dict
    mfa_input[CONST.IO_SHEET] = io_sheet
    # Output
    return ok, msg


def xl_read_input_output_data_sheet(
    io_excel_sheet: dict,
    options: dict,
    mfa_input: dict,
    sankey: Sankey
):
    """
    Read IO sheet

    Parameters
    ----------
    :param io_excel_sheet: Excel sheet to read (dataframe)
    :type io_excel_sheet: dict

    :param options: Dictionnary of parsing options.
    :type options: dict

    :param mfa_dict: Data struct for Sankey
    :type mfa_dict: dict, modified

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)
    """
    return xl_read_input_output_sheet(
        io_excel_sheet,
        options,
        mfa_input,
        sankey,
        read_data_in_matrix=True)


def xl_read_min_max_sheet(
    min_max_sheet: pd.DataFrame,
    options: dict,
    sankey: Sankey
):
    """
    Read CONST.MIN_MAX_SHEET.

    Parameters
    ----------
    :param min_max_sheet: Feuille excel à lire
    :type min_max_sheet: pd.DataFrame

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)
    """
    # Set column header consitant with tags groups
    tags = list(sankey.taggs[CONST.TAG_TYPE_FLUX].keys())
    tags += list(sankey.taggs[CONST.TAG_TYPE_DATA].keys())
    new_columns_names = list(
        map(lambda x: consistantColName(CONST.MIN_MAX_SHEET, x, sankey, tags),
            min_max_sheet.columns))
    # Waiting for these columns
    # Obligatory columns to have in tags sheet, with their default type
    oblig_columns = {
        CONST.MIN_MAX_ORIGIN: '',
        CONST.MIN_MAX_DESTINATION: ''}
    # All columns are here ?
    ok, msg = _checkNeededColumns(new_columns_names, list(oblig_columns.keys()), CONST.MIN_MAX_SHEET)
    if not ok:
        return ok, msg
    # Ok to Update columns name with consistant names
    min_max_sheet.columns = new_columns_names
    # Facultative columns we can have, with default value
    facul_columns = {}
    for tag in tags:
        facul_columns[tag] = ''
    # Convert to int, str, or None if Nan
    ok, msg = _castColumnType(
        min_max_sheet, dict(oblig_columns, **facul_columns))
    if not ok:
        return ok, msg
    # Update sankey struct
    ok, msg = sankey.update_from_min_max_table(
        min_max_sheet,
        options['warn_on_new_nodes'],
        options['warn_on_new_flux'])
    if not ok:
        return ok, msg
    return True, ''


def xl_read_constraints_sheet(
    constraints_sheet: pd.DataFrame,
    options: dict,
    sankey: Sankey
):
    """
    Read CONST.CONSTRAINTS_SHEET.

    Parameters
    ----------
    :param constraints_sheet: Feuille excel à lire
    :type constraints_sheet: pd.DataFrame

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)
    """
    # Set column header consitant with tags groups
    tags = list(sankey.taggs[CONST.TAG_TYPE_FLUX].keys())
    tags += list(sankey.taggs[CONST.TAG_TYPE_DATA].keys())
    new_columns_names = list(
        map(lambda x: consistantColName(CONST.CONSTRAINTS_SHEET, x, sankey, tags),
            constraints_sheet.columns))
    # Waiting for these columns
    # Obligatory columns to have in tags sheet, with their default type
    oblig_columns = {
        CONST.CONSTRAINT_ID: '',
        CONST.CONSTRAINT_ORIGIN: '',
        CONST.CONSTRAINT_DESTINATION: ''}
    onlyone_columns = {
        CONST.CONSTRAINT_EQ: 0.0,
        CONST.CONSTRAINT_INEQ_INF: 0.0,
        CONST.CONSTRAINT_INEQ_SUP: 0.0}
    # All columns are here ?
    ok, msg = _checkNeededColumns(
        new_columns_names,
        list(oblig_columns.keys()),
        CONST.CONSTRAINTS_SHEET,
        list(onlyone_columns.keys()))
    if not ok:
        return ok, msg
    # Ok to Update columns name with consistant names
    constraints_sheet.columns = new_columns_names
    # Facultative columns we can have, with default value
    facul_columns = {}
    for tag in tags:
        facul_columns[tag] = ''
    # Convert columns data to default data type or None if Nan
    ok, msg = _castColumnType(
        constraints_sheet, dict(oblig_columns, **onlyone_columns, **facul_columns))
    if not ok:
        return ok, msg
    ok, msg = sankey.update_from_constraints_table(
        constraints_sheet,
        options['warn_on_new_nodes'],
        options['warn_on_new_flux'])
    if not ok:
        return ok, msg
    return True, ''


def xl_read_result_sheet(
    result_sheet: pd.DataFrame,
    sankey: Sankey
):
    '''
    Read result sheet.

    Parameters
    ----------
    :param result_sheet: Feuille excel à lire
    :type result_sheet: pd.DataFrame

    :param options: Dictionnary of parsing options
    :type options: dict

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success code; Error message )
    :rtype: (int; string)
    '''
    # Set column header consitant with specified columns names for data sheet
    tags = list(sankey.taggs[CONST.TAG_TYPE_FLUX].keys())
    tags += list(sankey.taggs[CONST.TAG_TYPE_DATA].keys())
    new_columns_names = list(
        map(lambda x: consistantColName(CONST.RESULTS_SHEET, x, sankey, tags),
            result_sheet.columns))
    # Waiting for these columns
    # Obligatory columns to have in tags sheet, with their default type
    oblig_columns = {
        CONST.RESULTS_ORIGIN: '',
        CONST.RESULTS_DESTINATION: '',
        CONST.RESULTS_VALUE: 0.}
    # Check if we have the mandatory columns (Origin, destination, values)
    ok, msg = _checkNeededColumns(
        new_columns_names,
        list(oblig_columns.keys()),
        CONST.RESULTS_SHEET)
    if not ok:
        return ok, msg
    # Ok to Update columns name with consistant names
    result_sheet.columns = new_columns_names
    # Facultative columns we can have, with default value
    facul_columns = {
        CONST.RESULTS_FREE_MIN: 0.0,
        CONST.RESULTS_FREE_MAX: 0.0}
    # Convert columns data to default data type or None if Nan
    ok, msg = _castColumnType(
        result_sheet, dict(oblig_columns, **facul_columns))
    if not ok:
        return ok, msg
    # Update Sankey
    return sankey.update_from_result_table(result_sheet)


def xl_read_analysis_sheet(
    analysis_sheet: pd.DataFrame,
    mfa_dict: dict,
    sankey: Sankey
):
    """
    Read Analysis sheet.

    Parameters
    ----------
    :param analysis_sheet: Feuille excel à lire
    :type analysis_sheet: pd.DataFrame

    :param mfa_dict: MFA data after parsing
    :type mfa_dict: dict, modified

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)
    """
    # Set column header consitant with tags groups
    tags = list(sankey.taggs[CONST.TAG_TYPE_FLUX].keys())
    tags += list(sankey.taggs[CONST.TAG_TYPE_DATA].keys())
    new_columns_names = list(
        map(lambda x: consistantColName(CONST.ANALYSIS_SHEET, x, sankey, tags),
            analysis_sheet.columns))
    # Waiting for these columns
    # Obligatory columns to have in tags sheet, with their default type
    oblig_columns = {
        CONST.RESULTS_ORIGIN: '',
        CONST.RESULTS_DESTINATION: '',
        CONST.RESULTS_VALUE: 0.0}
    # All columns are here ?
    ok, msg = _checkNeededColumns(
        new_columns_names,
        list(oblig_columns.keys()),
        CONST.ANALYSIS_SHEET)
    if not ok:
        return ok, msg
    # Ok to Update columns name with consistant names
    analysis_sheet.columns = new_columns_names
    # Facultative columns we can have, with default value
    facul_columns = {}
    for tag in tags:
        facul_columns[tag] = ''
    # Convert columns data to default data type or None if Nan
    ok, msg = _castColumnType(
        analysis_sheet, dict(oblig_columns, **facul_columns))
    if not ok:
        return ok, msg
    # Update Sankey - analysis part
    ok, msg = sankey.update_from_analysis_table(
        analysis_sheet)
    if not ok:
        return ok, msg
    # Update MFA data dict
    mfa_dict[CONST.ANALYSIS_SHEET] = analysis_sheet
    return True, ''


def xl_read_uncertainty_sheet(
    uncertainty_sheet: pd.DataFrame,
    mfa_dict: dict,
    sankey: Sankey
):
    """
    Read UNCERTAINTY SHEET.

    Parameters
    ----------
    :param uncertainty_sheet: Feuille excel à lire
    :type uncertainty_sheet: pd.DataFrame

    :param mfa_dict: MFA data after parsing
    :type mfa_dict: dict, modified

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)
    """
    # Filter out empty columns
    for i, col in enumerate(uncertainty_sheet.columns):  # iterable on columns names
        if 'Unnamed' in col:
            uncertainty_sheet.drop(uncertainty_sheet.columns[i:], inplace=True, axis=1)
            break
    # Set column header consitant with tags groups
    tags = list(sankey.taggs[CONST.TAG_TYPE_FLUX].keys())
    tags += list(sankey.taggs[CONST.TAG_TYPE_DATA].keys())
    new_columns_names = list(
        map(lambda x: consistantColName(CONST.UNCERTAINTY_SHEET, x, sankey, tags),
            uncertainty_sheet.columns))
    # Waiting for these columns
    # Obligatory columns to have in tags sheet, with their default type
    oblig_columns = {
        CONST.UNCERTAINTY_ORIGIN: '',
        CONST.UNCERTAINTY_DESTINATION: ''}
    # All columns are here ?
    ok, msg = _checkNeededColumns(
        new_columns_names,
        list(oblig_columns.keys()),
        CONST.UNCERTAINTY_SHEET)
    if not ok:
        return ok, msg
    # Ok to Update columns name with consistant names
    uncertainty_sheet.columns = new_columns_names
    # Facultative columns we can have, with default value and default position in sheet
    facul_columns = {}
    facul_column_pos = 2
    for _ in CONST.UNCERTAINTY_SHEET_COLS:
        facul_columns['{}'.format(_)] = {'val': 0.0, 'pos': facul_column_pos}
        facul_column_pos += 1
    for tag in tags:
        facul_columns[tag] = {'val': '', 'pos': facul_column_pos}
        facul_column_pos += 1
    # Check if we need to add facultative columns
    for facul_column_name, facul_column in facul_columns.items():
        if facul_column_name not in uncertainty_sheet.columns:
            uncertainty_sheet.insert(
                facul_column['pos'], facul_column_name, facul_column['val'])
    # Convert to int, str, or None if Nan
    ok, msg = _castColumnType(
        uncertainty_sheet,
        dict(oblig_columns, **facul_columns),
        empty_to_default_value=True)
    if not ok:
        return ok, msg
    # Update Sankey - Uncertainty part
    ok, msg = sankey.update_from_uncertainty_table(
        uncertainty_sheet)
    if not ok:
        return ok, msg
    mfa_dict[CONST.UNCERTAINTY_SHEET] = uncertainty_sheet
    return True, ''


def xl_read_conversions_sheet(
    conversions_sheet: dict,
    mfa_dict: dict,
    sankey: Sankey
):
    """
    Read CONVERSION SHEET.
    TODO this sheet must be changed.

    Parameters
    ----------
    :param conversions_sheet: Feuille excel à lire
    :type conversions_sheet: pd.DataFrame

    :param mfa_dict: MFA data after parsing
    :type mfa_dict: dict, modified

    :param sankey: Sankey struct constructed from input
    :type sankey: Sankey, modified

    Returns
    -------
    :return: (Success ; Error message )
    :rtype: (bool; string)
    """
    # Set column header consitant with tags groups
    new_columns_names = list(
        map(lambda x: consistantColName(CONST.CONVERSIONS_SHEET, x, sankey),
            conversions_sheet.columns))
    # Waiting for these columns
    oblig_columns = {
        CONST.CONVERSIONS_LOCATION: '',
        CONST.CONVERSIONS_PRODUCT: '',
        CONST.CONVERSIONS_NATURAL_UNIT: '',
        CONST.CONVERSIONS_FACTOR: 0.0}
    # All columns are here ?
    ok, msg = _checkNeededColumns(new_columns_names, list(oblig_columns.keys()), CONST.CONVERSIONS_SHEET)
    if not ok:
        return ok, msg
    # Ok to Update columns name with consistant names
    conversions_sheet.columns = new_columns_names
    # # Facultative columns we can have, with default value
    # facul_columns = {
    #     CONST.CONVERSIONS_FACTOR_INV: 0.0}
    # # Convert columns data to default data type or None if Nan
    # ok, msg = _castColumnType(
    #     conversions_sheet.iloc[1:], dict(oblig_columns, **facul_columns))
    # if not ok:
    #     return ok, msg
    conversions_sheet.replace({np.nan: None}, inplace=True)
    # Update Sankey - analysis part
    nodes = []
    ok, msg = sankey.update_from_conversions_table(conversions_sheet, nodes)
    if not ok:
        return ok, msg
    # Update MFA data dict
    nodes2tooltips = {}
    nodes2units_conv = {}
    nodes2natural_unit = {}
    for node in nodes:
        for localisation in node.unit.keys():
            name = localisation + '/' + node.name
            node2tooltips = []
            node2units_conv = [1.0]
            for tooltip in sankey.tooltips.keys():
                if tooltip in node.tooltips.keys():
                    node2tooltips.append(node.tooltips[tooltip].content)
                else:
                    node2tooltips.append(None)
            for unit in sankey.units.keys():
                other_factors = node.get_other_factors(localisation)
                try:
                    node2units_conv.append(other_factors[unit])
                except Exception:
                    node2units_conv.append(None)
            nodes2tooltips[name] = node2tooltips
            nodes2units_conv[name] = node2units_conv
            nodes2natural_unit[name] = node.get_natural_unit(localisation)
    mfa_dict[CONST.CONVERSIONS_SHEET] = {
        'tooltip_names': [[name, desc] for name, desc in sankey.tooltips.items()],
        'units_names': [[name, desc] for name, desc in sankey.units.items()],
        'nodes2tooltips': nodes2tooltips,
        'nodes2units_conv': nodes2units_conv,
        'nodes2natural_unit': nodes2natural_unit}
    return True, ''


def write_excel_from_sankey(
    excel_filename: str,
    sankey: Sankey,
    mode: str = 'a',
    sheets_to_remove__names: list = [],
    **kwargs
):
    """
    _summary_

    Parameters
    ----------
    :param excel_filename: Name of Excel file to write
    :type excel_filename: str

    :param sankey: Sankey structure to write to Excel file
    :type sankey: Sankey

    Optional parameters
    -------------------
    :param mode: Writing mode (see pandas.ExcelWriter for more infos)
    :type mode: str, optional (defaults to 'a')

    :param sheets_to_remove__names: List of sheets (by name) to remove for Excel file if they are present
    :type sheets_to_remove__names: list[str, ...], optional (defaults to [])

    Hidden parameters
    -----------------
    :param additional_sheets: Dict of tables (pandas.DataFrame) to add in Excel file
    :type additional_sheets: Dict{str: pandas.DataFrame}
    """
    # Post-process function
    def _post_process_excel_file(
        excel_file
    ):
        # Extract excel book
        excel = excel_file.book
        # Remove sheets
        for sheet_to_remove__name in sheets_to_remove__names:
            sheets = excel._sheets
            try:
                sheet_to_remove__id = sheets.index(excel[sheet_to_remove__name])
                sheet = sheets.pop(sheet_to_remove__id)
            except Exception:
                pass
        # Read-me sheet must always be the first sheet
        try:
            read_me_sheet__id = excel.worksheets.index(excel['READ ME'])
            sheet = sheets.pop(read_me_sheet__id)
            sheets.insert(0, sheet)
        except Exception:
            pass
        # File is open and saved by xlwings to activate the formulas.
        # if has_xl_wings:
        #     try:
        #         app = xl.App(visible=False)
        #         book = app.books.open(excel_filename)
        #         book.save()
        #         app.kill()
        #     except Exception:
        #         pass
    # Write sheets from sankey
    if mode == 'a':
        with pd.ExcelWriter(excel_filename, engine='openpyxl', mode=mode, if_sheet_exists='replace') as excel_file:
            sankey.write_in_excel_file(excel_file, **kwargs)
            _post_process_excel_file(excel_file)
    else:
        with pd.ExcelWriter(excel_filename, engine='openpyxl', mode=mode) as excel_file:
            sankey.write_in_excel_file(excel_file, **kwargs)
            _post_process_excel_file(excel_file)
