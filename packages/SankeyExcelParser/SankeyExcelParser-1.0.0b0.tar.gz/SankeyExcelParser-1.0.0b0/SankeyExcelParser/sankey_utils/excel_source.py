"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains description for ExcelSource class

"""

# External libs ----------------------------------------------------------------
import pandas as pd


# CLASS ----------------------------------------------------------------------------
class ExcelSource(object):
    user_sheet_name: str
    sheet_type: str
    _table: pd.DataFrame

    def __init__(
        self,
        user_sheet_name: str,
        sheet_type: str,
    ):
        self.user_sheet_name = user_sheet_name
        self.sheet_type = sheet_type

    def save_origin_table(
        self,
        table: pd.DataFrame
    ):
        self.table = table
