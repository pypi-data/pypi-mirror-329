"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains functions used in sankey_utils modules

"""

# External libs ----------------------------------------------------------------
import pandas as pd
import re
import webcolors

# External modules ------------------------------------------------------------
from unidecode import unidecode


# FUNCTIONS -------------------------------------------------------------------
def _stdStr(s):
    """
    Returns standardize format for input string.

    Parameters
    ----------
    :param s: input.
    :type s: str | set | list

    Returns
    -------
    :return: formatted string(s).
    :rtype: same type as input
    """
    if type(s) is str:
        return unidecode(s).strip().lower().replace('.0', '')
    if type(s) is set:
        new_s = set()
        for _ in s:
            new_s.add(_stdStr(_))
        return s
    if type(s) is list:
        return [_stdStr(_) for _ in s]


def _getValueIfPresent(
    line: pd.Series,
    index: int,
    default_value
):
    """
    Extract the value from a table line for given column name.
    If nothing is found, returns a default value.

    Parameters
    ----------
    :param line: Line where the info should be find.
    :type line: pd.Series

    :param index: Column name under which we should find a value
    :type index: int

    :param default_value: If no value is found under the given column, this is the default output.

    Returns
    -------
    :return: Found value or default value if nothing is found.
    """
    value = line[index] if index in line.index else default_value
    return value


def _extractFluxFromMatrix(
    table: pd.DataFrame,
    origins: list,
    destinations: list,
    values: list
):
    """
    Extract flux from a matrix as following:

    +------+------+------+------+
    | -    | C4   | C5   | C6   |
    +======+======+======+======+
    | R3   | None | x    | x    |
    +------+------+------+------+
    | R4   | x    | None | None |
    +------+------+------+------+

    Parameters
    ----------
    :param table: Matrix table (rows = Origins, cols = Destinations)
    :type table: pd.DataFrame

    :param origins: List of all origins
    :type origins: list, modified

    :param destinations: List of all destinations
    :type destinations: list, modified

    :param values: List of all values for flux
    :type values: list, modified

    """
    for orig in table.index:
        for dest in table.columns:
            if orig == dest:
                continue
            v = table.loc[orig][dest]
            ok = (v is not None) and (v != 0) and (v != "0")
            if ok:
                origins.append(orig)
                destinations.append(dest)
                if re.fullmatch('[xX]', str(v)) is not None:
                    values.append(None)
                else:
                    values.append(float(v))


def _createMatrixFromFlux(
    origins: list,
    destinations: list,
    transpose=False
):
    """
    Create a matrix table (rows = Origins, cols = Destinations)

    Parameters
    ----------
    :param origins: List of all origin nodes
    :type origins: list[Node]

    :param destinations: List of all destination nodes
    :type destinations: list[Node]

    :param transpose: Return matrix as transpose version
    :type transpose: bool

    Returns
    -------
    :return: matrix table (rows = Origins, cols = Destinations).
        If "x" we have a flux from origin to destination
        If None we dont have a flux
    :rtype: list[list]
    """
    table = []
    if transpose:
        for destination in destinations:
            # Init new row
            row = []
            # Get all nodes that are registred as a flux destination from origin
            registered_origins = \
                [flux.orig for flux in destination.input_flux]
            # If we have such nodes
            if len(registered_origins) > 0:
                for origin in origins:
                    # 'x' if we have a flux origin -> destination
                    # None otherwise
                    if origin in registered_origins:
                        row.append('x')
                    else:
                        row.append(None)
            else:
                row += [None]*len(origins)
            # Add row to table
            table.append(row)
    else:
        for origin in origins:
            # Init new row
            row = []
            # Get all nodes that are registred as a flux destination from origin
            registered_destinations = \
                [flux.dest for flux in origin.output_flux]
            # If we have such nodes
            if len(registered_destinations) > 0:
                for destination in destinations:
                    # 'x' if we have a flux origin -> destination
                    # None otherwise
                    if destination in registered_destinations:
                        row.append('x')
                    else:
                        row.append(None)
            else:
                row += [None]*len(destinations)
            # Add row to table
            table.append(row)
    # Create and return panda table
    return table


def is_hex(s):
    return re.fullmatch(r"^\# ?[0-9a-fA-F]+$", s or "") is not None


def _convertColorToHex(color, default_color=''):
    """
    Convert a color str to hex value.

    Parameters
    ----------
    :param color: color to convert
    :type color: str
    """
    if type(color) is str:
        # is the color as hexa ?
        if (re.fullmatch(r"^\# ?[0-9a-fA-F]+$", color) is not None) or (color == ""):
            return color
        else:
            return webcolors.name_to_hex(color)
    return default_color


def _reorderTable(
    table: pd.DataFrame,
    cols: list,
    contents: list
):
    """
    Reorder table lines accordlying to values presents in list of cols

    Example :
    -------
    Col 1 | Col 2 | Col 3
    ---------------------
    a     | 1     | 2
    b     | 2     | 2
    c     | 2     | 1
    d     | 1     | 2

    Reordering as [Col2, Col3] gives
    Col 1 | Col 2 | Col 3
    ---------------------
    a     | 1     | 2
    d     | 1     | 2
    c     | 2     | 1
    b     | 2     | 2

    Parameters
    ----------
    :param table: Table to reorder
    :type table: panda.DataFrame

    :param cols: List of ref columns for reordering
    :type cols: list as [str, ...]

    :param contents: List possible content per col. Must be ordered following this.
    If content not in this list, then will be processed at the end.
    :type contents: list as [list as [str, ...], ...]

    Returns
    -------
    :return: Reordered table
    :rtype: panda.DataFrame

    """
    # No more ordering cols -> return table
    if len(cols) == 0:
        return table
    # Create new table to get block of sorted subtables
    new_table = pd.DataFrame(columns=table.columns)
    sorting_col = cols.pop()
    sorting_contents = contents.pop()
    present_contents = table[sorting_col].unique()
    # Update sorting content with unexpected content
    prio_sorting_contents = [_ for _ in sorting_contents if _ in present_contents]
    other_sorting_contents = [_ for _ in present_contents if _ not in sorting_contents]
    sorting_contents = prio_sorting_contents + other_sorting_contents
    # Sort
    for value in sorting_contents:
        # Get subtable
        if value is None:
            sub_table = table.loc[table[sorting_col].isnull()]
        else:
            sub_table = table.loc[table[sorting_col] == value]
        # Recursive filtering of sub_table
        if len(cols) > 0:
            sub_table = _reorderTable(sub_table, cols.copy(), contents.copy())
        # Appending results
        new_table = new_table._append(sub_table, ignore_index=True)
    return new_table
