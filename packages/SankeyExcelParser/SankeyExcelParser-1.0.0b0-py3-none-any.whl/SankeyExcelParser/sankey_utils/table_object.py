"""
Author : Vincent LE DOZE
Date : 31/05/23

This file contains descriptions for sankey proto class

"""


# CLASS ----------------------------------------------------------------------------
class TableObject(object):
    """
    Define an object that is created from given table

    :param extra_infos: Extra infos related to the object.
    :type extra_infos: dict {info_name: info_content}

    :param excel_source: Source Excel data.
    :type excel_source: ExcelSource
    """
    def __init__(self):
        self._extra_infos = {}
        self._excel_source = None

    @property
    def extra_infos(self):
        return self._extra_infos

    @property
    def extra_infos_name(self):
        return list(self._extra_infos.keys())

    def add_extra_info(self, info_name, info_content):
        self._extra_infos[info_name] = info_content

    def add_extra_infos(self, info_dict):
        self._extra_infos.update(info_dict)
