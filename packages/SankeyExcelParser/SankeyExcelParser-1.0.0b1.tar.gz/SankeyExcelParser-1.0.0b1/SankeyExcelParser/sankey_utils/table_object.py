'''
==================================================================================================
The MIT License (MIT)
==================================================================================================
Copyright (c) 2025 TerriFlux

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
==================================================================================================
Author        : Vincent LE DOZE & Vincent CLAVEL & Julien Alapetite for TerriFlux
==================================================================================================

Author : Vincent LE DOZE
Date : 31/05/23

This file contains descriptions for sankey proto class

'''


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
